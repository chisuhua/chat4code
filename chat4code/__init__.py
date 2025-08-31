"""
chat4code - 让代码与AI对话更简单
"""

__version__ = "1.0.0"
__author__ = "Chi Suhua"

from .core import CodeProjectAIHelper
from .tasks import TaskManager
from .parser import ResponseParser
from .validator import ResponseValidator
from .session import SessionManager
# --- 新增导入 ---
from .features import FeatureManager
# --- 新增导入结束 ---

__all__ = [
    'CodeProjectAIHelper',
    'TaskManager',
    'ResponseParser',
    'ResponseValidator',
    'SessionManager',
    # --- 新增导出 ---
    'FeatureManager'
    # --- 新增导出结束 ---
]