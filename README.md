# 微信接龙机器人

一个基于 Python 的微信机器人，用于在微信群聊中根据模板定时发送接龙消息，主要用于羽毛球活动报名。

## 快速开始

欢迎使用微信接龙机器人项目！本指南将帮助您快速搭建开发环境并运行代码。

### 第一步：安装 uv

uv 是一个快速的 Python 包管理器，请先安装它：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装完成后重启终端。

### 第二步：设置项目环境

```bash
# 克隆项目后，进入项目目录
cd wechat-dev

# 安装所有依赖
uv sync

# 激活虚拟环境
source .venv/bin/activate
```

### 第三步：测试运行

运行测试代码验证环境是否正常：

```bash
uv run python tests/test_bot.py
```

您应该看到系统测试的输出，包括模板渲染和配置管理的测试结果。

### 第四步：使用微信接龙机器人

项目已经实现了完整的微信接龙机器人功能，采用标准的 Python 包结构组织代码。

### 项目结构

```
wechat-dev/
├── src/wechat_bot/          # 主包目录
│   ├── core/                # 核心模块
│   │   ├── personal_bot.py         # 个人微信机器人核心
│   │   └── scheduler.py     # 定时任务调度器
│   ├── managers/            # 管理器模块
│   │   ├── config_manager.py     # 配置管理器
│   │   └── template_manager.py   # 模板管理器
│   ├── cli/                 # 命令行接口
│   │   └── commands.py      # CLI 配置管理命令
│   ├── __init__.py          # 包初始化
│   └── main.py              # 主程序入口
├── scripts/                 # 可执行脚本
│   ├── run_bot.py          # 启动机器人脚本
│   └── config_cli.py       # 配置管理脚本
├── tests/                   # 测试目录
│   └── test_bot.py         # 系统测试
├── config/                  # 配置文件
├── data/                    # 数据文件
├── logs/                    # 日志文件
└── docs/                    # 文档
```

### 使用方法

本项目基于**个人微信**，直接在微信群聊中发送接龙消息。

#### 基本使用

1. **安装包**（开发模式）：
   ```bash
   uv sync
   ```

2. **测试系统功能**：
   ```bash
   uv run python tests/test_bot.py
   ```

#### 配置管理

3. **添加群组配置**：
   ```bash
   # 添加微信群组配置
   uv run python scripts/config_cli.py add-group "羽毛球群" default 4 "20:00"
   ```

4. **添加模板**：
   ```bash
   # 添加模板
   uv run python scripts/config_cli.py add-template my_template
   ```

5. **查看配置**：
   ```bash
   # 列出所有群组配置
   uv run python scripts/config_cli.py list-groups

   # 列出所有模板
   uv run python scripts/config_cli.py list-templates
   ```

#### 启动机器人

6. **启动机器人**：
   ```bash
   uv run python scripts/run_bot.py
   ```

   首次运行时会显示微信登录二维码，请用手机微信扫描二维码登录。

### 配置说明

- **群组配置**：每个群组可以设置不同的模板和发送时间
- **模板变量**：支持 `{{date}}`、`{{weekday}}`、`{{time}}`、`{{location}}`、`{{price}}` 等变量
- **定时任务**：支持每周固定时间发送，使用 cron 表达式



### 注意事项

- **个人微信版本**：直接在微信群聊中发送消息，用户体验好
- **封号风险**：存在一定的封号风险，建议小范围使用
- **扫码登录**：首次运行需要扫码登录微信
- **稳定性**：相比公众号版本稳定性较差
- **适用场景**：小范围测试、内部使用、非商业用途

开始使用您的微信接龙机器人！

## 常用命令

```bash
# 运行代码
uv run python your_script.py

# 添加新依赖
uv add package_name

# 更新依赖
uv sync

# 查看已安装包
uv list
```

## 项目文档

- [技术方案文档](docs/微信接龙机器人技术方案.md) - 详细的项目设计和实现方案

## 故障排除

**遇到问题？**
- 确保 uv 已正确安装：`which uv`
- 检查 Python 版本：`python --version`
- 重新同步依赖：`uv sync`