#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话管理器测试
"""

import pytest
from unittest.mock import patch, mock_open
import json


def test_session_manager_import():
    """测试会话管理器导入"""
    try:
        from chat4code.core.session import SessionManager
        assert True
    except ImportError as e:
        pytest.fail(f"会话管理器导入失败: {e}")


@patch('os.path.exists', return_value=False)
@patch('os.makedirs')
def test_session_manager_initialization(mock_makedirs, mock_exists):
    """测试会话管理器初始化"""
    from chat4code.core.session import SessionManager
    
    manager = SessionManager()
    assert manager is not None


@patch('os.path.exists', return_value=True)
@patch('builtins.open', mock_open(read_data='{"sessions": {}}'))
def test_session_manager_with_existing_data(mock_exists):
    """测试会话管理器加载现有数据"""
    from chat4code.core.session import SessionManager
    
    manager = SessionManager()
    assert manager is not None


def test_session_manager_has_required_methods():
    """测试会话管理器具有必需的方法"""
    from chat4code.core.session import SessionManager
    
    manager = SessionManager()
    
    # 检查必需的方法
    methods = [
        'start_session',
        'log_task',
        'show_session_history',
        'list_sessions'
    ]
    
    for method_name in methods:
        assert hasattr(manager, method_name), f"会话管理器缺少方法: {method_name}"


# 添加缺失的函数
def test_session_manager_import_function():
    """测试会话管理器导入函数"""
    try:
        from chat4code.core.session import SessionManager
        assert SessionManager is not None
    except Exception as e:
        pytest.fail(f"会话管理器导入函数测试失败: {e}")


if __name__ == "__main__":
    test_session_manager_import()
    test_session_manager_initialization()
    test_session_manager_with_existing_data()
    test_session_manager_has_required_methods()
    test_session_manager_import_function()
    print("✅ 会话管理器测试通过！")
