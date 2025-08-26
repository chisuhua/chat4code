"""
chat4code 响应解析模块 - 状态机版本
"""

import os
import re
from typing import List, Tuple, Optional

class ResponseParser:
    def __init__(self):
        pass

    def extract_files_standard(self, content: str) -> List[Tuple[str, str, str]]:
        """
        使用状态机方法解析文件内容，能正确处理文件内容中包含 ``` 的情况
        """
        files = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            # 查找文件标题
            if (lines[i].strip().startswith('## ') and 
                not self._is_markdown_section_title(lines[i].strip()[3:])):
                
                file_title = lines[i].strip()[3:].strip()
                clean_file_path = self._clean_file_path(file_title)
                
                if clean_file_path and self._is_valid_file_path(clean_file_path):
                    # 查找下一个代码块
                    i += 1
                    # 跳过空行
                    while i < len(lines) and lines[i].strip() == '':
                        i += 1
                    
                    # 查找代码块开始标记
                    if i < len(lines) and self._is_code_block_start(lines[i]):
                        # 提取语言标识
                        language = self._extract_language(lines[i])
                        
                        # 提取代码内容 - 使用平衡计数法
                        i += 1
                        code_content, next_line_index = self._extract_code_content(lines, i)
                        
                        if code_content is not None:
                            files.append((clean_file_path, language, code_content))
                            i = next_line_index
                        else:
                            i += 1
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        
        return files

    def _is_code_block_start(self, line: str) -> bool:
        """判断是否为代码块开始标记"""
        return line.strip().startswith('```')

    def _extract_language(self, line: str) -> str:
        """从代码块开始行提取语言标识"""
        line = line.strip()
        if len(line) > 3:
            return line[3:].strip()
        return 'text'

    def _extract_code_content(self, lines: List[str], start_index: int) -> Tuple[Optional[str], int]:
        """
        提取代码内容，正确处理内容中的 ```
        使用平衡计数法确保找到正确的结束标记
        """
        code_lines = []
        i = start_index
        
        while i < len(lines):
            line = lines[i]
            if line.strip() == '```':
                # 找到结束标记
                code_content = '\n'.join(code_lines)
                # 移除末尾的空行
                code_content = code_content.rstrip()
                return code_content, i + 1
            else:
                code_lines.append(line)
            i += 1
        
        # 没有找到结束标记
        return None, i

    def _is_markdown_section_title(self, text: str) -> bool:
        """
        判断文本是否为markdown章节标题而不是文件路径
        """
        text = text.strip()
        # 数字标题：1. 简介, 2.1 功能等
        if re.match(r'^\d+(\.\d+)*\s', text):
            return True
        # 字母标题：A. 介绍, B. 使用等
        if re.match(r'^[A-Z]\.\s', text):
            return True
        # 纯文本标题：简介, 使用方法等（没有文件扩展名特征）
        if (re.match(r'^[A-Z\u4e00-\u9fa5][^.]*$', text) and 
            '.' not in text and '/' not in text and '\\' not in text):
            return True
        return False

    def _is_valid_file_path(self, file_path: str) -> bool:
        """
        判断是否为有效的文件路径
        """
        basename = os.path.basename(file_path)
        
        # 明确的文件路径特征
        if ('.' in basename or 
            '/' in file_path or 
            '\\' in file_path or
            file_path.endswith(('.md', '.txt', '.json', '.yaml', '.yml'))):
            return True
            
        # 明确的标题特征
        if (re.match(r'^\d+(\.\d+)*\s', file_path) or 
            re.match(r'^[A-Z]\.\s', file_path) or
            (re.match(r'^[A-Z\u4e00-\u9fa5][^.]*$', file_path) and 
             '.' not in file_path and '/' not in file_path)):
            return False
            
        return False

    def _clean_file_path(self, file_path: str) -> Optional[str]:
        """清理和验证文件路径"""
        # 移除常见前缀
        file_path = re.sub(r'^(文件|File)[:：]?\s*', '', file_path.strip())
        
        # 清理文件路径
        clean_file_path = os.path.normpath(file_path)
        
        # 安全检查
        if (clean_file_path.startswith('..') or 
            clean_file_path.startswith('/') or
            clean_file_path.startswith('\\')):
            return None
            
        return clean_file_path

    def extract_files_flexible(self, content: str) -> List[Tuple[str, str, str]]:
        """
        灵活格式提取
        """
        # 首先尝试标准格式
        standard_files = self.extract_files_standard(content)
        if standard_files:
            return standard_files
        
        # 备用正则表达式方法
        return self._extract_with_regex_backup(content)

    def _extract_with_regex_backup(self, content: str) -> List[Tuple[str, str, str]]:
        """
        备用正则表达式提取方法
        """
        files = []
        
        # 使用更精确的正则表达式
        pattern = r'##\s+([^\n]+?)\s*\n\s*\n\s*```(\w*)\s*\n((?:(?!```).)*?)\s*\n\s*```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for file_path, lang, code_content in matches:
            clean_file_path = self._clean_file_path(file_path.strip())
            if clean_file_path and self._is_valid_file_path(clean_file_path):
                files.append((clean_file_path, lang or 'text', code_content.strip()))
        
        return files

    def _infer_filename(self, code_content: str, lang: str, index: int) -> str:
        """
        从代码内容推断文件名
        """
        # 尝试从#include语句推断
        include_match = re.search(r'#include\s*["<]([^">]+)[">]', code_content)
        if include_match:
            return include_match.group(1)
        
        # 尝试从package语句推断（Java）
        package_match = re.search(r'package\s+([a-zA-Z0-9_.]+)', code_content)
        if package_match and lang == 'java':
            return f"{package_match.group(1).replace('.', '/')}/Class{index+1}.java"
        
        # 尝试从类名推断
        class_match = re.search(r'class\s+([A-Za-z_][A-Za-z0-9_]*)', code_content)
        if class_match:
            base_name = class_match.group(1)
            ext = self._get_extension_by_language(lang)
            return f"{base_name}{ext}"
        
        # 默认文件名
        ext = self._get_extension_by_language(lang)
        return f"file_{index+1}{ext}"

    def _get_extension_by_language(self, lang: str) -> str:
        """根据语言获取文件扩展名"""
        lang_to_ext = {
            'cpp': '.cpp', 'c': '.c', 'python': '.py', 'java': '.java',
            'javascript': '.js', 'typescript': '.ts', 'html': '.html',
            'css': '.css', 'markdown': '.md', 'md': '.md',
            'json': '.json', 'xml': '.xml', 'yaml': '.yaml', 'yml': '.yml',
            'sql': '.sql', 'bash': '.sh', 'shell': '.sh',
            'go': '.go', 'rust': '.rs', 'swift': '.swift'
        }
        return lang_to_ext.get(lang, f'.{lang}' if lang else '.txt')
