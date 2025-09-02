#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试动作处理器
"""


def process(args, helper):
    """处理调试解析动作"""
    if len(args.paths) < 1:
        print("❌ 错误: debug-parse操作需要指定Markdown文件")
        return

    markdown_file = args.paths[0]
    if '--detailed' in args.paths or '-d' in args.paths:
        helper.debug_parse_detailed(markdown_file)
    else:
        helper.debug_parse_response(markdown_file)
