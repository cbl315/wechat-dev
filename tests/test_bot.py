"""
测试微信接龙机器人
这个脚本用于测试机器人功能，不会实际发送微信消息
"""

import sys
import os
import logging

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from wechat_bot.managers.template_manager import TemplateManager
from wechat_bot.managers.config_manager import ConfigManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def test_template_manager():
    """测试模板管理器"""
    print("\n=== 测试模板管理器 ===")
    tm = TemplateManager()

    # 测试渲染默认模板
    message = tm.render_template("default")
    print("默认模板渲染结果:")
    print(message)

    # 测试添加新模板
    test_template = "【测试活动】\n时间：{{date}} {{weekday}} {{time}}\n地点：{{location}}\n备注：{{note}}\n\n报名接龙：\n1. \n2. \n3. "
    tm.add_template("test", test_template, {
        "time": "20:00-22:00",
        "location": "测试场馆",
        "note": "这是一个测试活动"
    })

    # 测试渲染新模板
    test_message = tm.render_template("test")
    print("\n测试模板渲染结果:")
    print(test_message)


def test_config_manager():
    """测试配置管理器"""
    print("\n=== 测试配置管理器 ===")
    cm = ConfigManager()

    # 测试添加群组配置
    success = cm.add_group_config(
        "测试群组",
        "default",
        4,
        "20:00"
    )
    print(f"添加群组配置: {'成功' if success else '失败'}")

    # 测试获取群组配置
    groups = cm.get_all_active_groups()
    print(f"当前活跃群组数量: {len(groups)}")
    for group in groups:
        print(f"  - {group['group_name']}: 模板={group['template_name']}, 时间=周{group['schedule_day']+1} {group['schedule_time']}")


def main():
    """主测试函数"""
    print("开始测试微信接龙机器人...")

    test_template_manager()
    test_config_manager()

    print("\n=== 测试完成 ===")
    print("所有模块测试完成，可以运行主程序启动机器人")


if __name__ == "__main__":
    main()