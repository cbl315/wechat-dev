"""
微信接龙机器人主程序
基于个人微信，直接在微信群聊中发送接龙消息
"""
import logging
import signal
import sys
from .core.personal_bot import PersonalWeChatBot
from .core.scheduler import TaskScheduler
from .managers.template_manager import TemplateManager
from .managers.config_manager import ConfigManager


class SignupBot:
    """微信接龙机器人主类"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # 初始化各个模块
        self.bot = PersonalWeChatBot()
        self.template_manager = TemplateManager()
        self.config_manager = ConfigManager()
        self.schedulers = []

        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def setup_logging(self):
        """配置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/wechat_bot.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def start(self):
        """启动机器人"""
        try:
            self.logger.info("开始启动微信接龙机器人...")

            # 登录个人微信
            if not self._login_wechat():
                self.logger.error("微信登录失败，程序退出")
                return

            # 从数据库加载配置并设置定时任务
            self._load_scheduled_tasks()

            self.logger.info("微信接龙机器人启动成功")
            self.logger.info("程序将在后台运行，按 Ctrl+C 退出")

            # 保持程序运行
            import time
            while True:
                time.sleep(60)

        except Exception as e:
            self.logger.error(f"启动失败: {e}")
            self.shutdown()

    def _login_wechat(self) -> bool:
        """登录个人微信"""
        try:
            self.logger.info("正在登录微信，请扫描二维码...")
            return self.bot.login()
        except Exception as e:
            self.logger.error(f"微信登录失败: {e}")
            return False

    def _load_scheduled_tasks(self):
        """从数据库加载定时任务"""
        try:
            active_groups = self.config_manager.get_all_active_groups()

            for group in active_groups:
                group_name = group['group_name']

                # 解析时间
                hour, minute = group['schedule_time'].split(':')

                # 创建调度器
                scheduler = TaskScheduler(self.bot, self.template_manager)

                # 添加定时任务
                scheduler.add_weekly_task(
                    group_name,
                    group['template_name'],
                    group['schedule_day'],
                    int(hour),
                    int(minute)
                )

                # 启动调度器
                scheduler.start()
                self.schedulers.append(scheduler)

            self.logger.info(f"已加载 {len(active_groups)} 个群组的定时任务")

        except Exception as e:
            self.logger.error(f"加载定时任务失败: {e}")

    def _signal_handler(self, signum, frame):
        """信号处理函数"""
        self.logger.info(f"收到信号 {signum}，正在关闭机器人...")
        self.shutdown()

    def shutdown(self):
        """关闭机器人"""
        self.logger.info("正在关闭微信接龙机器人...")

        # 关闭所有调度器
        for scheduler in self.schedulers:
            scheduler.stop()

        # 退出微信登录
        if self.bot.is_logged_in:
            self.bot.logout()

        self.logger.info("微信接龙机器人已关闭")
        sys.exit(0)


def main():
    """主函数"""
    bot = SignupBot()
    bot.start()


if __name__ == "__main__":
    main()