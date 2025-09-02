#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帮助动作处理器
"""


def show_help(helper):
    """显示帮助信息"""
    instructions = [
        "=== chat4code 使用说明 ===",
        " ",
        "基本用法: ",
        "1. 导出项目代码为Markdown格式: ",
        "   python -m chat4code export ./my_project project.md",
        "   python -m chat4code export ./my_project project.md --task analyze",
        "   python -m chat4code export ./my_project  # 输出到控制台",
        "   python -m chat4code export ex* project.md  # 使用模式匹配导出",
        " ",
        "2. 增量导出: ",
        "   python -m chat4code export ./my_project changes.md --incremental",
        "   python -m chat4code export ./my_project changes.md --since 2024-01-01",
        " ",
        "3. 将AI生成的Markdown应用到本地: ",
        "   python -m chat4code apply response.md ./updated_project",
        "   python -m chat4code apply response.md ./updated_project --show-diff",
        " ",
        "4. 任务提示处理: ",
        "   python -m chat4code export ./my_project project.md --task analyze  # 任务提示显示在屏幕",
        "   python -m chat4code export ./my_project project.md --task add_feature  # add_feature任务提示默认包含在文件中 (如果提供 --task-content)",
        "   python -m chat4code export ./my_project project.md --task explain  # explain任务提示默认包含在文件中 (如果提供 --task-content)",
        "   python -m chat4code export ./my_project project.md --task add_feature --task-content \"添加用户登录功能\" # 指定具体功能",
        "   python -m chat4code export ./my_project project.md --task explain --task-content \"解释用户认证模块的工作原理\" # 指定解释内容",
        "   python -m chat4code export ./my_project project.md --task analyze --task-prompt  # 其他任务强制包含提示词在文件中",
        " ",
        "5. 自定义任务内容: ",
        "   python -m chat4code export ./my_project project.md --task add_feature --task-content \"添加用户登录功能\" ",
        "   python -m chat4code export ./my_project project.md --task explain --task-content \"解释用户认证模块的工作原理\" ",
        " ",
        "6. 配置管理: ",
        "   python -m chat4code --config-init  # 初始化配置文件",
        "   python -m chat4code --config-show   # 显示当前配置",
        " ",
        "7. 交互模式: ",
        "   python -m chat4code --interactive   # 启动交互式模式",
        " ",
        "8. 验证AI响应格式: ",
        "   python -m chat4code validate response.md",
        "   python -m chat4code validate response.md --verbose",
        " ",
        "9. 查看可用任务模板: ",
        "   python -m chat4code --list-tasks",
        " ",
        "10. 查看任务特定格式要求: ",
        "    python -m chat4code --task-format analyze",
        " ",
        "11. 会话管理: ",
        "    python -m chat4code session start my_session",
        "    python -m chat4code session log --task \"分析代码\" --desc \"分析项目结构\" my_session",
        "    python -m chat4code session history my_session",
        "    python -m chat4code session list",
        " ",
        "12. 特性管理: ",
        "    python -m chat4code feature list [--status <pending|exported|applied>] # 列出特性",
        "    python -m chat4code feature show <ID>                                  # 显示特性详情",
        "    python -m chat4code feature edit                                      # 编辑特性数据库",
        "    python -m chat4code feature find <关键词>                             # 根据描述查找特性",
        " ",
        "13. 调试解析: ",
        "    python -m chat4code debug-parse response.md",
        " ",
        "支持的文件类型: ",
        ", ".join(helper.list_supported_extensions()),
        " "
    ]
    print("\n".join(instructions))


def show_tasks(helper):
    """显示任务列表"""
    tasks = helper.task_manager.list_tasks()
    print("=== 可用任务模板 ===")
    print(" ")
    for key, task in tasks.items():
        print(f"{key}: {task['name']}")
        print(f"  描述: {task['description']}")
        print(" ")


def show_extensions(helper):
    """显示支持的扩展名"""
    print("支持的文件扩展名: ")
    for ext in helper.list_supported_extensions():
        print(f"  {ext}")


def show_task_format(helper, task_format):
    """显示任务格式要求"""
    print(helper.task_manager.show_task_format(task_format))
