#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用动作处理器
"""


def process(args, helper):
    """处理应用动作"""
    if len(args.paths) < 2:
        _show_apply_usage()
        return

    markdown_file = args.paths[0]
    dst_dir = args.paths[1]

    try:
        # 应用到本地，使用灵活解析模式
        result = helper.apply_markdown_response(
            markdown_file, dst_dir,
            not args.no_backup if args.no_backup else None,
            not args.strict,
            args.show_diff
        )
    except Exception as e:
        print(f"❌ 应用失败: {e}")


def _show_apply_usage():
    """显示应用用法"""
    print("❌ 错误: apply操作需要指定Markdown文件和目标目录")
    print("用法: python -m chat4code apply <Markdown文件> <目标目录>")
