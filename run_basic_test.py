#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试运行脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_basic_tests():
    """运行基本测试"""
    print("🚀 开始运行基本测试...")
    
    try:
        # 导入测试模块
        from tests.test_basic import (
            test_import_modules,
            test_helper_initialization,
            test_session_manager_initialization,
            test_feature_manager_initialization,
            test_parser_creation
        )
        
        # 运行所有测试
        test_functions = [
            test_import_modules,
            test_helper_initialization,
            test_session_manager_initialization,
            test_feature_manager_initialization,
            test_parser_creation
        ]
        
        for test_func in test_functions:
            try:
                test_func()
                print(f"✅ {test_func.__name__} 通过")
            except Exception as e:
                print(f"❌ {test_func.__name__} 失败: {e}")
                return False
        
        print("\n🎉 所有基本测试都通过了！")
        return True
        
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        return False

if __name__ == "__main__":
    success = run_basic_tests()
    sys.exit(0 if success else 1)
