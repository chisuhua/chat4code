#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数解析器测试
"""

import pytest
from chat4code.utils.parser import create_parser


def test_parser_creation():
    """测试解析器创建"""
    parser = create_parser()
    assert parser is not None
    assert hasattr(parser, 'parse_args')


def test_basic_action_parsing():
    """测试基本动作解析"""
    parser = create_parser()
    
    # 测试导出动作
    args = parser.parse_args(['export'])
    assert args.action == 'export'
    
    # 测试应用动作
    args = parser.parse_args(['apply'])
    assert args.action == 'apply'
    
    # 测试无动作（默认帮助）
    args = parser.parse_args([])
    assert args.action is None


def test_export_with_paths():
    """测试导出路径参数解析"""
    parser = create_parser()
    args = parser.parse_args(['export', './src', 'output.md'])
    assert args.action == 'export'
    assert args.paths == ['./src', 'output.md']


def test_apply_with_paths():
    """测试应用路径参数解析"""
    parser = create_parser()
    args = parser.parse_args(['apply', 'response.md', './project'])
    assert args.action == 'apply'
    assert args.paths == ['response.md', './project']


def test_interactive_mode_flag():
    """测试交互模式标志解析"""
    parser = create_parser()
    args = parser.parse_args(['--interactive'])
    assert args.interactive is True
    
    args = parser.parse_args(['-i'])
    assert args.interactive is True


def test_config_flags():
    """测试配置标志解析"""
    parser = create_parser()
    
    # 测试配置初始化
    args = parser.parse_args(['--config-init'])
    assert args.config_init is True
    
    # 测试配置显示
    args = parser.parse_args(['--config-show'])
    assert args.config_show is True


def test_list_flags():
    """测试列表标志解析"""
    parser = create_parser()
    
    # 测试列出任务
    args = parser.parse_args(['--list-tasks'])
    assert args.list_tasks is True
    
    # 测试列出扩展名
    args = parser.parse_args(['--list-extensions'])
    assert args.list_extensions is True


if __name__ == "__main__":
    test_parser_creation()
    test_basic_action_parsing()
    test_export_with_paths()
    test_apply_with_paths()
    test_interactive_mode_flag()
    test_config_flags()
    test_list_flags()
    print("✅ 参数解析器测试通过！")
