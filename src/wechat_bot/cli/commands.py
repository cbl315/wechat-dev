"""
微信接龙机器人配置管理工具
支持个人微信机器人配置
"""
import argparse
import sys
from ..managers.config_manager import ConfigManager
from ..managers.template_manager import TemplateManager


class ConfigManagerCLI:
    """配置管理命令行工具"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()

    def add_group(self, args):
        """添加群组配置"""
        success = self.config_manager.add_group_config(
            args.group_name,
            args.template_name,
            args.day,
            args.time
        )
        if success:
            print(f"成功添加群组配置: {args.group_name}")
        else:
            print(f"添加群组配置失败: {args.group_name}")

    def list_groups(self, args):
        """列出所有群组配置"""
        groups = self.config_manager.get_all_active_groups()
        if groups:
            print("当前活跃群组配置:")
            for group in groups:
                print(f"  - {group['group_name']}: 模板={group['template_name']}, 时间=周{group['schedule_day']+1} {group['schedule_time']}")
        else:
            print("当前没有活跃的群组配置")

    def deactivate_group(self, args):
        """停用群组配置"""
        success = self.config_manager.deactivate_group(args.group_name)
        if success:
            print(f"成功停用群组配置: {args.group_name}")
        else:
            print(f"停用群组配置失败: {args.group_name}")

    def add_template(self, args):
        """添加模板"""
        template_content = input("请输入模板内容: ")
        default_vars = {}

        # 询问默认变量值
        time = input("活动时间 (默认 19:00-21:00): ") or "19:00-21:00"
        location = input("活动地点 (默认 XX羽毛球馆): ") or "XX羽毛球馆"
        price = input("活动费用 (默认 30元/人): ") or "30元/人"
        note = input("备注信息 (可选): ") or ""

        default_vars = {
            'time': time,
            'location': location,
            'price': price,
            'note': note
        }

        self.template_manager.add_template(args.template_name, template_content, default_vars)
        print(f"成功添加模板: {args.template_name}")

    def list_templates(self, args):
        """列出所有模板"""
        templates = self.template_manager.get_all_templates()
        if templates:
            print("当前可用模板:")
            for name, template in templates.items():
                print(f"  - {name}: {template['content'][:50]}...")
        else:
            print("当前没有可用的模板")

    def main(self):
        """主函数"""
        parser = argparse.ArgumentParser(description='微信接龙机器人配置管理工具')
        subparsers = parser.add_subparsers(dest='command', help='可用命令')

        # 添加群组配置命令
        add_group_parser = subparsers.add_parser('add-group', help='添加群组配置')
        add_group_parser.add_argument('group_name', help='群组名称')
        add_group_parser.add_argument('template_name', help='模板名称')
        add_group_parser.add_argument('day', type=int, help='星期几 (0-6，0=周一)')
        add_group_parser.add_argument('time', help='发送时间 (HH:MM)')
        add_group_parser.set_defaults(func=self.add_group)

        # 列出群组配置命令
        list_groups_parser = subparsers.add_parser('list-groups', help='列出所有群组配置')
        list_groups_parser.set_defaults(func=self.list_groups)

        # 停用群组配置命令
        deactivate_group_parser = subparsers.add_parser('deactivate-group', help='停用群组配置')
        deactivate_group_parser.add_argument('group_name', help='群组名称')
        deactivate_group_parser.set_defaults(func=self.deactivate_group)

        # 添加模板命令
        add_template_parser = subparsers.add_parser('add-template', help='添加模板')
        add_template_parser.add_argument('template_name', help='模板名称')
        add_template_parser.set_defaults(func=self.add_template)

        # 列出模板命令
        list_templates_parser = subparsers.add_parser('list-templates', help='列出所有模板')
        list_templates_parser.set_defaults(func=self.list_templates)

        args = parser.parse_args()

        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()


def main():
    """主函数"""
    cli = ConfigManagerCLI()
    cli.main()


if __name__ == "__main__":
    main()