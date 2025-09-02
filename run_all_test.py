#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有测试的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_test_module(module_name, test_functions):
    """运行测试模块"""
    print(f"\n🚀 运行 {module_name} 测试...")
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"  ✅ {test_func.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test_func.__name__}: {e}")
            failed += 1
    
    return passed, failed


def run_all_tests():
    """运行所有测试"""
    print("🧪 开始运行所有测试...")
    
    # 测试结果统计
    total_passed = 0
    total_failed = 0
    
    try:
        # 基本测试
        from tests.test_basic import (
            test_import_modules,
            test_helper_initialization,
            test_session_manager_initialization,
            test_feature_manager_initialization,
            test_parser_creation
        )
        
        passed, failed = run_test_module("基本测试", [
            test_import_modules,
            test_helper_initialization,
            test_session_manager_initialization,
            test_feature_manager_initialization,
            test_parser_creation
        ])
        total_passed += passed
        total_failed += failed
        
        # CLI测试
        from tests.test_cli import (
            test_cli_import,
            test_cli_main_function_exists
        )
        
        passed, failed = run_test_module("CLI测试", [
            test_cli_import,
            test_cli_main_function_exists
        ])
        total_passed += passed
        total_failed += failed
        
        # 参数解析器测试
        from tests.test_parser import (
            test_parser_creation as parser_test1,
            test_basic_action_parsing,
            test_export_with_paths,
            test_apply_with_paths,
            test_interactive_mode_flag,
            test_config_flags,
            test_list_flags
        )
        
        passed, failed = run_test_module("参数解析器测试", [
            parser_test1,
            test_basic_action_parsing,
            test_export_with_paths,
            test_apply_with_paths,
            test_interactive_mode_flag,
            test_config_flags,
            test_list_flags
        ])
        total_passed += passed
        total_failed += failed
        
        # 核心模块测试
        from tests.test_core_helper import (
            test_helper_import,
            test_helper_initialization as helper_init_test,
            test_helper_has_required_methods
        )
        
        passed, failed = run_test_module("核心助手类测试", [
            test_helper_import,
            helper_init_test,
            test_helper_has_required_methods
        ])
        total_passed += passed
        total_failed += failed
        
        from tests.test_core_session import (
            test_session_manager_import,
            test_session_manager_initialization as session_init_test,
            test_session_manager_with_existing_data,
            test_session_manager_has_required_methods
        )
        
        passed, failed = run_test_module("会话管理器测试", [
            test_session_manager_import,
            session_init_test,
            test_session_manager_with_existing_data,
            test_session_manager_has_required_methods
        ])
        total_passed += passed
        total_failed += failed
        
        from tests.test_core_features import (
            test_feature_manager_import,
            test_feature_manager_initialization as feature_init_test,
            test_feature_manager_with_existing_data,
            test_feature_manager_has_required_methods
        )
        
        passed, failed = run_test_module("特性管理器测试", [
            test_feature_manager_import,
            feature_init_test,
            test_feature_manager_with_existing_data,
            test_feature_manager_has_required_methods
        ])
        total_passed += passed
        total_failed += failed
        
        # 工具模块测试
        from tests.test_utils import (
            test_utils_import,
            test_parser_function_exists
        )
        
        passed, failed = run_test_module("工具模块测试", [
            test_utils_import,
            test_parser_function_exists
        ])
        total_passed += passed
        total_failed += failed
        
        total_passed += passed
        total_failed += failed
        
    except Exception as e:
        print(f"❌ 测试运行过程中出现错误: {e}")
        return False
    
    # 输出测试结果总结
    print(f"\n📊 测试结果总结:")
    print(f"   通过: {total_passed}")
    print(f"   失败: {total_failed}")
    print(f"   总计: {total_passed + total_failed}")
    
    if total_failed == 0:
        print("\n🎉 所有测试都通过了！")
        return True
    else:
        print(f"\n⚠️  有 {total_failed} 个测试失败。")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
