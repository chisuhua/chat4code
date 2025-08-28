#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chat4code 命令行接口模块
"""

import argparse
import os
from .core import CodeProjectAIHelper
from .session import SessionManager

def main():
    """主函数 - 命令行接口"""
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
    
    parser.add_argument('action', nargs='?', choices=['export', 'apply', 'validate', 'session', 'debug-parse', 'config', 'help'],
                       help='操作类型: export(导出代码), apply(应用响应), validate(验证格式), session(会话管理), debug-parse(调试解析), config(配置管理), help(帮助)')
    
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
    parser.add_argument('--task-prompt', action='store_true', help='在导出文件中包含任务提示')
    
    # 自定义任务内容参数
    parser.add_argument('--task-content', help='为任务提供具体要求内容（如add_feature）')
    
    # 配置相关参数
    parser.add_argument('--config-init', action='store_true', help='初始化配置文件')
    parser.add_argument('--config-show', action='store_true', help='显示当前配置')
    
    # 交互模式参数
    parser.add_argument('--interactive', '-i', action='store_true', help='启动交互式模式')
    
    # 会话相关参数
    parser.add_argument('--session-task', dest='session_task', help='会话中的任务')
    parser.add_argument('--desc', '--description', dest='description', help='任务描述')
    
    args = parser.parse_args()
    
    # 如果指定了交互模式，启动交互式界面
    if args.interactive:
        interactive_mode()
        return
    
    # 初始化助手
    helper = CodeProjectAIHelper()
    session_manager = SessionManager()
    
    # 处理配置相关命令
    if args.config_init:
        helper.init_config()
        return
    
    if args.config_show:
        helper.show_config()
        return
    
    # 处理 --list-tasks 参数
    if args.list_tasks:
        tasks = helper.task_manager.list_tasks()
        print("=== 可用任务模板 ===")
        print(" ")
        for key, task in tasks.items():
            print(f"{key}: {task['name']}")
            print(f"  描述: {task['description']}")
            print(" ")
        return
    
    # 处理 --list-extensions 参数
    if args.list_extensions:
        print("支持的文件扩展名: ")
        for ext in helper.list_supported_extensions():
            print(f"  {ext}")
        return
    
    # 处理 --task-format 参数
    if args.task_format:
        print(helper.task_manager.show_task_format(args.task_format))
        return
    
    # 处理 help 动作 
    if args.action == 'help' or not args.action:
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
            "   python -m chat4code export ./my_project project.md --task analyze --task-prompt  # 任务提示包含在文件中",
            " ",
            "5. 自定义任务内容: ",
            "   python -m chat4code export ./my_project project.md --task add_feature --task-content \"添加用户登录功能\"",
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
            "12. 调试解析: ",
            "    python -m chat4code debug-parse response.md",
            " ",
            "支持的文件类型: ",
            ",  ".join(helper.list_supported_extensions()),
            " "
        ]
        print("\n".join(instructions))
        return
    
    # 处理 session 动作
    if args.action == 'session':
        if len(args.paths) < 1:
            print("❌ 错误: session操作需要指定子命令")
            print("用法: python -m chat4code session start <会话名>")
            print("     python -m chat4code session log --task <任务> [--desc <描述>] <会话名>")
            print("     python -m chat4code session history <会话名>")
            print("     python -m chat4code session list")
            return
        
        sub_action = args.paths[0]
        if sub_action == 'start':
            if len(args.paths) < 2:
                print("❌ 错误: 需要指定会话名称")
                return
            session_name = args.paths[1]
            print(session_manager.start_session(session_name))
        
        elif sub_action == 'log':
            if not args.session_task:
                print("❌ 错误: 需要指定 --task 参数")
                return
            if len(args.paths) < 2:
                print("❌ 错误: 需要指定会话名称")
                return
            session_name = args.paths[1]
            print(session_manager.log_task(session_name, args.session_task, args.description or " "))
        
        elif sub_action == 'history':
            if len(args.paths) < 2:
                print("❌ 错误: 需要指定会话名称")
                return
            session_name = args.paths[1]
            print(session_manager.show_session_history(session_name))
        
        elif sub_action == 'list': 
            print(session_manager.list_sessions())
        
        else:
            print(f"❌ 未知的session子命令: {sub_action}")
            return
        
        return
    
    # 处理 validate 动作
    if args.action == 'validate':
        if len(args.paths) < 1:
            print("❌ 错误: validate操作需要指定Markdown文件")
            return
        
        markdown_file = args.paths[0]
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            validation_result = helper.validate_response_format(content, args.verbose)
            
            print(f"格式验证结果: ")
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
            
            if args.verbose and 'details' in validation_result:
                print(f"  详细信息: ")
                print(f"    解析方法: {validation_result['details']['method']}")
                print(f"    提取文件数: {len(validation_result['details']['extracted_files'])}")
                    
        except Exception as e:
            print(f"❌ 验证失败: {e}")
        return
    
    # 处理 debug-parse 动作
    if args.action == 'debug-parse':
        if len(args.paths) < 1:
            print("❌ 错误: debug-parse操作需要指定Markdown文件")
            return
    
        markdown_file = args.paths[0]
        if '--detailed' in args.paths or '-d' in args.paths:
            helper.debug_parse_detailed(markdown_file) 
        else:
            helper.debug_parse_response(markdown_file)
        return
    
    # 处理 config 动作
    if args.action == 'config':
        if len(args.paths) < 1:
            print("❌ 错误: config操作需要指定子命令")
            print("用法: python -m chat4code config init")
            print("     python -m chat4code config show")
            return
        
        sub_action = args.paths[0]
        if sub_action == 'init':
            helper.init_config()
        elif sub_action == 'show':
            helper.show_config()
        else:
            print(f"❌ 未知的config子命令: {sub_action}")
        return
    
    # 处理 export 动作
    if args.action == 'export':
        if len(args.paths) < 1:
            print("❌ 错误: export操作需要指定源目录")
            print("用法: python -m chat4code export <源目录> [输出文件]")
            print("示例: python -m chat4code export dir1 dir2 output.md")
            print("示例: python -m chat4code export ex* output.md")
            return
        
        # 所有参数除了最后一个都是源目录，最后一个（如果存在）是输出文件
        src_dirs = args.paths[:-1] if len(args.paths) > 1 else args.paths
        output_file = args.paths[-1] if len(args.paths) > 1 and not args.paths[-1].endswith(('.md', '.txt', '.markdown')) and os.path.splitext(args.paths[-1])[1] == '' else \
                     args.paths[-1] if len(args.paths) > 1 else None
        
        # 如果最后一个参数看起来像文件名，则它是输出文件，其余是源目录
        if len(args.paths) > 1 and (args.paths[-1].endswith(('.md', '.txt', '.markdown')) or '.' in os.path.splitext(args.paths[-1])[1]):
            src_dirs = args.paths[:-1]
            output_file = args.paths[-1]
        else:
            src_dirs = args.paths
            output_file = None
        
        extensions = tuple(args.ext) if args.ext else helper.default_extensions
        try:
            helper.export_to_markdown(
                src_dirs, output_file, extensions, args.task,
                args.incremental, args.since_time,
                args.task_prompt,  # 使用 --task-prompt 参数
                args.task_content  # 使用 --task-content 参数
            )
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return
    
    # 处理 apply 动作
    elif args.action == 'apply':
        if len(args.paths) < 2:
            print("❌ 错误: apply操作需要指定Markdown文件和目标目录")
            print("用法: python -m chat4code apply <Markdown文件> <目标目录>")
            return
        
        markdown_file = args.paths[0]
        dst_dir = args.paths[1]
        
        try:
            # 应用到本地，使用灵活解析模式
            helper.apply_markdown_response(
                markdown_file, dst_dir, 
                not args.no_backup if args.no_backup else None,  # 如果指定了--no-backup则为False，否则使用配置默认值
                not args.strict,  # 默认使用灵活解析
                args.show_diff    # 显示差异
            )
        except Exception as e:
            print(f"❌ 应用失败: {e}")
            return

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
                print("👋 再见！")
                break
                
            if command.lower() == 'help':
                _show_interactive_help()
                continue
                
            # 解析命令
            parts = command.split()
            action = parts[0].lower()
            
            if action == 'export':
                _interactive_export(helper, parts[1:])
            elif action == 'apply':
                _interactive_apply(helper, parts[1:])
            elif action == 'validate':
                _interactive_validate(helper, parts[1:])
            elif action == 'session':
                _interactive_session(session_manager, parts[1:])
            elif action == 'config':
                _interactive_config(helper, parts[1:])
            elif action == 'tasks':
                _show_tasks(helper)
            elif action == 'extensions':
                _show_extensions(helper)
            else:
                print(f"❌ 未知命令: {action}")
                print("输入 'help' 查看可用命令")
                
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
  apply [文件] [目录] [--show-diff] [--no-backup]                     应用AI响应
  validate [文件]                                                      验证响应格式
  session start|log|history|list [参数]                               会话管理
  config init|show                                                     配置管理
  tasks                                                               显示可用任务
  extensions                                                          显示支持的扩展名
  help                                                                 显示此帮助
  quit/exit                                                           退出程序
    """
    print(help_text)

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
    
    # 如果没有指定任务，直接进入任务选择流程，不再询问 y/N
    # 修改点：移除了 "use_task = input("是否指定任务? (y/N): ").strip().lower()" 这一步
    if not task:
        # 直接显示可用任务并让用户选择
        tasks = list(helper.task_manager.list_tasks().keys())
        if tasks:
            print("可用任务: ")
            for i, t in enumerate(tasks, 1):
                print(f"  {i}. {t}")
            try:
                choice_input = input("请选择任务 (输入数字，或直接回车跳过): ").strip()
                if choice_input: # 只有在用户输入了内容时才尝试解析
                    choice = int(choice_input) - 1
                    if 0 <= choice < len(tasks):
                        task = tasks[choice]
                    else:
                        print("无效选择，跳过任务指定")
            except ValueError: # 捕获非数字输入
                print("无效输入，跳过任务指定")
        else:
            print("当前没有可用的任务模板。")
    
    # 如果是 add_feature 任务且没有指定具体内容，询问用户输入
    if task == "add_feature" and not task_content:
        task_content = input("请输入具体功能需求: ").strip()
    
    # 询问是否在导出文件中包含任务提示 (这部分保持不变，因为它是在已选择任务后才询问)
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

    # 询问是否在导出文件中包含任务提示 (仅当有任务且有输出文件时)

    if task and output_file:
        include_prompt = input("是否在导出文件中包含任务提示? (Y/n): ").strip().lower()
        if include_prompt != 'n':
            include_task_prompt = True
    
    try:
        result_file = helper.export_to_markdown(
            src_dirs, output_file, task=task, 
            incremental=incremental, 
            include_task_prompt=include_task_prompt,
            custom_task_content=task_content
        )
        print("✅ 导出完成! ")
        print(f"   导出文件: {result_file}")
    except Exception as e:
        print(f"❌ 导出失败: {e}")

# 在交互式应用函数中添加自动文件名选择
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
        helper.apply_markdown_response(
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

if __name__ == "__main__":
    main()
