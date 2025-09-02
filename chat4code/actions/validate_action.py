#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证动作处理器
"""


def process(args, helper):
    """处理验证动作"""
    if len(args.paths) < 1:
        print("❌ 错误: validate操作需要指定Markdown文件")
        return

    markdown_file = args.paths[0]
    try:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        validation_result = helper.validate_response_format(content, args.verbose)

        _display_validation_result(validation_result, args.verbose)

    except Exception as e:
        print(f"❌ 验证失败: {e}")


def _display_validation_result(validation_result, verbose):
    """显示验证结果"""
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

    if verbose and 'details' in validation_result:
        print(f"  详细信息: ")
        print(f"    解析方法: {validation_result['details']['method']}")
        print(f"    提取文件数: {len(validation_result['details']['extracted_files'])}")
