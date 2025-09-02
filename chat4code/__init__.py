"""
chat4code - 让代码与AI对话更简单
"""

__version__ = "1.0.0"
__author__ = "Chi Suhua"

from .core.helper import CodeProjectAIHelper
from .core.tasks import TaskManager
from .core.parser import ResponseParser
from .core.validator import ResponseValidator
from .core.session import SessionManager
from .core.features import FeatureManager

from .cli import main

__all__ = [
    'CodeProjectAIHelper',
    'TaskManager',
    'ResponseParser',
    'ResponseValidator',
    'SessionManager',
    'FeatureManager'
    'main'
]
