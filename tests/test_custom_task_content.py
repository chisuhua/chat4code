"""
测试自定义任务内容功能
"""

import os
import tempfile
from chat4code.core import CodeProjectAIHelper
from chat4code.tasks import TaskManager

def test_custom_task_content():
    """测试自定义任务内容功能"""
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试文件
        test_file = os.path.join(temp_dir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('Hello World')")
        
        # 初始化助手
        helper = CodeProjectAIHelper()
        
        # 测试自定义任务内容
        output_file = os.path.join(temp_dir, "custom_task_export.md")
        helper.export_to_markdown(
            [temp_dir], 
            output_file, 
            task="add_feature",
            custom_task_content="添加用户认证功能"
        )
        
        # 验证输出文件存在
        assert os.path.exists(output_file)
        
        # 读取并验证内容
        with open(output_file, "r") as f:
            content = f.read()
            assert "添加用户认证功能" in content
            assert "[请在此处描述具体功能需求]" not in content
            
        print("✅ 自定义任务内容测试通过")

def test_task_manager_customization():
    """测试任务管理器的定制功能"""
    task_manager = TaskManager()
    
    # 测试定制 add_feature 任务
    customized_prompt = task_manager.customize_task_prompt(
        "add_feature", 
        "generic", 
        "实现数据导出到CSV功能"
    )
    
    assert customized_prompt is not None
    assert "实现数据导出到CSV功能" in customized_prompt
    assert "[请在此处描述具体功能需求]" not in customized_prompt
    
    # 测试不存在的任务
    customized_prompt = task_manager.customize_task_prompt(
        "nonexistent_task", 
        "generic", 
        "some content"
    )
    
    assert customized_prompt is None
    
    print("✅ 任务管理器定制功能测试通过")

if __name__ == "__main__":
    test_custom_task_content()
    test_task_manager_customization()
