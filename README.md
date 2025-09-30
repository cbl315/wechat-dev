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

运行示例代码验证环境是否正常：

```bash
uv run python hello.py
```

您应该看到输出：
```
Hello from wechat-dev!
```

### 第四步：开发微信机器人

项目已经配置了以下核心依赖：
- `itchat` - 微信个人号 API
- `apscheduler` - 定时任务调度
- `jinja2` - 模板引擎

开始开发您的微信接龙机器人！

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