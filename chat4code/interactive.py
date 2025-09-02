#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat4code 交互模式模块
"""

from .core.helper import CodeProjectAIHelper
from .core.session import SessionManager
import os


def interactive_mode():
    """交互式模式"""
    print("=== chat4code 交互式模式 ===")
    print("输入 'help' 查看可用命令，输入 'quit' 或 'exit' 退出")
    print()

    # 初始化助手和会话管理器
    helper = CodeProjectAIHelper()
    session_manager = SessionManager()

    while True:
        try:
            command = input("chat4code > ").strip()

            if not command:
                continue

            if command.lower() in ['quit', 'exit']:
                print("\n👋 再见！")
                break

            if command.lower() == 'help':
                _show_interactive_help()
                continue

            # 解析命令
            parts = command.split()
            action = parts[0].lower()

            # 处理各种交互命令
            _handle_interactive_command(action, parts[1:], helper, session_manager)

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def _show_interactive_help():
    """显示交互式模式帮助"""
    help_text = """
可用命令:
  export [目录1] [目录2] ... [文件] [--task 任务] [--task-content 内容] [--incremental] [--task-prompt]  导出项目代码
  apply [文件] [目录] [--show-diff] [--no-backup]                     应用AI 响应
  validate [文件]                                                      验证响应格式
  session start|log|history|list [参数]                               会话管理
  config init|show                                                         配置管理
  tasks                                                               显示可用任务
  extensions                                                              显示支持的扩展名
  feature list|show|edit|find [参数]                                  特性管理
  help                                                                  显示此帮助
  quit/exit                                                           退出程序
