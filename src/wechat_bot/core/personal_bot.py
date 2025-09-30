"""
个人微信机器人
使用 itchat 库实现微信群聊消息发送
"""
import itchat
import logging
from typing import Dict, List, Optional


class PersonalWeChatBot:
    """个人微信机器人"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_logged_in = False

    def login(self) -> bool:
        """登录微信"""
        try:
            self.logger.info("正在登录微信...")
            itchat.auto_login(hotReload=True, enableCmdQR=2)
            self.is_logged_in = True
            self.logger.info("微信登录成功")
            return True
        except Exception as e:
            self.logger.error(f"微信登录失败: {e}")
            return False

    def send_message_to_group(self, group_name: str, message: str) -> bool:
        """发送消息到微信群"""
        if not self.is_logged_in:
            self.logger.error("请先登录微信")
            return False

        try:
            # 搜索群聊
            groups = itchat.search_chatrooms(name=group_name)
            if not groups:
                self.logger.error(f"未找到群聊: {group_name}")
                return False

            # 获取第一个匹配的群聊
            group = groups[0]

            # 发送消息
            itchat.send_msg(message, group['UserName'])
            self.logger.info(f"已发送消息到群聊: {group_name}")
            return True

        except Exception as e:
            self.logger.error(f"发送消息失败: {e}")
            return False

    def get_group_list(self) -> List[Dict]:
        """获取群聊列表"""
        if not self.is_logged_in:
            return []

        try:
            groups = itchat.get_chatrooms()
            return [
                {
                    'name': group['NickName'],
                    'user_name': group['UserName'],
                    'member_count': group.get('MemberCount', 0)
                }
                for group in groups
            ]
        except Exception as e:
            self.logger.error(f"获取群聊列表失败: {e}")
            return []

    def logout(self):
        """退出登录"""
        if self.is_logged_in:
            itchat.logout()
            self.is_logged_in = False
            self.logger.info("已退出微信登录")