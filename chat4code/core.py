"""
chat4code 核心模块
"""

import os
import json
import hashlib
import re
from datetime import datetime
from typing import List, Tuple, Dict, Optional, Set
from .tasks import TaskManager
from .parser import ResponseParser
from .validator import ResponseValidator
from .config import ConfigManager
import fnmatch
import glob

class CodeProjectAIHelper:
    def __init__(self):
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 从配置获取设置
        self.language_map = self.config_manager.get_language_map()
        self.default_extensions = self.config_manager.get_extensions()
        self.metadata_dir = self.config_manager.get_metadata_dir()
        self.exclude_patterns = self.config_manager.get_exclude_patterns()
        
        # 初始化子模块（传递配置中的提示词文件路径）
        prompts_file = self.config_manager.get("prompts_file", None)
        try:
            self.task_manager = TaskManager(prompts_file)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            print("\n💡 解决方案:")
            print("   1. 运行 'python -m chat4code --config-init' 初始化配置")
            print("   2. 或者手动创建 prompts.yaml 文件")
            print("   3. 或者在 .chat4code.json 中指定 prompts_file 路径")
            raise
        except Exception as e:
            print(f"❌ 初始化任务管理器失败: {e}")
            raise
            
        self.response_parser = ResponseParser()
        self.response_validator = ResponseValidator()

    def get_next_sequential_filename(self, pattern: str, output_dir: str) -> str:
        """
        获取下一个序列化文件名
        例如: req.md -> req1.md, req2.md, req3.md...
        """
        # 分离文件名和扩展名
        base_name, ext = os.path.splitext(pattern)
        
        # 获取目录中已有的文件
        existing_files = []
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                if file.startswith(base_name) and file.endswith(ext):
                    existing_files.append(file)
        
        # 找到最大的序列号
        max_num = 0
        for file in existing_files:
            # 匹配 req1.md, req2.md 这样的模式
            match = re.match(rf'{re.escape(base_name)}(\d+){re.escape(ext)}', file)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
        
        # 生成下一个序列号
        next_num = max_num + 1
        new_filename = f"{base_name}{next_num}{ext}"
        return os.path.join(output_dir, new_filename)

    def _match_source_dirs(self, src_dirs: List[str], base_dir: str = ".") -> List[str]:
        """
        根据模式匹配源目录
        支持通配符如 'ex*' 匹配 ex 开头的目录
        """
        matched_dirs = []
        if not src_dirs:
            return [base_dir]
            
        for src_dir in src_dirs:
            # 如果是绝对路径或已包含路径分隔符，则直接使用
            if os.path.isabs(src_dir) or os.sep in src_dir or (os.altsep and os.altsep in src_dir):
                if os.path.exists(src_dir):
                    matched_dirs.append(src_dir)
                else:
                    print(f"⚠️ 指定的源目录不存在: {src_dir}")
            else:
                # 在 base_dir 下查找匹配的目录
                search_path = os.path.join(base_dir, src_dir)
                if '*' in src_dir or '?' in src_dir:
                    # 使用 glob 匹配
                    matches = glob.glob(search_path)
                    for match in matches:
                        if os.path.isdir(match):
                            matched_dirs.append(match)
                else:
                    # 直接检查目录是否存在
                    if os.path.exists(search_path) and os.path.isdir(search_path):
                        matched_dirs.append(search_path)
                    else:
                        print(f"⚠️ 指定的源目录不存在: {search_path}")
        
        if not matched_dirs:
            print("⚠️ 未找到匹配的源目录，使用默认目录")
            matched_dirs = [base_dir]
            
        return matched_dirs

    def export_to_markdown(self, src_dirs: List[str] = None, output_file: str = None, 
                          extensions: tuple = None, task: str = None,
                          incremental: bool = False, since_time: str = None,
                          include_task_prompt: bool = False) -> str:
        """
        导出代码到Markdown，支持增量导出和智能任务提示
        默认任务提示显示在屏幕上，使用 --task-prompt 时包含在导出文件中
        支持多个源目录和模式匹配
        """
        # 使用配置中的默认值
        if src_dirs is None:
            src_dirs = self.config_manager.get_default_source_dirs()
        
        # 匹配源目录
        matched_src_dirs = self._match_source_dirs(src_dirs)
        
        if extensions is None:
            extensions = self.default_extensions
            
        # 检查所有源目录是否存在
        for src_dir in matched_src_dirs:
            if not os.path.exists(src_dir):
                raise FileNotFoundError(f"源目录不存在: {src_dir}")
        
        # 如果没有指定输出文件，使用序列化文件名
        if output_file is None:
            export_pattern = self.config_manager.get_export_filename_pattern()
            export_dir = self.config_manager.get_export_output_dir()
            output_file = self.get_next_sequential_filename(export_pattern, export_dir)
            print(f"ℹ️  使用自动序列化文件名: {output_file}")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
         
        # 检测项目类型（支持配置强制指定）
        project_type = self._detect_project_type_multi(matched_src_dirs, extensions)
        
        # 如果是增量导出，获取变更的文件
        changed_files = None
        if incremental:
            changed_files = self._get_changed_files_multi(matched_src_dirs, since_time)
        
        markdown_lines = []
        
        # 添加标题和基本信息
        markdown_lines.append("# 项目代码导出")
        markdown_lines.append(f"项目名称: {', '.join([os.path.basename(os.path.abspath(src_dir)) for src_dir in matched_src_dirs])}")
        markdown_lines.append(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        markdown_lines.append(f"源目录: {', '.join([os.path.abspath(src_dir) for src_dir in matched_src_dirs])}")
        markdown_lines.append(f"项目类型: {project_type}")
        if self.config_manager.get_project_type():
            markdown_lines.append("类型来源: 配置指定")
        else:
            markdown_lines.append("类型来源: 自动检测")
        if incremental:
            markdown_lines.append("模式: 增量导出")
            if since_time:
                markdown_lines.append(f"自时间: {since_time}")
            else:
                markdown_lines.append("自上次导出以来的变更")
        markdown_lines.append(" ")
        markdown_lines.append("---")
        markdown_lines.append(" ")
        
        # 如果有任务，处理任务提示
        task_info = None
        if task and self.task_manager.has_task(task):
            task_info = self.task_manager.get_task_info(task, project_type)
            if include_task_prompt:
                # 在导出文件中包含任务提示
                markdown_lines.append("## AI任务提示")
                markdown_lines.append(" ")
                markdown_lines.append("**请按照以下要求执行任务**: ")
                markdown_lines.append(task_info['prompt'])
                markdown_lines.append(" ")
                markdown_lines.append("---")
                markdown_lines.append(" ")
            else:
                # 只在屏幕上显示任务提示，不在导出文件中包含
                print("\n=== AI任务提示 ===")
                print("请按照以下要求执行任务: ")
                print(task_info['prompt'])
                print("==================\n")
        
        # 遍历所有匹配的目录
        file_count = 0
        for src_dir in matched_src_dirs:
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith(extensions):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, src_dir)
                        
                        # 检查是否应该排除此文件
                        if self._should_exclude_file(rel_path, self.exclude_patterns):
                            continue
                        
                        # 如果是增量导出，只处理变更的文件
                        if incremental and changed_files is not None:
                            if rel_path not in changed_files:
                                continue
                        
                        # 添加文件标题
                        markdown_lines.append(f"## {rel_path}")
                        markdown_lines.append(" ")
                        
                        # 确定代码语言
                        lang = self._get_language_by_extension(file)
                        markdown_lines.append(f"```{lang}")
                        
                        # 读取文件内容
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            markdown_lines.append(content)
                        except UnicodeDecodeError:
                            markdown_lines.append("[该文件无法读取，请检查编码或文件类型]")
                        except Exception as e:
                            markdown_lines.append(f"[读取文件时发生错误: {str(e)}]")
                        
                        markdown_lines.append("```")
                        markdown_lines.append(" ")
                        file_count += 1
        
        if file_count == 0:
            markdown_lines.append("## 未找到匹配的代码文件")
            if incremental:
                markdown_lines.append("自上次导出以来没有文件变更")
            markdown_lines.append(f"请检查目录路径和文件扩展名: {', '.join(extensions)}")
            markdown_lines.append(" ")
        
        markdown_content = "\n".join(markdown_lines)
        
        # 如果指定了输出文件，则保存；否则打印到控制台
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"✅ 项目已导出到: {output_file}")
            print(f"📁 包含 {file_count} 个代码文件")
            
            # 保存导出元数据（用于增量导出）
            if not incremental:
                self._save_export_metadata_multi(matched_src_dirs, output_file)
        else:
            # 输出到控制台
            print(markdown_content)
        
        return output_file

    def apply_markdown_response(self, markdown_file: str = None, dst_dir: str = None, 
                                create_backup: bool = None, 
                                flexible_parsing: bool = True,
                                show_diff: bool = False) -> Dict:
        """
        应用Markdown响应到本地目录，支持差异显示
        """
        # 使用配置中的默认值
        if markdown_file is None:
            import_pattern = self.config_manager.get_import_filename_pattern()
            import_dir = self.config_manager.get_import_output_dir()
            markdown_file = self.get_next_sequential_filename(import_pattern, import_dir)
            print(f"ℹ️  使用自动序列化导入文件: {markdown_file}")
        
        if dst_dir is None:
            dst_dir = self.config_manager.get_default_target_dir()
        
        # 如果未指定备份选项，使用配置中的默认值
        if create_backup is None:
            create_backup = self.config_manager.is_backup_enabled()
            
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        
        # 读取Markdown文件
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except Exception as e:
            raise Exception(f"读取Markdown文件失败: {e}")
        
        # 提取文件信息
        if flexible_parsing:
            files = self.response_parser.extract_files_flexible(markdown_content)
        else:
            files = self.response_parser.extract_files_standard(markdown_content)
        
        result = {
            'success': [],
            'failed': [],
            'total': len(files),
            'parsed_files': [f[0] for f in files],
            'diffs': []  # 用于存储差异信息
        }
        
        for file_path, lang, content in files:
            try:
                # 检查是否为删除操作
                if lang == 'deleted' or content == 'DELETED':
                    # 删除文件操作
                    full_path = os.path.join(dst_dir, file_path)
                    if os.path.exists(full_path):
                        if create_backup:
                            backup_path = f"{full_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                            os.rename(full_path, backup_path)
                            print(f"🗑️  删除文件 (已备份): {full_path}")
                            result['deleted'].append({
                                'file': full_path,
                                'backup': backup_path
                            })
                        else:
                            os.remove(full_path)
                            print(f"🗑️  删除文件: {full_path}")
                            result['deleted'].append({
                                'file': full_path,
                                'backup': None
                            })
                    else:
                        print(f"⚠️  文件不存在，无法删除: {full_path}")
                        result['failed'].append({
                            'file': file_path,
                            'error': '文件不存在，无法删除'
                        })
                    continue

                # 构建完整路径
                full_path = os.path.join(dst_dir, file_path)
                
                # 检查是否应该排除此文件
                if self._should_exclude_file(file_path, self.exclude_patterns):
                    print(f"⚠️  跳过排除的文件: {file_path}")
                    continue
                
                # 如果需要显示差异，计算差异
                diff_info = None
                if show_diff and os.path.exists(full_path):
                    diff_info = self._calculate_diff(full_path, content)
                
                # 创建目录
                file_dir = os.path.dirname(full_path)
                if file_dir and not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                
                # 创建备份（如果文件已存在且需要备份）
                backup_path = None
                if create_backup and os.path.exists(full_path):
                    backup_path = f"{full_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    os.rename(full_path, backup_path)
                
                # 写入文件
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                success_info = {
                    'file': full_path,
                    'language': lang,
                    'backup': backup_path
                }
                
                if diff_info:
                    success_info['diff'] = diff_info
                    result['diffs'].append({
                        'file': full_path,
                        'diff': diff_info
                    })
                
                result['success'].append(success_info)
                print(f"✅ 创建/更新文件: {full_path}")
                
                # 显示差异（如果需要）
                if show_diff and diff_info:
                    print(f"   差异信息: {diff_info['summary']}")
                
            except Exception as e:
                result['failed'].append({
                    'file': file_path,
                    'error': str(e)
                })
                print(f"❌ 处理文件失败 {file_path}: {e}")
        
        # 输出统计信息
        print(f"\n📊 处理完成: {len(result['success'])}/{result['total']} 个文件成功")
        if result['failed']:
            print("❌ 失败的文件: ")
            for item in result['failed']:
                print(f"   - {item['file']}: {item['error']}")
        
        # 显示详细差异报告
        if show_diff and (result['diffs'] or result['deleted']):
            print("\n📝 差异详情: ")
            print("= " * 50)
            for diff_info in result['diffs']:
                print(f"\n文件: {diff_info['file']}")
                print(f"差异: {diff_info['diff']['summary']}")
                if diff_info['diff']['lines_added'] > 0:
                    print(f"      + 新增 {diff_info['diff']['lines_added']} 行")
                if diff_info['diff']['lines_removed'] > 0:
                    print(f"      - 删除 {diff_info['diff']['lines_removed']} 行")
                if diff_info['diff']['lines_modified'] > 0:
                    print(f"      ~ 修改 {diff_info['diff']['lines_modified']} 行")

            # 显示删除的文件
            if 'deleted' in result and result['deleted']:
                print(f"\n🗑️  删除的文件: ")
                for deleted_info in result['deleted']:
                    print(f"   - {deleted_info['file']}")
                    if deleted_info['backup']:
                        print(f"     (已备份: {deleted_info['backup']})")
        
        return result

    def _should_exclude_file(self, file_path: str, exclude_patterns: List[str]) -> bool:
        """检查文件是否应该被排除"""
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
            # 也检查目录模式
            if pattern.endswith('/') and file_path.startswith(pattern):
                return True
        return False

    def _detect_project_type_multi(self, src_dirs: List[str], extensions: tuple = None) -> str:
        """
        检测多个目录的项目类型（C++、Python、JavaScript等）
        如果配置中指定了项目类型，则使用配置的类型
        """
        # 首先检查配置中是否强制指定了项目类型
        config_project_type = self.config_manager.get_project_type()
        if config_project_type:
            print(f"ℹ️  使用配置指定的项目类型: {config_project_type}")
            return config_project_type
        
        # 否则自动检测项目类型（基于文件数量）
        if extensions is None:
            extensions = self.default_extensions
        
        # 统计各类型文件数量
        cpp_extensions = {'.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp'}
        python_extensions = {'.py'}
        js_extensions = {'.js', '.ts', '.jsx', '.tsx'}
         
        cpp_count = 0
        python_count = 0
        js_count = 0
        
        for src_dir in src_dirs:
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith(extensions):
                        _, ext = os.path.splitext(file.lower())
                        if ext in cpp_extensions:
                            cpp_count += 1
                        elif ext in python_extensions:
                            python_count += 1
                        elif ext in js_extensions:
                            js_count += 1
        
        print(f"🔍 项目类型检测结果: ")
        print(f"   C++ 文件: {cpp_count} 个")
        print(f"   Python 文件: {python_count} 个")
        print(f"   JavaScript 文件: {js_count} 个")
        
        # 根据文件数量最多的类型来判断
        if cpp_count > python_count and cpp_count > js_count:
            detected_type = "cpp"
        elif python_count > cpp_count and python_count > js_count:
            detected_type = "python"
        elif js_count > cpp_count and js_count > python_count:
            detected_type = "javascript"
        else:
            detected_type = "generic"
        
        print(f"   检测到项目类型: {detected_type}")
        return detected_type

    def _get_changed_files_multi(self, src_dirs: List[str], since_time: str = None) -> Set[str]:
        """
        获取多个目录中变更的文件列表
        """
        changed_files = set()
        
        for src_dir in src_dirs:
            changed_in_dir = self._get_changed_files(src_dir, since_time)
            changed_files.update(changed_in_dir)
            
        return changed_files

    def _get_changed_files(self, src_dir: str, since_time: str = None) -> set:
        """
        获取变更的文件列表
        """
        changed_files = set()
        
        # 如果指定了时间，比较文件修改时间
        if since_time:
            try:
                since_timestamp = datetime.fromisoformat(since_time).timestamp()
            except:
                since_timestamp = 0
            
            for root, _, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, src_dir)
                    # 检查是否应该排除
                    if self._should_exclude_file(rel_path, self.exclude_patterns):
                        continue
                    if os.path.getmtime(file_path) > since_timestamp:
                        changed_files.add(rel_path)
        else:
            # 否则比较文件哈希值
            metadata_file = os.path.join(self.metadata_dir, "export_metadata.json")
            if os.path.exists(metadata_file):
                try:
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    current_hashes = self._get_file_hashes(src_dir)
                    previous_hashes = metadata.get('file_hashes', {})
                     
                    for file_path, current_hash in current_hashes.items():
                        # 检查是否应该排除
                        if self._should_exclude_file(file_path, self.exclude_patterns):
                            continue
                        previous_hash = previous_hashes.get(file_path)
                        if previous_hash != current_hash:
                            changed_files.add(file_path)
                except:
                    # 如果无法读取元数据，返回所有文件（排除排除的文件）
                    for root, _, files in os.walk(src_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, src_dir)
                            if not self._should_exclude_file(rel_path, self.exclude_patterns):
                                changed_files.add(rel_path)
            else:
                # 如果没有元数据，返回所有文件（排除排除的文件）
                for root, _, files in os.walk(src_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, src_dir)
                        if not self._should_exclude_file(rel_path, self.exclude_patterns):
                            changed_files.add(rel_path)
        
        return changed_files

    def _get_file_hashes(self, src_dir: str) -> Dict[str, str]:
        """
        获取目录中所有文件的哈希值（排除指定的文件）
        """
        file_hashes = {}
        for root, _, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, src_dir)
                # 检查是否应该排除
                if self._should_exclude_file(rel_path, self.exclude_patterns):
                    continue
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        file_hash = hashlib.md5(content).hexdigest()
                        file_hashes[rel_path] = file_hash
                except:
                    file_hashes[rel_path] = " "
        return file_hashes

    def _save_export_metadata_multi(self, src_dirs: List[str], output_file: str):
        """
        保存多个目录的导出元数据，用于增量导出
        """
        if not os.path.exists(self.metadata_dir):
            os.makedirs(self.metadata_dir)
        
        all_file_hashes = {}
        for src_dir in src_dirs:
            dir_hashes = self._get_file_hashes(src_dir)
            all_file_hashes.update(dir_hashes)
            
        metadata = {
            'export_time': datetime.now().isoformat(),
            'source_dirs': [os.path.abspath(src_dir) for src_dir in src_dirs],
            'output_file': os.path.abspath(output_file),
            'file_hashes': all_file_hashes
        }
         
        metadata_file = os.path.join(self.metadata_dir, "export_metadata.json")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

    def _calculate_diff(self, file_path: str, new_content: str) -> Dict:
        """
        计算文件差异（更详细的实现）
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
        except:
            # 如果文件不存在或无法读取，认为是新增文件
            return {
                'type': 'new_file',
                'summary': '新增文件',
                'lines_added': len(new_content.split('\n')),
                'lines_removed': 0,
                'lines_modified': 0
            }
        
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        # 检查内容是否完全相同
        if old_content == new_content:
            return {
                'type': 'no_change',
                'summary': '无变化',
                'lines_added': 0,
                'lines_removed': 0,
                'lines_modified': 0
            }
        
        # 计算基本差异统计
        old_line_count = len(old_lines)
        new_line_count = len(new_lines)
         
        lines_added = max(0, new_line_count - old_line_count)
        lines_removed = max(0, old_line_count - new_line_count)
        
        # 简单的差异描述
        if lines_added > 0 and lines_removed > 0:
            summary = f'修改文件 (新增{lines_added}行, 删除{lines_removed}行)'
        elif lines_added > 0:
            summary = f'修改文件 (新增{lines_added}行)'
        elif lines_removed > 0:
            summary = f'修改文件 (删除{lines_removed}行)'
        else:
            summary = '修改文件内容'
        
        return {
            'type': 'modified',
            'summary': summary,
            'lines_added': lines_added,
            'lines_removed': lines_removed,
            'lines_modified': 0
        }

    def _get_language_by_extension(self, filename: str) -> str:
        """根据文件扩展名获取编程语言"""
        _, ext = os.path.splitext(filename.lower())
        return self.language_map.get(ext, 'text')

    def validate_response_format(self, markdown_content: str, verbose: bool = False) -> Dict:
        """
        验证AI响应格式是否正确
        """
        return self.response_validator.validate(markdown_content, verbose)

    def list_supported_extensions(self) -> List[str]:
        """列出支持的文件扩展名"""
        return sorted(list(set(self.language_map.keys())))

    def debug_parse_response(self, markdown_file: str):
        """
        调试方法：显示解析结果
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("=== 标准解析结果 ===")
            standard_files = self.response_parser.extract_files_standard(content)
            for i, (file_path, lang, file_content) in enumerate(standard_files):
                print(f"文件 {i+1}: {file_path} ({lang})")
                print(f"内容长度: {len(file_content)} 字符")
                print("---")
            
            print(f"\n总共识别到 {len(standard_files)} 个文件")
            
            if not standard_files:
                print("\n=== 灵活解析结果 ===")
                flexible_files = self.response_parser.extract_files_flexible(content)
                for i, (file_path, lang, file_content) in enumerate(flexible_files):
                    print(f"文件 {i+1}: {file_path} ({lang})")
                    print(f"内容长度: {len(file_content)} 字符")
                    print("---")
                print(f"总共识别到 {len(flexible_files)} 个文件")
                
        except Exception as e:
            print(f"调试解析失败: {e}")

    def init_config(self):
        """初始化配置文件"""
        self.config_manager.init_config_file()

    def show_config(self):
        """显示当前配置"""
        self.config_manager.show_config()

    def debug_parse_detailed(self, markdown_file: str):
        """
        详细调试解析：显示解析过程中的每一步
        """
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("=== 详细解析调试 ===")
            print("原始内容行数: ", len(content.split('\n')))
            
            # 尝试标准解析
            print("\n--- 标准解析尝试 ---")
            standard_files = self.response_parser.extract_files_standard(content)
            print(f"标准解析找到 {len(standard_files)} 个文件")
            
            for i, (file_path, lang, file_content) in enumerate(standard_files):
                print(f"  文件 {i+1}: {file_path}")
                print(f"  语言: {lang}")
                print(f"  内容行数: {len(file_content.split())}")
                print("  内容预览: ")
                lines = file_content.split('\n')[:5]
                for line in lines:
                    print(f"    {line}")
                print()
            
            # 如果标准解析失败，尝试灵活解析
            if not standard_files:
                print("\n--- 灵活解析尝试 ---")
                flexible_files = self.response_parser.extract_files_flexible(content)
                print(f"灵活解析找到 {len(flexible_files)} 个文件")
                
                for i, (file_path, lang, file_content) in enumerate(flexible_files):
                    print(f"  文件 {i+1}: {file_path}")
                    print(f"  语言: {lang}")
                    print(f"  内容行数: {len(file_content.split())}")
                    print("  内容预览: ")
                    lines = file_content.split('\n')[:5]
                    for line in lines:
                        print(f"    {line}")
                    print()
            
            # 显示文件标题行
            print("\n--- 所有 ## 开头的行 ---")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('##'):
                    print(f"  行 {i+1}: {line.strip()}")
                    
        except Exception as e:
            print(f"调试解析失败: {e}")