"""
微信机器人核心模块
处理微信登录、消息发送和连接管理
"""
import itchat
from itchat.content import TEXT
import logging


class WechatBot:
    """微信机器人核心类"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scheduler = None

    def login(self):
        """微信登录"""
        try:
            itchat.auto_login(
                hotReload=True,
                enableCmdQR=2,
                statusStorageDir='itchat.pkl'
            )
            self.logger.info("微信登录成功")
        except Exception as e:
            self.logger.error(f"微信登录失败: {e}")
            raise

    def send_group_message(self, group_name, message):
        """发送群消息"""
        try:
            groups = itchat.search_chatrooms(name=group_name)
            if groups:
                groups[0].send(message)
                self.logger.info(f"成功发送消息到群组: {group_name}")
                return True
            else:
                self.logger.warning(f"未找到群组: {group_name}")
                return False
        except Exception as e:
            self.logger.error(f"发送消息失败: {e}")
            return False

    def start_listening(self):
        """启动消息监听"""
        try:
            itchat.run()
        except KeyboardInterrupt:
            self.logger.info("程序被用户中断")
        except Exception as e:
            self.logger.error(f"消息监听异常: {e}")