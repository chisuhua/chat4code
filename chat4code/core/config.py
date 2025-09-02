"""
chat4code 配置管理模块
"""

import json
import os
import yaml
from typing import Dict, Any, List, Optional

class ConfigManager:
    def __init__(self, config_file: str = ".chat4code.json"):
        self.config_file = config_file
        self.default_config = {
            "default_extensions": [".cpp", ".h", ".cc", ".hh"],
            "language_map": {
                ".cpp": "cpp", ".cc": "cpp", ".cxx": "cpp", ".c": "c",
                ".h": "cpp", ".hh": "cpp", ".hpp": "cpp",
                ".py": "python", ".java": "java", ".js": "javascript",
                ".ts": "typescript", ".html": "html", ".css": "css",
                ".sql": "sql", ".sh": "bash", ".bash": "bash",
                ".json": "json", ".xml": "xml", ".yaml": "yaml", ".yml": "yaml",
                ".go": "go", ".rs": "rust", ".swift": "swift"
            },
            "exclude_patterns": ["*.log", "*.tmp", "node_modules/", "*.backup*"],
            "backup_enabled": True,
            "metadata_dir": ".chat4code",
            "prompts_file": None,
            "project_type": None,
            "development_mode": "batch",
            # 新增的默认路径和文件名配置
            # 修改为支持多个源目录
            "default_source_dirs": ["."],
            "default_target_dir": "./updated_project",
            "export_filename_pattern": "req.md",
            "import_filename_pattern": "resp.md",
            "export_output_dir": "./exports",
            "import_output_dir": "./imports"
        }
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并默认配置和用户配置
                    config = self.default_config.copy()
                    config.update(user_config)
                    return config
            except Exception as e:
                print(f"⚠️  配置文件加载失败: {e}，使用默认配置")
                return self.default_config
        return self.default_config

    def save_config(self):
        """保存配置文件"""
        try:
            # 确保配置目录存在
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"❌ 配置保存失败: {e}")

    def get(self, key: str, default=None):
        """获取配置项"""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """设置配置项"""
        self.config[key] = value

    def get_extensions(self) -> tuple:
        """获取默认文件扩展名"""
        extensions = self.config.get("default_extensions", self.default_config["default_extensions"])
        return tuple(extensions)

    def get_language_map(self) -> Dict[str, str]:
        """获取语言映射"""
        return self.config.get("language_map", self.default_config["language_map"])

    def get_exclude_patterns(self) -> List[str]:
        """获取排除模式"""
        return self.config.get("exclude_patterns", self.default_config["exclude_patterns"])

    def is_backup_enabled(self) -> bool:
        """检查是否启用备份"""
        return self.config.get("backup_enabled", self.default_config["backup_enabled"])

    def get_metadata_dir(self) -> str:
        """获取元数据目录"""
        return self.config.get("metadata_dir", self.default_config["metadata_dir"])

    def get_project_type(self) -> Optional[str]:
        """获取强制指定的项目类型"""
        return self.config.get("project_type", self.default_config["project_type"])

    def get_development_mode(self) -> str:
        """获取开发模式"""
        return self.config.get("development_mode", self.default_config["development_mode"])

    # 修改获取默认源目录的方法，支持多个目录
    def get_default_source_dirs(self) -> List[str]:
        """获取默认源目录列表"""
        source_dirs = self.config.get("default_source_dirs", self.default_config["default_source_dirs"])
        # 确保返回的是列表格式
        if isinstance(source_dirs, str):
            return [source_dirs]
        return source_dirs

    def get_default_target_dir(self) -> str:
        """获取默认目标目录"""
        return self.config.get("default_target_dir", self.default_config["default_target_dir"])

    def get_export_filename_pattern(self) -> str:
        """获取导出文件名模式"""
        return self.config.get("export_filename_pattern", self.default_config["export_filename_pattern"])

    def get_import_filename_pattern(self) -> str:
        """获取导入文件名模式"""
        return self.config.get("import_filename_pattern", self.default_config["import_filename_pattern"])

    def get_export_output_dir(self) -> str:
        """获取导出文件输出目录"""
        return self.config.get("export_output_dir", self.default_config["export_output_dir"])

    def get_import_output_dir(self) -> str:
        """获取导入文件输出目录"""
        return self.config.get("import_output_dir", self.default_config["import_output_dir"])

    def init_config_file(self):
        """初始化配置文件和示例提示词文件"""
        if not os.path.exists(self.config_file):
            # 从包目录复制默认配置
            package_config_path = os.path.join(os.path.dirname(__file__), ".chat4code.json")
            if os.path.exists(package_config_path):
                import shutil
                shutil.copy2(package_config_path, self.config_file)
                print(f"✅ 从包目录复制默认配置: {package_config_path}")
            else:
                # 如果包目录下没有默认配置，使用内置默认配置
                self.save_config()
                print(f"✅ 初始化配置文件: {self.config_file}")
            print("   您可以编辑此文件来自定义默认设置")
        else:
            print(f"ℹ️  配置文件已存在: {self.config_file}")
        
        # 初始化示例提示词文件（使用包目录下的默认提示词）
        prompts_file = os.path.join(os.path.dirname(self.config_file), "prompts.yaml")
        if not os.path.exists(prompts_file):
            self._create_package_prompts(prompts_file)
            print(f"✅ 创建提示词文件: {prompts_file}")
            print("   您可以编辑此文件来自定义AI任务提示")
        else:
            print(f"ℹ️  提示词文件已存在: {prompts_file}")

        # 创建导出和导入目录
        export_dir = self.get_export_output_dir()
        import_dir = self.get_import_output_dir()
        
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
            print(f"✅ 创建导出目录: {export_dir}")
        
        if not os.path.exists(import_dir):
            os.makedirs(import_dir)
            print(f"✅ 创建导入目录: {import_dir}")

    def show_config(self):
        """显示当前配置"""
        print("=== 当前配置 ===")
        print(f"配置文件: {self.config_file}")
        print()
        for key, value in self.config.items():
            print(f"{key}: {value}")

    def _create_package_prompts(self, prompts_file: str):
        """从包目录创建提示词文件"""
        try:
            # 尝试从包目录获取默认提示词
            package_prompts_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
            
            if os.path.exists(package_prompts_path):
                # 复制包目录下的提示词文件
                import shutil
                shutil.copy2(package_prompts_path, prompts_file)
                print(f"✅ 从包目录复制提示词文件: {package_prompts_path}")
            else:
                # 如果包目录下没有提示词文件，创建基本的提示词
                self._create_basic_prompts(prompts_file)
                print("⚠️  包目录下未找到提示词文件，创建基本提示词")
                
        except Exception as e:
            print(f"⚠️  创建提示词文件时出错: {e}")
            # 创建基本的提示词作为后备