"""
    print(help_text)


def _handle_interactive_command(action, args, helper, session_manager):
    """处理交互命令"""
    handlers = {
        'export': lambda: _interactive_export(helper, args),
        'apply': lambda: _interactive_apply(helper, args),
        'validate': lambda: _interactive_validate(helper, args),
        'session': lambda: _interactive_session(session_manager, args),
        'config': lambda: _interactive_config(helper, args),
        'tasks': lambda: _show_tasks(helper),
        'extensions': lambda: _show_extensions(helper),
        'feature': lambda: _interactive_feature(helper.feature_manager, args)
    }
    
    handler = handlers.get(action)
    if handler:
        handler()
    else:
        print(f"❌ 未知命令: {action}")
        print("输入 'help' 查看可用命令")


def _interactive_export(helper, args):
    """交互式导出"""
    # 解析参数
    src_dirs = []
    output_file = None
    task = None
    task_content = None
    incremental = False
    include_task_prompt = False  # 默认不包含任务提示在文件中

    # 解析命令行参数
    i = 0
    while i < len(args):
        if args[i] == '--task' and i + 1 < len(args):
            task = args[i + 1]
            i += 2
        elif args[i] == '--task-content' and i + 1 < len(args):
            task_content = args[i + 1]
            i += 2
        elif args[i] == '--incremental':
            incremental = True
            i += 1
        elif args[i] == '--task-prompt':
            include_task_prompt = True
            i += 1
        elif args[i].startswith('--'):
            # 跳过其他标志
            i += 1
        else:
            # 收集源目录，最后一个（如果是文件）作为输出文件
            src_dirs.append(args[i])
            i += 1

    # 如果没有指定源目录，使用配置默认值或询问用户
    if not src_dirs:
        default_srcs = helper.config_manager.get_default_source_dirs()
        use_default = input(f"使用默认源目录 '{', '.join(default_srcs)}'? (Y/n): ").strip().lower()
        if use_default != 'n':
            src_dirs = default_srcs
        else:
            src_input = input("请输入源目录路径（多个目录用空格分隔）: ").strip()
            if src_input:
                src_dirs = src_input.split()
            else:
                src_dirs = ["."]

    # 确定输出文件（最后一个参数如果是文件名）
    if src_dirs and ('.' in os.path.splitext(src_dirs[-1])[1] or src_dirs[-1].endswith(('.md', '.txt', '.markdown'))):
        output_file = src_dirs.pop()

    # 如果没有指定任务，直接进入任务选择流程
    if not task:
        # 直接显示可用任务并让用户选择
        tasks = list(helper.task_manager.list_tasks().keys())
        if tasks:
            print("可用任务: ")
            for i, t in enumerate(tasks, 1):
                print(f"  {i}. {t}")
            try:
                choice_input = input("请选择任务 (输入数字，或直接回车跳过): ").strip()
                if choice_input:  # 只有在用户输入了内容时才尝试解析
                    choice = int(choice_input) - 1
                    if 0 <= choice < len(tasks):
                        task = tasks[choice]
                    else:
                        print("无效选择，跳过任务指定")
            except ValueError:  # 捕获非数字输入
                print("无效输入，跳过任务指定")
        else:
            print("当前没有可用的任务模板。")

    # 在交互模式中也处理 add_feature 和 explain 的用户输入
    # 如果是 add_feature 或 explain 任务且没有指定具体内容，询问用户输入
    if task in ["add_feature", "explain"] and not task_content:
        prompt_msg = "请输入具体功能需求: " if task == "add_feature" else "请输入需要解释的内容: "
        task_content = input(prompt_msg).strip()
        # 在交互模式中，用户输入了内容后，也应默认包含提示词
        if task_content:
            include_task_prompt = True  # 确保包含

    # 如果没有指定输出文件，根据任务自动生成文件名
    if not output_file:
        export_dir = helper.config_manager.get_export_output_dir()
        if task:
            # 使用任务名作为文件名基础，并自动生成序号
            export_pattern = f"{task}_.md"
        else:
            # 如果没有任务，使用配置中的默认模式
            export_pattern = helper.config_manager.get_export_filename_pattern()

        try:
            auto_filename = helper.get_next_sequential_filename(export_pattern, export_dir)
            print(f"自动生成的输出文件名: {auto_filename}")
            output_file = auto_filename
        except Exception as e:
            print(f"⚠️ 生成自动文件名时出错: {e}，使用默认名称")
            output_file = "export_output.md"

    # 调整交互模式中的提示逻辑
    # 对于 add_feature 和 explain 任务，如果用户已经输入了内容，则默认包含提示词，不再询问。
    # 对于其他任务，或者用户未输入内容的情况，保留原有询问逻辑。
    if task and output_file:
        # 如果是 add_feature 或 explain 且有内容，跳过询问
        if task in ["add_feature", "explain"] and task_content:
            pass  # 已在上面设置 include_task_prompt = True
        else:
            # 对于其他情况，询问用户
            include_prompt = input("是否在导出文件中包含任务提示? (Y/n): ").strip().lower()
            if include_prompt != 'n':
                include_task_prompt = True

    try:
        # 传递 custom_task_content 参数
        result_file = helper.export_to_markdown(
            src_dirs, output_file, task=task,
            incremental=incremental,
            include_task_prompt=include_task_prompt,
            custom_task_content=task_content  # 注意：交互模式中传递的是 task_content
        )
        print("✅ 导出完成! ")
        print(f"   导出文件: {result_file}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")


def _interactive_apply(helper, args):
    """交互式应用"""
    # 解析参数
    markdown_file = None
    dst_dir = None
    show_diff = '--show-diff' in args
    no_backup = '--no-backup' in args

    # 获取非标志参数
    non_flag_args = [arg for arg in args if not arg.startswith('--')]
    if len(non_flag_args) >= 1:
        markdown_file = non_flag_args[0]
    if len(non_flag_args) >= 2:
        dst_dir = non_flag_args[1]

    # 如果没有指定导入文件，询问用户是否使用自动序列化文件名
    if markdown_file is None:
        import_pattern = helper.config_manager.get_import_filename_pattern()
        import_dir = helper.config_manager.get_import_output_dir()
        auto_filename = helper.get_next_sequential_filename(import_pattern, import_dir)

        use_auto = input(f"使用自动序列化导入文件 '{auto_filename}'? (Y/n): ").strip().lower()
        if use_auto != 'n':
            markdown_file = auto_filename
        else:
            markdown_file = input("请输入Markdown文件路径: ").strip()
            if not markdown_file:
                print("❌ 必须指定Markdown文件")
                return

    # 如果没有指定目标目录，使用配置默认值或询问用户
    if dst_dir is None:
        default_dst = helper.config_manager.get_default_target_dir()
        use_default = input(f"使用默认目标目录 '{default_dst}'? (Y/n): ").strip().lower()
        if use_default != 'n':
            dst_dir = default_dst
        else:
            dst_dir = input("请输入目标目录路径: ").strip()
            if not dst_dir:
                print("❌ 必须指定目标目录")
                return

    try:
        # 应用响应
        result = helper.apply_markdown_response(
            markdown_file, dst_dir,
            create_backup=not no_backup,
            show_diff=show_diff
        )
        print("✅ 应用完成! ")
    except Exception as e:
        print(f"❌ 应用失败: {e}")


def _interactive_validate(helper, args):
    """交互式验证"""
    markdown_file = args[0] if args else None

    if not markdown_file:
        markdown_file = input("请输入要验证的Markdown文件路径: ").strip()
        if not markdown_file:
            print("❌ 必须指定Markdown文件")
            return

    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        validation_result = helper.validate_response_format(content, verbose=True)

        print(f"\n格式验证结果: ")
        print(f"  有效: {'✅ 是' if validation_result['is_valid'] else '❌ 否'}")
        print(f"  格式类型: {validation_result['format_type']}")
        print(f"  文件数: {validation_result['file_count']}")

        if validation_result['files']:
            print(f"  文件列表: ")
            for file in validation_result['files']:
                print(f"    - {file}")

        if validation_result['warnings']:
            print(f"  ⚠️  警告: ")
            for warning in validation_result['warnings']:
                print(f"    - {warning}")

        if validation_result['issues']:
            print(f"  ❌ 问题: ")
            for issue in validation_result['issues']:
                print(f"    - {issue}")

    except Exception as e:
        print(f"❌ 验证失败: {e}")


def _interactive_session(session_manager, args):
    """交互式会话管理"""
    if not args:
        print("会话命令: start, log, history, list")
        return

    sub_action = args[0].lower()

    if sub_action == 'start':
        session_name = args[1] if len(args) > 1 else input("请输入会话名称: ").strip()
        if session_name:
            print(session_manager.start_session(session_name))
        else:
            print("❌ 必须指定会话名称")

    elif sub_action == 'log':
        session_name = args[-1] if len(args) > 1 else input("请输入会话名称: ").strip()
        task = None
        description = " "

        # 查找任务参数
        for i, arg in enumerate(args):
            if arg == '--task' and i + 1 < len(args):
                task = args[i + 1]
            elif arg == '--desc' and i + 1 < len(args):
                description = args[i + 1]

        if not task:
            task = input("请输入任务名称: ").strip()
        if not description:
            description = input("请输入任务描述 (可选): ").strip()

        if session_name and task:
            print(session_manager.log_task(session_name, task, description))
        else:
            print("❌ 必须指定会话名称和任务")

    elif sub_action == 'history':
        session_name = args[1] if len(args) > 1 else input("请输入会话名称: ").strip()
        if session_name:
            print(session_manager.show_session_history(session_name))
        else:
            print("❌ 必须指定会话名称")

    elif sub_action == 'list':
        print(session_manager.list_sessions())

    else:
        print(f"❌ 未知的会话命令: {sub_action}")


def _interactive_config(helper, args):
    """交互式配置管理"""
    if not args:
        print("配置命令: init, show")
        return

    sub_action = args[0].lower()

    if sub_action == 'init':
        helper.init_config()
    elif sub_action == 'show':
        helper.show_config()
    else: 
        print(f"❌ 未知的配置命令: {sub_action}")


def _show_tasks(helper):
    """显示任务列表"""
    tasks = helper.task_manager.list_tasks()
    print("=== 可用任务模板 ===")
    for key, task in tasks.items():
        print(f"{key}: {task['name']}")
        print(f"  描述: {task['description']}")
        print()


def _show_extensions(helper):
    """显示支持的扩展名"""
    print("支持的文件扩展名: ")
    for ext in helper.list_supported_extensions():
        print(f"  {ext}")


def _interactive_feature(feature_manager, args):
    """交互式特性管理"""
    if not args:
        print("特性命令: list, show, edit, find")
        return

    sub_action = args[0].lower()

    if sub_action == 'list':
        status_filter = None
        if '--status' in args:
            try:
                status_idx = args.index('--status')
                status_filter = args[status_idx + 1]
            except (IndexError, ValueError):
                print("⚠️  --status 参数格式不正确")
        features = feature_manager.list_features(status_filter)
        if not features:
            print(f"ℹ️  没有找到{'状态为 ' + status_filter + ' 的' if status_filter else ''}特性。")
        else:
            print(f"=== 特性列表 ({len(features)} 个){' - 状态: ' + status_filter if status_filter else ''} ===")
            for feat in features:
                print(f"ID: {feat['id']}, 状态: {feat['status']}")
                print(f"  描述: {feat['description']}")
                print(f"  创建时间: {feat.get('created_at', 'N/A')}")
                if feat.get('exported_at'):
                    print(f"  导出时间: {feat['exported_at']}")
                if feat.get('applied_at'):
                    print(f"  应用时间: {feat['applied_at']}")
                if feat.get('export_file'):
                    print(f"  导出文件: {feat['export_file']}")
                if feat.get('response_file'):
                    print(f"  响应文件: {feat['response_file']}")
                print("-" * 20)

    elif sub_action == 'show':
        feature_id = args[1] if len(args) > 1 else input("请输入特性ID: ").strip()
        if not feature_id:
            print("❌ 必须指定特性ID")
            return
        feature = feature_manager.get_feature(feature_id)
        if not feature:
            print(f"❌ 未找到特性: {feature_id}")
            return
        print(f"=== 特性详情: {feature_id} ===")
        print(f"状态: {feature['status']}")
        print(f"描述: {feature['description']}")
        print(f"创建时间: {feature.get('created_at', 'N/A')}")
        if feature.get('exported_at'):
            print(f"导出时间: {feature['exported_at']}")
        if feature.get('applied_at'):
            print(f"应用时间: {feature['applied_at']}")
        if feature.get('export_file'):
            print(f"关联导出文件: {feature['export_file']}")
        if feature.get('response_file'):
            print(f"关联响应文件: {feature['response_file']}")

    elif sub_action == 'edit':
        feature_manager.edit_features_file()

    elif sub_action == 'find':
        keyword = args[1] if len(args) > 1 else input("请输入描述关键词: ").strip()
        if not keyword:
            print("❌ 必须指定关键词")
            return
        features = feature_manager.find_feature_by_description(keyword)
        if not features:
            print(f"ℹ️  未找到包含关键词 '{keyword}' 的特性。")
        else:
            print(f"=== 匹配特性 (关键词: '{keyword}') ===")
            for feat in features:
                print(f"ID: {feat['id']}, 状态: {feat['status']}")
                print(f"  描述: {feat['description']}")
                print("-" * 20)
    else:
        print(f"❌ 未知的 feature 子命令: {sub_action}")
