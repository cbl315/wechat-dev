"""
配置管理模块
支持个人微信机器人配置
"""
import sqlite3
import json
import logging
from typing import Dict, List, Optional


class ConfigManager:
    """配置管理器 - 支持个人微信机器人"""

    def __init__(self, db_file='data/wechat_bot.db'):
        self.db_file = db_file
        self.logger = logging.getLogger(__name__)
        self._init_database()

    def _init_database(self):
        """初始化数据库"""
        try:
            # 确保数据目录存在
            import os
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)

            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            # 创建群组配置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS group_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT UNIQUE NOT NULL,
                    template_name TEXT NOT NULL,
                    schedule_day INTEGER NOT NULL,  -- 0-6 代表周一到周日
                    schedule_time TEXT NOT NULL,    -- HH:MM 格式
                    is_active BOOLEAN DEFAULT 1,
                    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建发送记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS send_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL,
                    message_content TEXT,
                    send_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT 1
                )
            ''')

            conn.commit()
            conn.close()
            self.logger.info("数据库初始化完成")

        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
            raise

    def add_group_config(self, group_name: str, template_name: str,
                        schedule_day: int, schedule_time: str) -> bool:
        """添加群组配置"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO group_configs
                (group_name, template_name, schedule_day, schedule_time, is_active)
                VALUES (?, ?, ?, ?, 1)
            ''', (group_name, template_name, schedule_day, schedule_time))

            conn.commit()
            conn.close()
            self.logger.info(f"已添加群组配置: {group_name}")
            return True

        except Exception as e:
            self.logger.error(f"添加群组配置失败: {e}")
            return False

    def get_all_active_groups(self) -> List[Dict]:
        """获取所有活跃的群组配置"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT group_name, template_name, schedule_day, schedule_time
                FROM group_configs
                WHERE is_active = 1
                ORDER BY schedule_day, schedule_time
            ''')

            groups = []
            for row in cursor.fetchall():
                groups.append({
                    'group_name': row[0],
                    'template_name': row[1],
                    'schedule_day': row[2],
                    'schedule_time': row[3]
                })

            conn.close()
            return groups

        except Exception as e:
            self.logger.error(f"获取群组配置失败: {e}")
            return []

    def deactivate_group(self, group_name: str) -> bool:
        """停用群组配置"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE group_configs
                SET is_active = 0
                WHERE group_name = ?
            ''', (group_name,))

            conn.commit()
            conn.close()
            self.logger.info(f"已停用群组配置: {group_name}")
            return True

        except Exception as e:
            self.logger.error(f"停用群组配置失败: {e}")
            return False

    def add_send_record(self, group_name: str, message_content: str, success: bool = True):
        """添加发送记录"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO send_records (group_name, message_content, success)
                VALUES (?, ?, ?)
            ''', (group_name, message_content, success))

            conn.commit()
            conn.close()

        except Exception as e:
            self.logger.error(f"添加发送记录失败: {e}")