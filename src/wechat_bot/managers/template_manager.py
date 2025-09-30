"""
模板管理模块
管理消息模板和变量替换
"""
import json
import os
from datetime import datetime
import logging


class TemplateManager:
    """模板管理器"""

    def __init__(self, config_file='config/templates.json'):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.templates = self._load_templates()

    def _load_templates(self):
        """加载模板配置"""
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 创建默认模板配置
                default_templates = {
                    "default": {
                        "template": "【羽毛球活动报名】\n时间：{{date}} {{weekday}} {{time}}\n地点：{{location}}\n费用：{{price}}\n\n报名接龙：\n1. \n2. \n3. ",
                        "variables": {
                            "time": "19:00-21:00",
                            "location": "XX羽毛球馆",
                            "price": "30元/人"
                        }
                    }
                }
                self._save_templates(default_templates)
                return default_templates

        except Exception as e:
            self.logger.error(f"加载模板配置失败: {e}")
            return {}

    def _save_templates(self, templates):
        """保存模板配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(templates, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存模板配置失败: {e}")

    def get_template(self, template_name):
        """获取模板配置"""
        return self.templates.get(template_name)

    def add_template(self, template_name, template_content, variables=None):
        """添加新模板"""
        if variables is None:
            variables = {}

        self.templates[template_name] = {
            "template": template_content,
            "variables": variables
        }
        self._save_templates(self.templates)
        self.logger.info(f"已添加模板: {template_name}")

    def render_template(self, template_name, extra_variables=None):
        """渲染模板"""
        try:
            template_config = self.get_template(template_name)
            if not template_config:
                self.logger.error(f"模板不存在: {template_name}")
                return ""

            template = template_config["template"]
            variables = template_config.get("variables", {})

            # 合并变量
            if extra_variables:
                variables.update(extra_variables)

            # 添加系统变量
            system_vars = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'weekday': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][datetime.now().weekday()],
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
            variables.update(system_vars)

            # 模板渲染
            rendered = template
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                rendered = rendered.replace(placeholder, str(value))

            return rendered

        except Exception as e:
            self.logger.error(f"模板渲染失败: {e}")
            return ""