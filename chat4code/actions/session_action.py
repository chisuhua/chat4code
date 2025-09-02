#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话动作处理器
"""


def process(args, session_manager):
    """处理会话动作"""
    if len(args.paths) < 1:
        _show_session_usage()
        return

    sub_action = args.paths[0]
    action_handlers = {
        'start': lambda: _handle_start(args, session_manager),
        'log': lambda: _handle_log(args, session_manager),
        'history': lambda: _handle_history(args, session_manager),
        'list': lambda: _handle_list(session_manager)
    }

    handler = action_handlers.get(sub_action)
    if handler:
        handler()
    else:
        print(f"❌ 未知的session子命令: {sub_action}")


def _show_session_usage():
    """显示会话用法"""
    print("❌ 错误: session操作需要指定子命令")
    print("用法: python -m chat4code session start <会话名>")
    print("     python -m chat4code session log --task <任务> [--desc <描述>] <会话名>")
    print("     python -m chat4code session history <会话名>")
    print("     python -m chat4code session list")


def _handle_start(args, session_manager):
    """处理开始会话"""
    if len(args.paths) < 2:
        print("❌ 错误: 需要指定会话名称")
        return
    session_name = args.paths[1]
    print(session_manager.start_session(session_name))


def _handle_log(args, session_manager):
    """处理日志记录"""
    if not args.session_task:
        print("❌ 错误: 需要指定 --task 参数")
        return
    if len(args.paths) < 2:
        print("❌ 错误: 需要指定会话名称")
        return
    session_name = args.paths[1]
    print(session_manager.log_task(session_name, args.session_task, args.description or " "))


def _handle_history(args, session_manager):
    """处理历史记录"""
    if len(args.paths) < 2:
        print("❌ 错误: 需要指定会话名称")
        return
    session_name = args.paths[1]
    print(session_manager.show_session_history(session_name))


def _handle_list(session_manager):
    """处理列表显示"""
    print(session_manager.list_sessions())
