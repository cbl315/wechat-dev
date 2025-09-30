#!/usr/bin/env python3
"""
微信接龙机器人配置管理工具
基于微信公众号API
"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from wechat_bot.cli.commands import main

if __name__ == "__main__":
    main()