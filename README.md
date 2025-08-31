# chat4code 🤖

让代码项目与AI对话变得简单

[![Python](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 简介

chat4code 是一个简单易用的工具，帮助开发者将本地代码项目转换为适合与AI对话的Markdown格式，同时也能将AI生成的代码响应转换回本地文件。

---

### 📁 使用流程

```
[导出代码给AI对话] 
        ↓
   生成 prompt.txt → 你复制内容 → 粘贴给 AI
        ↑               ↓
      （你）     你复制 AI 回答 → 保存为 response.md
                        ↓
               [应用AI响应到本地]
                        ↓
                   [执行本地开发任务]
```

---

## 功能特点

- 🔄 **双向转换**：代码 ↔ Markdown
- 🎯 **任务模板**：预设常用AI任务
- 📈 **增量处理**：支持增量导出和应用
- 🌍 **多语言支持**：支持多种编程语言语法高亮
- 🛡️ **安全操作**：自动备份、路径安全检查
- 🔍 **差异对比**：显示文件变更详情
- ⌨️ **多种交互方式**：命令行、交互式、配置化
- 📦 **零依赖**：只使用Python标准库
- 🧩 **模板系统**：减少提示词重复，提高维护效率
- 📋 **功能需求管理**：保存、查询和跟踪功能需求，支持状态管理、标签和搜索

## 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/chat4code.git  
cd chat4code

# 直接使用（无需安装）
python -m chat4code --help

# 或者安装为命令
pip install -e .
```

## 快速开始

### 1. 导出代码给AI对话

```bash
# 导出到文件
python -m chat4code export ./my_project project.md

# 快速导出（输出到控制台）
python -m chat4code export ./my_project

# 导出并添加任务提示
python -m chat4code export ./my_project project.md --task analyze

# 增量导出（只导出变更的文件）
python -m chat4code export ./my_project changes.md --incremental

# 导出自指定时间以来的变更
python -m chat4code export ./my_project recent.md --since 2024-01-01T10:00:00
```

### 2. 应用AI响应到本地

```bash
# 基本用法
python -m chat4code apply response.md ./updated_project

# 应用并显示差异
python -m chat4code apply response.md ./updated_project --show-diff

# 不创建备份文件
python -m chat4code apply response.md ./updated_project --no-backup
```

### 3. 交互式模式

```bash
# 启动交互式模式
python -m chat4code --interactive
# 或
python -m chat4code -i
```

在交互式模式中：
```
chat4code> export ./my_project project.md --task analyze
chat4code> apply response.md ./updated_project --show-diff
chat4code> tasks
chat4code> help
chat4code> quit
```

## 常用任务类型

| 任务代码 | 任务名称 | 说明 |
|---------|---------|------|
| analyze | 代码分析 | 分析项目结构和功能 |
| bugfix | Bug修复 | 修复代码中的错误 |
| optimize | 性能优化 | 优化代码性能 |
| document | 添加注释文档 | 为代码添加注释和文档 |
| test | 添加测试 | 为代码添加单元测试 |
| refactor | 代码重构 | 改善代码结构和可读性 |
| add_feature | 添加功能 | 添加新功能特性 |
| security | 安全检查 | 检查代码安全问题 |
| port | 代码移植 | 移植到其他平台或语言 |
| review | 代码审查 | 进行全面代码审查 |
| autonomous_development | 自主开发 | 自主执行开发任务 |
| systematic_debugging | 系统调试 | 系统性的问题分析和解决 |
| comprehensive_review | 全面审查 | 全面的代码质量审查 |
| deep_analysis | 深度分析 | 深度项目架构和技术分析 |
| interactive_development | 交互开发 | 支持交互式的渐进开发 |

## 高级功能

### 配置管理
```bash
# 初始化配置文件
python -m chat4code --config-init

# 查看当前配置
python -m chat4code --config-show
```

### 会话管理
```bash
# 创建开发会话
python -m chat4code session start my_development

# 记录任务
python -m chat4code session log --task "添加用户认证" --description "实现登录注册功能" my_development

# 查看会话历史
python -m chat4code session history my_development

# 列出所有会话
python -m chat4code session list
```

### 功能需求管理

功能需求管理系统帮助您跟踪和管理通过`add_feature`任务创建的功能需求，支持状态管理、标签系统和多种视图选项。

#### 状态管理

每个功能需求有三种状态：
- `pending`（待处理）：已创建但尚未导出
- `exported`（已导出）：已导出给AI但尚未应用
- `applied`（已应用）：AI响应已应用到本地代码

#### 标签系统

为功能需求添加标签，便于分类和过滤：
```bash
# 为功能添加标签
python -m chat4code feature tag add 1 auth high-priority

# 移除功能标签
python -m chat4code feature tag remove 1 high-priority

# 列出所有标签
python -m chat4code feature tags
```

#### 搜索能力

按关键词、状态和标签搜索功能需求：
```bash
# 搜索关键词
python -m chat4code feature search "登录"

# 带状态过滤的搜索
python -m chat4code feature search "登录" --status applied
```

#### 视图选项

多种视图选项帮助您更好地组织和查看功能需求：

```bash
# 默认视图（按时间排序）
python -m chat4code feature list

# 按状态视图
python -m chat4code feature list --view status

# 按标签视图
python -m chat4code feature list --view tags

# 按时间线视图
python -m chat4code feature list --view timeline
```

#### 基本用法

```bash
# 保存功能需求
python -m chat4code export ./my_project --task add_feature --task-content "添加用户登录功能"

# 查看功能需求列表
python -m chat4code feature list

# 查看特定功能详情
python -m chat4code feature show 1

# 直接编辑功能数据库
python -m chat4code feature edit
```

#### 与工作流集成

功能需求管理系统与导出和应用流程无缝集成：

1. **导出阶段**：当执行`add_feature`任务时，功能描述自动保存到数据库
2. **应用阶段**：当应用AI响应后，关联的功能需求自动标记为"已应用"
3. **状态跟踪**：您可以通过`feature list`随时查看功能需求的状态

### 格式验证
```bash
# 验证AI响应格式
python -m chat4code validate response.md

# 详细验证
python -m chat4code validate response.md --verbose
```

### 调试工具
```bash
# 调试AI响应解析
python -m chat4code debug-parse response.md
```

## 模板系统

chat4code 使用模板系统来减少提示词重复，提高维护效率。

### 模板定义

在 `prompts.yaml` 中定义模板：

```yaml
templates:
  standard_response:
    name: "标准响应模板"
    description: "标准的AI响应格式要求"
    template: |
      **请按照以下要求执行任务**:
      请对上面所有代码进行{{action}}，并按以下规则返回结果：

      1. 保持原有的 `## 文件路径` 结构；
      2. 在每个原始代码块位置，替换成{{action_desc}}：
      ```markdown
      ## 文件路径1
      ```cpp
      // {{result_desc}}
      ```
      ```
      3. {{additional_rules}}
      4. 不要合并文件、不要省略代码、不要添加额外解释；
      5. 确保输出仍是有效的 Markdown；
      6. 保留项目头部信息（项目名称、导出时间等）；
      7. {{file_selection_rule}}
```

### 模板使用

在具体任务中引用模板：

```yaml
generic:
  optimize:
    name: "性能优化"
    description: "优化代码性能"
    prompt: |
      请分析代码的性能瓶颈，并提供优化建议。
      
      {{standard_response:
        action=优化,
        action_desc=优化后的新代码块,
        result_desc=优化后的代码内容,
        additional_rules=每个文件后可附加「### 优化说明」，列出改进点；,
        file_selection_rule=只返回需要修改的文件。
      }}
```

### 模板优势

1. **减少重复** - 避免在每个任务中重复相同的格式要求
2. **易于维护** - 统一修改格式要求只需修改模板
3. **保持一致性** - 所有任务使用相同的响应格式
4. **灵活定制** - 通过参数定制模板内容
5. **提高可读性** - 任务定义更加简洁明了

## 配置文件

chat4code 支持通过 `.chat4code.json` 文件进行配置：

```json
{
  "default_extensions": [".cpp", ".h", ".cc", ".hh", ".py", ".js"],
  "language_map": {
    ".cpp": "cpp",
    ".py": "python",
    ".js": "javascript"
  },
  "exclude_patterns": ["*.log", "*.tmp", "node_modules/"],
  "backup_enabled": true,
  "metadata_dir": ".chat4code",
  "prompts_file": "./my_prompts.yaml",
  "project_type": "cpp",
  "development_mode": "batch",
  "default_source_dir": "./my_project",
  "default_target_dir": "./updated_project",
  "export_filename_pattern": "req.md",
  "import_filename_pattern": "resp.md",
  "export_output_dir": "./exports",
  "import_output_dir": "./imports"
}
```

### 自动序列化文件名功能

chat4code 支持自动序列化文件名功能：

- **导出文件**: 如果配置 `export_filename_pattern` 为 `req.md`，则自动创建 `req1.md`, `req2.md`, `req3.md`...
- **导入文件**: 如果配置 `import_filename_pattern` 为 `resp.md`，则自动创建 `resp1.md`, `resp2.md`, `resp3.md`...

### 默认目录配置

- `default_source_dir`: 默认源代码目录
- `default_target_dir`: 默认应用目标目录
- `export_output_dir`: 导出文件存储目录
- `import_output_dir`: 导入文件存储目录

### 项目类型配置

chat4code 支持自动检测项目类型，也可以通过配置强制指定：

```json
{
  "project_type": "cpp"  // 强制指定为C++项目
}
```

支持的项目类型：
- `cpp`: C/C++ 项目
- `python`: Python 项目  
- `javascript`: JavaScript/TypeScript 项目
- `generic`: 通用项目（混合类型或无法识别的项目）

当配置了 `project_type` 时，chat4code 会：
1. 使用配置指定的项目类型
2. 不再自动检测项目类型
3. 使用对应类型的任务提示词

### 初始化配置
```bash
# 初始化配置文件和示例提示词文件
python -m chat4code --config-init
```

这将创建以下目录结构：
```
.
├── .chat4code.json          # 配置文件
├── prompts.yaml             # 提示词文件
├── exports/                 # 导出文件目录
└── imports/                 # 导入文件目录
└── .chat4code/              # 元数据目录（包含features.json等）
```

## 使用流程

### 完整开发工作流
1. **准备项目**：
   ```bash
   python -m chat4code export ./my_project project_for_ai.md --task analyze
   ```

2. **与AI对话**：
   - 将 `project_for_ai.md` 上传给AI
   - AI会根据任务提示执行相应操作

3. **验证响应**：
   ```bash
   python -m chat4code validate ai_response.md
   ```

4. **应用修改**：
   ```bash
   python -m chat4code apply ai_response.md ./updated_project --show-diff
   ```

5. **查看差异**：
   ```bash
   # 差异信息会自动显示在应用结果中
   ```

### 功能需求管理工作流

```bash
# 1. 保存功能需求
python -m chat4code export ./my_project --task add_feature --task-content "添加用户登录功能"

# 2. 查看功能需求列表
python -m chat4code feature list
# 输出示例：
# ⏳ #1 [pending] 添加用户登录功能
#    🏷️ 标签: auth, high-priority

# 3. 应用AI响应
python -m chat4code apply response.md ./updated_project

# 4. 再次查看功能需求列表（状态已更新）
python -m chat4code feature list
# 输出示例：
# ✅ #1 [applied] 添加用户登录功能
#    🏷️ 标签: auth, high-priority

# 5. 按状态查看功能需求
python -m chat4code feature list --view status

# 6. 按标签查看功能需求
python -m chat4code feature list --view tags

# 7. 按时间线查看功能需求
python -m chat4code feature list --view timeline

# 8. 搜索功能需求
python -m chat4code feature search "登录"
```

### 增量开发工作流
```bash
# 第一次导出
python -m chat4code export ./my_project v1.md

# 开发过程中只导出变更
python -m chat4code export ./my_project changes.md --incremental

# 应用AI建议
python -m chat4code apply ai_suggestions.md ./my_project --show-diff

# 记录到会话
python -m chat4code session log --task "实现用户功能" my_session
```

### 交互式开发工作流
```bash
# 启动交互式模式
python -m chat4code --interactive

chat4code> config set-type python  # 设置项目类型
chat4code> export ./my_project --task analyze  # 自动序列化文件名
chat4code> apply  # 自动使用最新的导入文件
chat4code> feature list  # 查看功能需求
chat4code> feature search "登录"  # 搜索功能需求
```

## 支持的文件类型

```bash
# 查看支持的文件扩展名
python -m chat4code --list-extensions
```

包括：`.cpp`, `.h`, `.cc`, `.hh`, `.py`, `.java`, `.js`, `.ts`, `.html`, `.css`, `.sql`, `.sh`, `.json`, `.xml`, `.yaml`, `.yml`, `.go`, `.rs`, `.swift` 等

## 最佳实践

### 1. 与版本控制集成
```bash
# 导出前提交
git add .
git commit -m "准备AI分析"

# 应用AI修改后提交
python -m chat4code apply response.md ./project
git add .
git commit -m "应用AI建议的修改"
```

### 2. 团队协作
```bash
# 为不同开发者创建会话
python -m chat4code session start developer1_task
python -m chat4code session start developer2_task

# 分别跟踪进度
python -m chat4code session log --task "前端开发" --desc "实现用户界面" developer1_task
```

### 3. 安全使用
- chat4code 会自动创建备份文件
- 支持路径安全检查，防止目录遍历攻击
- 可以通过配置文件自定义排除敏感文件

### 4. 功能需求管理最佳实践
```bash
# 1. 为功能需求添加标签
python -m chat4code export ./my_project --task add_feature --task-content "实现数据导出功能" --tags "data,high-priority"

# 2. 按状态跟踪功能需求
python -m chat4code feature list --view status

# 3. 直接编辑功能数据库（高级用法）
python -m chat4code feature edit
```

### 5. 项目类型管理
```bash
# 强制指定项目类型
python -m chat4code config set-type cpp

# 或在配置文件中指定
{
  "project_type": "python"
}
```

### 6. 自动化脚本
```bash
#!/bin/bash
# 自动化AI代码审查脚本

PROJECT_DIR="./my_project"
EXPORT_FILE="code_review_$(date +%Y%m%d_%H%M%S).md"

# 导出代码并请求代码审查
python -m chat4code export $PROJECT_DIR $EXPORT_FILE --task review

echo "✅ 代码已导出到: $EXPORT_FILE"
echo "📋 请将此文件发送给AI进行代码审查"
```

## 贡献

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系

项目链接: [https://github.com/chisuhua/chat4code](https://github.com/chisuhua/chat4code)
