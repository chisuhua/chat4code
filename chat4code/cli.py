#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat4code 命令行接口入口
"""

from .utils.parser import create_parser
from .core.helper import CodeProjectAIHelper
from .core.session import SessionManager
from .core.features import FeatureManager

from .actions import (
    export_action,
    apply_action,
    validate_action,
    session_action,
    feature_action,
    config_action,
    debug_action,
    help_action
)


def main():
    """主函数 - 命令行接口"""
    parser = create_parser()
    args = parser.parse_args()

    # 如果指定了交互模式，启动交互式界面 
    if args.interactive:
        from .interactive import interactive_mode
        interactive_mode()
        return

    # 初始化核心组件
    helper = CodeProjectAIHelper()
    session_manager = SessionManager()
    feature_manager = FeatureManager()

    # 处理各种动作
    if args.config_init:
        config_action.handle_init(helper)
        return

    if args.config_show:
        config_action.handle_show(helper)
        return

    if args.list_tasks:
        help_action.show_tasks(helper)
        return

    if args.list_extensions:
        help_action.show_extensions(helper)
        return

    if args.task_format:
        help_action.show_task_format(helper, args.task_format)
        return

    # 根据动作类型分发处理
    action_handlers = {
        'export': lambda: export_action.process(args, helper),
        'apply': lambda: apply_action.process(args, helper),
        'validate': lambda: validate_action.process(args, helper),
        'session': lambda: session_action.process(args, session_manager),
        'feature': lambda: feature_action.process(args, feature_manager),
        'config': lambda: config_action.process(args, helper),
        'debug-parse': lambda: debug_action.process(args, helper),
        'help': lambda: help_action.show_help(helper),
        None: lambda: help_action.show_help(helper)
    }

    handler = action_handlers.get(args.action)
    if handler:
        handler()
    else:
        print(f"❌ 未知的动作: {args.action}")


if __name__ == "__main__":
    main()
