#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特性管理器测试
"""

import pytest
from unittest.mock import patch, mock_open
import json


def test_feature_manager_import():
    """测试特性管理器导入"""
    try:
        from chat4code.core.features import FeatureManager
        assert True
    except ImportError as e:
        pytest.fail(f"特性管理器导入失败: {e}")


@patch('os.path.exists', return_value=False)
@patch('os.makedirs')
def test_feature_manager_initialization(mock_makedirs, mock_exists):
    """测试特性管理器初始化"""
    from chat4code.core.features import FeatureManager
    
    manager = FeatureManager()
    assert manager is not None


@patch('os.path.exists', return_value=True)
@patch('builtins.open', mock_open(read_data='{"features": []}'))
def test_feature_manager_with_existing_data(mock_exists):
    """测试特性管理器加载现有数据"""
    from chat4code.core.features import FeatureManager
    
    manager = FeatureManager()
    assert manager is not None


def test_feature_manager_has_required_methods():
    """测试特性管理器具有必需的方法"""
    from chat4code.core.features import FeatureManager
    
    manager = FeatureManager()
    
    # 检查必需的方法
    methods = [
        'list_features',
        'get_feature',
        'edit_features_file',
        'find_feature_by_description'
    ]
    
    for method_name in methods:
        assert hasattr(manager, method_name), f"特性管理器缺少方法: {method_name}"


# 添加缺失的函数
def test_feature_manager_import_function():
    """测试特性管理器导入函数"""
    try:
        from chat4code.core.features import FeatureManager
        assert FeatureManager is not None
    except Exception as e:
        pytest.fail(f"特性管理器导入函数测试失败: {e}")


if __name__ == "__main__":
    test_feature_manager_import()
    test_feature_manager_initialization()
    test_feature_manager_with_existing_data()
    test_feature_manager_has_required_methods()
    test_feature_manager_import_function()
    print("✅ 特性管理器测试通过！")
