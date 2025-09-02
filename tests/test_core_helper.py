#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心助手类测试
"""

import pytest
from unittest.mock import patch, Mock


def test_helper_import():
    """测试助手类导入"""
    try:
        from chat4code.core.helper import CodeProjectAIHelper
        assert True
    except ImportError as e:
        pytest.fail(f"助手类导入失败: {e}")


@patch('chat4code.core.helper.ConfigManager')
@patch('chat4code.core.helper.TaskManager')
def test_helper_initialization(mock_task_manager, mock_config_manager):
    """测试助手类初始化"""
    from chat4code.core.helper import CodeProjectAIHelper
    
    # 创建助手实例
    helper = CodeProjectAIHelper()
    
    # 验证属性存在
    assert hasattr(helper, 'default_extensions')
    assert hasattr(helper, 'config_manager')
    assert hasattr(helper, 'task_manager')


def test_helper_has_required_methods():
    """测试助手类具有必需的方法"""
    from chat4code.core.helper import CodeProjectAIHelper
    
    # 检查类是否有关键方法（即使它们还没有实现）
    helper = CodeProjectAIHelper()
    
    # 这些方法应该存在（即使抛出异常）
    methods = [
        'export_to_markdown',
        'apply_markdown_response', 
        'validate_response_format',
        'list_supported_extensions'
    ]
    
    for method_name in methods:
        assert hasattr(helper, method_name), f"助手类缺少方法: {method_name}"


# 添加缺失的函数
def test_helper_import_function():
    """测试助手类导入函数"""
    try:
        from chat4code.core.helper import CodeProjectAIHelper
        assert CodeProjectAIHelper is not None
    except Exception as e:
        pytest.fail(f"助手类导入函数测试失败: {e}")


if __name__ == "__main__":
    test_helper_import()
    test_helper_initialization()
    test_helper_has_required_methods()
    test_helper_import_function()
    print("✅ 核心助手类测试通过！")
