#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置动作处理器
"""


def process(args, helper):
    """处理配置动作"""
    if len(args.paths) < 1:
        print("❌ 错误: config操作需要指定子命令")
        print("用法: python -m chat4code config init")
        print("     python -m chat4code config show")
        return

    sub_action = args.paths[0]
    if sub_action == 'init':
        handle_init(helper)
    elif sub_action == 'show':
        handle_show(helper)
    else:
        print(f"❌ 未知的config子命令: {sub_action}")


def handle_init(helper):
    """处理初始化配置"""
    helper.init_config()


def handle_show(helper):
    """处理显示配置"""
    helper.show_config()
