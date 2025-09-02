#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
特性动作处理器
"""


def process(args, feature_manager):
    """处理特性动作"""
    if len(args.paths) < 1:
        _show_feature_usage()
        return

    sub_action = args.paths[0]
    action_handlers = {
        'list': lambda: _handle_list(args, feature_manager),
        'show': lambda: _handle_show(args, feature_manager),
        'edit': lambda: _handle_edit(feature_manager),
        'find': lambda: _handle_find(args, feature_manager)
    }

    handler = action_handlers.get(sub_action)
    if handler:
        handler()
    else:
        print(f"❌ 未知的 feature 子命令: {sub_action}")


def _show_feature_usage():
    """显示特性用法"""
    print("❌ 错误: feature 操作需要指定子命令")
    print("用法: python -m chat4code feature list [--status <status>]")
    print("     python -m chat4code feature show <ID>")
    print("     python -m chat4code feature edit")
    print("     python -m chat4code feature find <描述关键词>")


def _handle_list(args, feature_manager):
    """处理列表显示"""
    status_filter = None
    if '--status' in args.paths:
        try:
            status_idx = args.paths.index('--status')
            status_filter = args.paths[status_idx + 1]
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


def _handle_show(args, feature_manager):
    """处理显示详情"""
    if len(args.paths) < 2:
        print("❌ 错误: 需要指定特性ID")
        return
    feature_id = args.paths[1]
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


def _handle_edit(feature_manager):
    """处理编辑"""
    feature_manager.edit_features_file()


def _handle_find(args, feature_manager):
    """处理查找"""
    if len(args.paths) < 2:
        print("❌ 错误: 需要指定描述关键词")
        return
    keyword = args.paths[1]
    features = feature_manager.find_feature_by_description(keyword)
    if not features:
        print(f"ℹ️  未找到包含关键词 '{keyword}' 的特性。")
    else:
        print(f"=== 匹配特性 (关键词: '{keyword}') ===")
        for feat in features:
            print(f"ID: {feat['id']}, 状态: {feat['status']}")
            print(f"  描述: {feat['description']}")
            print("-" * 20)
