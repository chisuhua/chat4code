"""
chat4code 任务管理模块 - 支持模板系统
"""

import json
import yaml
import os
import re
from typing import Dict, Any, Match, Optional
from string import Template

class TaskManager:
    def __init__(self, prompts_file: str = None):
        # 如果没有指定提示词文件，使用默认路径
        if prompts_file is None:
            # 尝试在当前目录或包目录查找提示词文件
            possible_paths = [
                "chat4code/prompts.yaml",
                "prompts.yaml",
                os.path.join(os.path.dirname(__file__), "prompts.yaml"),
                "chat4code/prompts.json",
                "prompts.json",
                os.path.join(os.path.dirname(__file__), "prompts.json")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    prompts_file = path
                    break
            else:
                # 如果找不到文件，尝试从包目录复制默认提示词
                package_prompts_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
                if os.path.exists(package_prompts_path):
                    # 复制到当前目录
                    import shutil
                    target_prompts_path = "prompts.yaml"
                    shutil.copy2(package_prompts_path, target_prompts_path)
                    prompts_file = target_prompts_path
                    print(f"✅ 从包目录复制默认提示词文件: {package_prompts_path}")
                else:
                    # 如果找不到文件，抛出异常
                    raise FileNotFoundError(
                        "找不到提示词文件！\n"
                        "chat4code需要外部提示词文件才能工作。\n"
                        "请确保以下文件之一存在：\n"
                        + "\n".join(f"  - {path}" for path in possible_paths[:3]) + "\n"
                        "或者在配置文件中指定 prompts_file 路径。"
                    )
        
        # 加载提示词
        if prompts_file and os.path.exists(prompts_file):
            try:
                if prompts_file.endswith('.yaml') or prompts_file.endswith('.yml'):
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        raw_prompts = yaml.safe_load(f)
                    print(f"✅ 已加载YAML提示词文件: {prompts_file}")
                else:
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        raw_prompts = json.load(f)
                    print(f"✅ 已加载JSON提示词文件: {prompts_file}")
                
                # 处理模板
                self.templates = raw_prompts.get('templates', {})
                self.prompts = self._process_templates(raw_prompts)
                   
            except Exception as e:
                raise Exception(f"加载提示词文件失败: {e}")
        else:
            raise FileNotFoundError(f"提示词文件不存在: {prompts_file}")

    def _process_templates(self, raw_prompts: Dict) -> Dict:
        """处理模板引用"""
        processed_prompts = {}
        
        # 复制非模板部分
        for key, value in raw_prompts.items():
            if key != 'templates':
                processed_prompts[key] = value
        
        # 处理模板替换
        self._expand_template_references(processed_prompts)
        
        return processed_prompts

    def _expand_template_references(self, prompts_dict: Dict):
        """展开模板引用"""
        for category, tasks in prompts_dict.items():
            if isinstance(tasks, dict):
                for task_name, task_info in tasks.items():
                    if isinstance(task_info, dict) and 'prompt' in task_info:
                        task_info['prompt'] = self._expand_template_in_text(
                            task_info['prompt'], task_info
                        )

    def _expand_template_in_text(self, text: str, context: Dict) -> str:
        """在文本中展开模板引用"""
        # 查找 {template_name:param=value,param2=value2} 格式的模板引用
        def replace_template(match: Match) -> str:
            template_ref = match.group(1)
            
            # 解析模板名称和参数
            if ':' in template_ref:
                template_name, params_str = template_ref.split(':', 1)
                # 解析参数
                params = {}
                for param in params_str.split(','):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        params[key.strip()] = value.strip()
            else:
                template_name = template_ref
                params = {}   
            
            # 查找模板
            if template_name in self.templates:
                template_content = self.templates[template_name].get('template', '')
                # 替换参数
                try:
                    # 使用字符串替换处理参数
                    result = template_content
                    for key, value in params.items():
                        result = result.replace(f'{{{key}}}', value)
                    # --- 核心修改点 ---
                    # 替换 [关联特性ID] 为 关联特性ID: {feature_id}
                    result = result.replace("[关联特性ID]", "关联特性ID: {feature_id}")
                    # --- 修改结束 ---
                    return result
                except Exception as e:
                    print(f"⚠️ 模板替换失败: {e}")
                    return match.group(0)
            else:
                return match.group(0)
        
        # 使用正则表达式查找并替换模板引用
        pattern = r'\{([^}]+)\}'
        return re.sub(pattern, replace_template, text)

    def get_task_info(self, task_key: str, project_type: str = "generic") -> dict:
        """获取指定任务的信息，支持项目类型特定的任务"""
        # 根据项目类型选择任务模板
        if project_type in self.prompts and task_key in self.prompts[project_type]:
            return self.prompts[project_type][task_key]
        elif "generic" in self.prompts and task_key in self.prompts["generic"]:
            return self.prompts["generic"][task_key]
        
        # 返回空字典如果找不到任务
        return {}

    def has_task(self, task_key: str, project_type: str = "generic") -> bool:
        """检查任务是否存在"""
        return (task_key in self.prompts.get(project_type, {}) or 
                task_key in self.prompts.get("generic", {}))

    def list_tasks(self, project_type: str = "generic") -> dict:
        """列出指定项目类型的任务"""
        tasks = {}
        # 先添加通用任务
        if "generic" in self.prompts:
            tasks.update(self.prompts["generic"])
        # 再添加特定于项目类型的任务
        if project_type in self.prompts and project_type != "generic":
            tasks.update(self.prompts[project_type])
        return tasks

    def show_task_format(self, task_key: str, project_type: str = "generic") -> str:
        """显示任务特定的提示信息"""
        task_info = self.get_task_info(task_key, project_type)
        if not task_info:
            return f"❌ 未知的任务类型: {task_key}"
        
        lines = [
            f"=== {task_info['name']} 任务提示 ===",
            "",
            "任务描述: ",
            f"  {task_info['description']}",
            "",
            "AI提示: ",
            f"  {task_info['prompt']}",
            ""
        ]
        return "\n".join(lines)

    def detect_project_type(self, file_extensions: set) -> str:
        """
        根据文件扩展名检测项目类型
        """
        cpp_extensions = {'.cpp', '.cc', '.cxx', '.c', '.h', '.hh', '.hpp'}
        python_extensions = {'.py'}
        js_extensions = {'.js', '.ts', '.jsx', '.tsx'}
        
        cpp_count = len(file_extensions & cpp_extensions)
        python_count = len(file_extensions & python_extensions)
        js_count = len(file_extensions & js_extensions)
        
        if cpp_count > python_count and cpp_count > js_count:
            return "cpp"
        elif python_count > cpp_count and python_count > js_count:
            return "python"
        elif js_count > cpp_count and js_count > python_count:
            return "javascript"
        else:
            return "generic"

    def reload_prompts(self, prompts_file: str = None):
        """重新加载提示词文件"""
        if prompts_file is None:
            # 重新初始化当前文件
            self.__init__(None)
        else:
            # 从指定文件加载
            try:
                if prompts_file.endswith('.yaml') or prompts_file.endswith('.yml'):
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        raw_prompts = yaml.safe_load(f)
                    print(f"✅ 已重新加载YAML提示词文件: {prompts_file}")
                else:
                    with open(prompts_file, 'r', encoding='utf-8') as f:
                        raw_prompts = json.load(f)
                    print(f"✅ 已重新加载JSON提示词文件: {prompts_file}")
                
                # 处理模板
                self.templates = raw_prompts.get('templates', {})
                self.prompts = self._process_templates(raw_prompts)
                   
            except Exception as e:
                print(f"❌ 重新加载提示词文件失败: {e}")

    def customize_task_prompt(self, task_key: str, project_type: str, custom_content: str) -> Optional[str]:
        """
        根据用户输入的具体内容定制任务提示
        专门为 add_feature 和 explain 任务设计，将 '[请在此处描述具体功能]' 替换为 custom_content
        
        Args:
            task_key: 任务键名 (如 'add_feature', 'explain')
            project_type: 项目类型 (如 'generic', 'python')
            custom_content: 用户提供的具体任务内容
            
        Returns:
            定制后的提示字符串，如果任务不存在则返回 None
        """
        # --- 修正点 1: 使用正确的占位符 '[请在此处描述具体功能]' ---
        PLACEHOLDER = '[请在此处描述具体功能]'
        task_info = self.get_task_info(task_key, project_type)
        if not task_info:
            return None
            
        original_prompt = task_info.get('prompt', '')
        # 替换占位符
        customized_prompt = original_prompt.replace(PLACEHOLDER, custom_content)
        return customized_prompt
