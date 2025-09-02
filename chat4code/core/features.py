"""
chat4code 特性管理模块
负责存储、检索、更新和编辑特性（Features）信息。
实现任务描述中的功能：
1. 保存 add_feature 任务描述，允许查询/浏览和编号引用。
2. 实现完整的状态管理 (pending, exported, applied)。
3. 支持直接编辑数据库文件。
4. 将 feature 与导出文件、响应文件关联。
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any, Optional, List
import tempfile
import subprocess
import sys

FEATURES_FILENAME = "features.json" # 或者 "features.yaml"

class FeatureManager:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.metadata_dir = os.path.join(base_dir, ".chat4code") # 与配置元数据目录一致
        self.features_file = os.path.join(self.metadata_dir, FEATURES_FILENAME)
        self.features: Dict[str, Dict[str, Any]] = self._load_features()

    def _load_features(self) -> Dict[str, Dict[str, Any]]:
        """加载特性数据"""
        if not os.path.exists(self.features_file):
            return {}
        try:
            with open(self.features_file, 'r', encoding='utf-8') as f:
                # 简单支持 JSON 和 YAML
                if self.features_file.endswith(('.yml', '.yaml')):
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f) or {}
        except (json.JSONDecodeError, yaml.YAMLError, Exception) as e:
            print(f"⚠️  加载特性文件失败 {self.features_file}: {e}")
            return {}

    def _save_features(self):
        """保存特性数据"""
        try:
            if not os.path.exists(self.metadata_dir):
                os.makedirs(self.metadata_dir)
            
            with open(self.features_file, 'w', encoding='utf-8') as f:
                # 简单支持 JSON 和 YAML
                if self.features_file.endswith(('.yml', '.yaml')):
                    yaml.dump(self.features, f, indent=2, allow_unicode=True, sort_keys=False)
                else:
                    json.dump(self.features, f, indent=2, ensure_ascii=False, sort_keys=False)
        except Exception as e:
            print(f"❌ 保存特性文件失败 {self.features_file}: {e}")

    def add_feature(self, description: str, export_file: str) -> str:
        """
        添加一个新的特性
        Args:
            description: 特性描述
            export_file: 关联的导出文件名
        Returns:
            feature_id: 新生成的特性ID
        """
        # 生成唯一ID，这里简单使用时间戳+序号
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        counter = 1
        feature_id = f"F{timestamp}{counter:03d}"
        while feature_id in self.features:
            counter += 1
            feature_id = f"F{timestamp}{counter:03d}"

        feature_data = {
            "id": feature_id,
            "description": description,
            "status": "pending", # 初始状态为 pending
            "created_at": datetime.now().isoformat(),
            "exported_at": None,
            "applied_at": None,
            "export_file": export_file, # 关联导出文件
            "response_file": None,      # 关联响应文件 (初始为空)
        }
        self.features[feature_id] = feature_data
        self._save_features()
        print(f"✅ 特性已添加并编号为: {feature_id}")
        return feature_id

    def update_feature_status(self, feature_id: str, status: str, response_file: Optional[str] = None):
        """
        更新特性状态
        Args:
            feature_id: 特性ID
            status: 新状态 (exported, applied)
            response_file: 关联的响应文件名 (仅在 applied 时提供)
        """
        if feature_id not in self.features:
            print(f"⚠️  特性 {feature_id} 不存在")
            return

        valid_statuses = ["pending", "exported", "applied"]
        if status not in valid_statuses:
            print(f"⚠️  无效状态 '{status}'，有效状态为: {valid_statuses}")
            return

        self.features[feature_id]["status"] = status
        if status == "exported":
            self.features[feature_id]["exported_at"] = datetime.now().isoformat()
        elif status == "applied":
            self.features[feature_id]["applied_at"] = datetime.now().isoformat()
            if response_file:
                 self.features[feature_id]["response_file"] = response_file
        self._save_features()
        print(f"✅ 特性 {feature_id} 状态已更新为 '{status}'")

    def get_feature(self, feature_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取特性"""
        return self.features.get(feature_id)

    def list_features(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出所有特性，可选按状态过滤"""
        features_list = list(self.features.values())
        if status_filter:
            features_list = [f for f in features_list if f.get("status") == status_filter]
        return features_list

    def edit_features_file(self):
        """直接编辑特性数据库文件"""
        if not os.path.exists(self.features_file):
            # 如果文件不存在，先创建一个空的
            self._save_features()
            print(f"ℹ️  创建特性文件: {self.features_file}")

        editor = os.environ.get('EDITOR', 'nano') # 尝试获取环境变量 EDITOR，默认使用 nano
        if sys.platform.startswith('win'):
            editor = os.environ.get('EDITOR', 'notepad')

        try:
            # 使用 subprocess 调用编辑器
            subprocess.run([editor, self.features_file], check=True)
            print(f"✅ 特性文件编辑完成: {self.features_file}")
            # 重新加载编辑后的文件
            self.features = self._load_features()
        except subprocess.CalledProcessError as e:
            print(f"❌ 编辑器退出异常: {e}")
        except FileNotFoundError:
            print(f"❌ 未找到编辑器 '{editor}'，请检查环境变量 EDITOR 或系统PATH。")
        except Exception as e:
            print(f"❌ 编辑文件时发生错误: {e}")

    def find_feature_by_description(self, description: str) -> List[Dict[str, Any]]:
        """根据描述模糊查找特性"""
        results = []
        desc_lower = description.lower()
        for feature in self.features.values():
            if desc_lower in feature.get("description", "").lower():
                results.append(feature)
        return results

