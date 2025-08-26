## 基本概念

chat4code 是一个双向转换工具，帮助你在本地代码项目和AI对话之间建立桥梁。

### 工作流程

```
本地代码项目 → [chat4code export] → Markdown文件 → AI对话 → 
Markdown响应 → [chat4code apply] → 更新后的本地项目
```

## 详细使用说明

### 1. 导出项目代码

#### 基本导出
```bash
python chat4code.py export ./my_project project.md
```

#### 指定文件类型
```bash
python chat4code.py export ./my_project project.md --ext .py .js .html
```

#### 快速导出（输出到控制台）
```bash
python chat4code.py export ./my_project
```

### 2. 应用AI响应

#### 基本应用
```bash
python chat4code.py apply ai_response.md ./updated_project
```

#### 不创建备份
```bash
python chat4code.py apply ai_response.md ./updated_project --no-backup
```

## 与AI对话的最佳实践

### 1. 准备阶段
```bash
# 导出项目
python chat4code.py export --src ./my_project --output project_for_ai.md

# 上传 project_for_ai.md 给AI
```

### 2. 对话提示模板
```
我将上传一个Markdown文件，其中包含了我项目的代码。
请帮我：
1. 分析这个项目的主要功能
2. [你的具体需求，如：添加一个排序功能]
3. 按照原始格式返回修改后的代码

要求：
- 只返回需要修改或新增的文件
- 保持原有的文件路径结构
- 使用正确的代码块语言标识
```

### 3. 应用修改
```bash
# 将AI的响应保存为 response.md
python chat4code.py apply --input response.md --dst ./updated_project
```

## 常见问题

### Q: 导出的文件太大怎么办？
A: 可以分模块导出，或者只导出核心文件：
```bash
python chat4code.py export --src ./my_project/src/core --output core.md
```

### Q: 如何添加新的文件类型支持？
A: 修改 `chat4code.py` 中的 `language_map` 字典。

### Q: 应用响应时出错怎么办？
A: 检查AI返回的格式是否正确，确保使用了标准的Markdown代码块格式。

## 高级用法

### 批量处理
```bash
# 处理多个项目
for project in project1 project2 project3; do
    python chat4code.py export --src ./$project --output ./$project.md
done
```

### 与版本控制结合
```bash
# 导出前创建分支
git checkout -b ai-modification
python chat4code.py export --src ./my_project --output project.md

# 应用后提交
python chat4code.py apply --input response.md --dst ./my_project
git add .
git commit -m "Apply AI modifications"
```
```

