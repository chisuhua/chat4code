"""
chat4code 会话管理模块
"""

import os
import json
from datetime import datetime
from typing import Dict, List

class SessionManager:
    def __init__(self, session_dir: str = ".chat4code_sessions"):
        self.session_dir = session_dir
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

    def start_session(self, session_name: str) -> str:
        """开始新的开发会话"""
        session_file = os.path.join(self.session_dir, f"{session_name}.json")
        
        session_data = {
            "name": session_name,
            "created": datetime.now().isoformat(),
            "tasks": []
        }
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return f"✅ 会话 '{session_name}' 已创建"

    def log_task(self, session_name: str, task: str, description: str = "") -> str:
        """记录任务到会话"""
        session_file = os.path.join(self.session_dir, f"{session_name}.json")
        
        if not os.path.exists(session_file):
            return f"❌ 会话 '{session_name}' 不存在"
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        task_entry = {
            "id": len(session_data["tasks"]) + 1,
            "task": task,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        session_data["tasks"].append(task_entry)
        
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        return f"✅ 任务已记录到会话 '{session_name}'"

    def show_session_history(self, session_name: str) -> str:
        """显示会话历史"""
        session_file = os.path.join(self.session_dir, f"{session_name}.json")
        
        if not os.path.exists(session_file):
            return f"❌ 会话 '{session_name}' 不存在"
        
        with open(session_file, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        lines = [f"=== 会话 '{session_name}' 历史 ===", ""]
        lines.append(f"创建时间: {session_data['created']}")
        lines.append("")
        lines.append("任务记录:")
        lines.append("---------")
        
        for task in session_data["tasks"]:
            lines.append(f"#{task['id']} {task['task']}")
            if task['description']:
                lines.append(f"  描述: {task['description']}")
            lines.append(f"  时间: {task['timestamp']}")
            lines.append("")
        
        return "\n".join(lines)

    def list_sessions(self) -> str:
        """列出所有会话"""
        if not os.path.exists(self.session_dir):
            return "没有找到会话"
        
        sessions = []
        for file in os.listdir(self.session_dir):
            if file.endswith('.json'):
                sessions.append(file[:-5])  # 移除 .json 扩展名
        
        if not sessions:
            return "没有找到会话"
        
        lines = ["=== 会话列表 ===", ""]
        for session in sessions:
            lines.append(f"- {session}")
        return "\n".join(lines)

