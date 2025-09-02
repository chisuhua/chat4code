#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具模块测试
"""

import pytest


def test_utils_import():
    """测试工具模块导入"""
    try:
        from chat4code.utils.parser import create_parser
        assert True
    except ImportError as e:
        pytest.fail(f"工具模块导入失败: {e}")


def test_parser_function_exists():
    """测试解析器函数存在"""
    from chat4code.utils import create_parser
    assert callable(create_parser)


if __name__ == "__main__":
    test_utils_import()
    test_parser_function_exists()
    print("✅ 工具模块测试通过！")
