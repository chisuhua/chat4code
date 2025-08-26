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
            "default_source_dir": ".",
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

    def get_default_source_dir(self) -> str:
        """获取默认源目录"""
        return self.config.get("default_source_dir", self.default_config["default_source_dir"])

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
            self._create_basic_prompts(prompts_file)

    def _create_basic_prompts(self, prompts_file: str):
        """创建基本的提示词文件"""
        basic_prompts = {
            "generic": {
                "analyze": {
                    "name": "代码分析",
                    "description": "分析项目结构和功能",
                    "prompt": "请分析这个项目的整体结构、主要功能模块和技术栈。",
                    "response_format": "分析报告格式",
                    "response_example": "## 项目分析报告\n\n### 项目概述\n- 项目名称: [项目名]\n- 主要技术栈: [技术列表]\n- 项目规模: [文件数量]\n\n### 功能模块\n1. **模块1**: [功能描述]\n2. **模块2**: [功能描述]"
                },
                "bugfix": {
                    "name": "Bug修复",
                    "description": "修复代码中的错误",
                    "prompt": "请检查代码中可能存在的bug，并提供修复方案。特别注意：内存泄漏、空指针、数组越界等问题。",
                    "response_format": "修复格式",
                    "response_example": "## src/main.cpp\n```cpp\n#include <iostream>\n#include <memory>\n\nint main() {\n    // 修复了内存泄漏问题\n    std::unique_ptr<int[]> arr(new int[100]);\n    \n    // 修复了数组越界检查\n    for(int i = 0; i < 100; i++) {\n        arr[i] = i;\n    }\n    \n    return 0;\n}\n```"
                },
                "optimize": {
                    "name": "性能优化",
                    "description": "优化代码性能",
                    "prompt": "请分析代码的性能瓶颈，并提供优化建议。请严格按照以下格式返回：\n\n## 文件路径1\n```cpp\n// 优化后的代码内容\n```\n\n## src/utils.cpp\n```cpp\n#include \"utils.h\"\n#include <sstream>\n#include <vector>\n\nnamespace Utils {\n    std::vector<std::string> splitString(const std::string& str, char delimiter) {\n        std::vector<std::string> result;\n        // 预估大小以减少重新分配\n        result.reserve(str.size() / 5 + 1);\n        \n        std::stringstream ss(str);\n        std::string item;\n        \n        while (std::getline(ss, item, delimiter)) {\n            result.push_back(item);\n        }\n        \n        return result;\n    }\n}\n```",
                    "response_format": "优化格式",
                    "response_example": "## src/sort.cpp\n```cpp\n#include <vector>\n#include <algorithm>\n\n// 优化前: O(n^2) 冒泡排序\n// 优化后: O(n log n) 快速排序\nvoid sortArray(std::vector<int>& arr) {\n    std::sort(arr.begin(), arr.end());\n}\n```"
                }
            },
            "cpp": {
                "analyze": {
                    "name": "C++代码分析",
                    "description": "分析C++项目结构和功能",
                    "prompt": "请分析这个C++项目的整体结构、主要功能模块、使用的C++标准版本、第三方库依赖等。特别关注：内存管理方式、设计模式应用、编译构建系统等。",
                    "response_format": "C++分析报告格式",
                    "response_example": "## C++项目分析报告\n\n### 项目概述\n- 项目名称: [项目名]\n- C++标准: C++17/C++20\n- 构建系统: CMake/Makefile\n- 第三方库: [库列表]\n\n### 核心模块\n1. **核心逻辑模块**: [功能描述]\n2. **网络通信模块**: [使用的技术]\n3. **数据存储模块**: [数据库/文件格式]"
                }
            },
            "python": {
                "analyze": {
                    "name": "Python代码分析",
                    "description": "分析Python项目结构和功能",
                    "prompt": "请分析这个Python项目的整体结构、主要功能模块、使用的Python版本、第三方库依赖、包管理方式等。特别关注：模块组织、虚拟环境使用、测试框架等。",
                    "response_format": "Python分析报告格式",
                    "response_example": "## Python项目分析报告\n\n### 项目概述\n- 项目名称: [项目名]\n- Python版本: 3.8+/3.9+\n- 包管理: pip/conda/poetry\n- 依赖管理: requirements.txt/pyproject.toml\n\n### 核心模块\n1. **核心逻辑模块**: [功能描述]\n2. **Web框架模块**: Flask/Django/FastAPI\n3. **数据处理模块**: pandas/numpy"
                }
            }
        }
        
        with open(prompts_file, 'w', encoding='utf-8') as f:
            yaml.dump(basic_prompts, f, allow_unicode=True, indent=2)
