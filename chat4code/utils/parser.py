#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参数解析工具
"""

import argparse


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="chat4code - 让代码与AI对话更简单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  导出项目: python -m chat4code export ./my_project project.md
  增量导出: python -m chat4code export ./my_project changes.md --incremental
  应用响应: python -m chat4code apply response.md ./updated_project
  交互模式: python -m chat4code --interactive
        """
    )

    parser.add_argument('action', nargs='?', choices=['export', 'apply', 'validate', 'session', 'debug-parse', 'config', 'help', 'feature'],
                        help=' 操作类型: export(导出代码), apply(应用响应), validate(验证格式), session(会话管理), debug-parse(调试解析), config(配置管理), help(帮助), feature(特性管理)')

    parser.add_argument('paths', nargs='*', help='路径参数') 

    parser.add_argument('--ext', nargs='*', help='文件扩展名 (如: .cpp .h .py)')
    parser.add_argument('--list-extensions', action='store_true', help='列出支持的文件扩展名')
    parser.add_argument('--list-tasks', action='store_true', help='列出可用任务模板')
    parser.add_argument('--task', help='指定任务类型 (如: analyze, bugfix, optimize)')
    parser.add_argument('--task-format', help='显示任务特定格式要求')
    parser.add_argument('--no-backup', action='store_true', help='不创建备份文件')
    parser.add_argument('--strict', action='store_true', help='使用严格格式解析')
    parser.add_argument('--verbose', action='store_true', help='详细输出(用于validate)')

    # 增量导出参数
    parser.add_argument('--incremental', action='store_true', help='增量导出')
    parser.add_argument('--since', dest='since_time', help='导出自指定时间以来的变更')

    # 差异显示参数
    parser.add_argument('--show-diff', action='store_true', help='显示应用前后的差异')

    # 任务提示参数
    parser.add_argument('--task-prompt', action='store_true', help='在导出文件中包含任务提示 (默认对 add_feature 和 explain 任务且提供 --task-content 时开启)')

    # 自定义任务内容参数
    parser.add_argument('--task-content', help='为任务提供具体要求内容（如add_feature, explain）')

    # 配置相关参数
    parser.add_argument('--config-init', action='store_true', help='初始化配置文件')
    parser.add_argument('--config-show', action='store_true', help='显示当前配置')

    # 交互模式参数
    parser.add_argument('--interactive', '-i', action='store_true', help='启动交互式模式')

    # 会话相关参数
    parser.add_argument('--session-task', dest='session_task', help='会话中的任务')
    parser.add_argument('--desc', '--description', dest='description', help='任务描述')

    return parser
