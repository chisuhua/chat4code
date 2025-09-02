#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最基本的测试用例 - 验证核心功能
"""

import pytest
from unittest.mock import patch, Mock


def test_import_modules():
    """测试基本模块导入"""
    # 测试核心模块导入
    try:
        from chat4code import CodeProjectAIHelper, SessionManager, FeatureManager
        assert True
    except ImportError as e:
        pytest.fail(f"模块导入失败: {e}")

    # 测试CLI模块导入
    try:
        from chat4code.cli import main
        assert True
    except ImportError as e:
        pytest.fail(f"CLI模块导入失败: {e}")

    # 测试交互模式导入
    try:
        from chat4code.interactive import interactive_mode
        assert True
    except ImportError as e:
        pytest.fail(f"交互模式模块导入失败: {e}")


def test_helper_initialization():
    """测试助手类初始化"""
    with patch('chat4code.core.helper.ConfigManager'), \
         patch('chat4code.core.helper.TaskManager'):
        from chat4code.core.helper import CodeProjectAIHelper
        try:
            helper = CodeProjectAIHelper()
            assert helper is not None
        except Exception as e:
            pytest.fail(f"助手类初始化失败: {e}")


def test_session_manager_initialization():
    """测试会话管理器初始化"""
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs'):
        from chat4code.core.session import SessionManager
        try:
            manager = SessionManager()
            assert manager is not None
        except Exception as e:
            pytest.fail(f"会话管理器初始化失败: {e}")


def test_feature_manager_initialization():
    """测试特性管理器初始化"""
    with patch('os.path.exists', return_value=False), \
         patch('os.makedirs'):
        from chat4code.core.features import FeatureManager
        try:
            manager = FeatureManager()
            assert manager is not None
        except Exception as e:
            pytest.fail(f"特性管理器初始化失败: {e}")


def test_parser_creation():
    """测试参数解析器创建"""
    try:
        from chat4code.utils.parser import create_parser
        parser = create_parser()
        assert parser is not None
    except Exception as e:
        pytest.fail(f"参数解析器创建失败: {e}")


def test_package_main_function():
    """测试包主函数"""
    try:
        from chat4code import main
        # main可能是一个函数或CLI入口，我们只检查它是否存在
        assert main is not None
    except ImportError as e:
        # 如果导入失败，我们检查CLI模块
        try:
            from chat4code.cli import main as cli_main
            assert cli_main is not None
        except ImportError as e2:
            pytest.fail(f"主函数导入失败: {e}")

if __name__ == "__main__":
    # 运行基本测试
    test_import_modules()
    test_helper_initialization()
    test_session_manager_initialization()
    test_feature_manager_initialization()
    test_parser_creation()
    test_package_main_function()
    print("✅ 所有基本测试通过！")
