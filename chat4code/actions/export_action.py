#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出动作处理器
"""

import os


def process(args, helper):
    """处理导出动作"""
    if len(args.paths) < 1:
        _show_export_usage()
        return

    # 解析路径参数
    src_dirs, output_file = _parse_paths(args.paths)

    # 获取文件扩展名
    extensions = tuple(args.ext) if args.ext else helper.default_extensions

    # 处理 add_feature 和 explain 任务的用户输入
    task_content = _handle_task_content_input(args.task, args.task_content)

    # 设置任务提示包含逻辑
    include_task_prompt = _should_include_task_prompt(args, task_content)

    try:
        # 执行导出
        helper.export_to_markdown(
            src_dirs, output_file, extensions, args.task,
            args.incremental, args.since_time,
            include_task_prompt, task_content
        )
    except Exception as e:
        print(f"❌ 导出失败: {e}")


def _show_export_usage():
    """显示导出用法"""
    print("❌ 错误: export操作需要指定源目录")
    print("用法: python -m chat4code export <源目录> [输出文件]")
    print("示例: python -m chat4code export dir1 dir2 output.md")
    print("示例: python -m chat4code export ex* output.md")


def _parse_paths(paths):
    """解析路径参数"""
    if len(paths) > 1 and (paths[-1].endswith(('.md', '.txt', '.markdown')) or '.' in os.path.splitext(paths[-1])[1]):
        src_dirs = paths[:-1]
        output_file = paths[-1]
    else:
        src_dirs = paths
        output_file = None
    return src_dirs, output_file


def _handle_task_content_input(task, task_content):
    """处理任务内容输入"""
    if task in ["add_feature", "explain"] and not task_content:
        prompt_msg = "请输入具体功能需求: " if task == "add_feature" else "请输入需要解释的内容: "
        task_content = input(prompt_msg).strip()
        if not task_content:
            print("⚠️ 未提供具体内容，将使用默认提示词。")
    return task_content


def _should_include_task_prompt(args, task_content):
    """判断是否应该包含任务提示"""
    include_task_prompt = args.task_prompt
    if args.task in ["add_feature", "explain"] and (task_content or include_task_prompt):
        include_task_prompt = True
    return include_task_prompt
