"""
定时任务调度模块
管理微信消息的定时发送
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import pytz
import logging


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self, bot, template_manager):
        self.scheduler = BackgroundScheduler()
        self.bot = bot
        self.template_manager = template_manager
        self.timezone = pytz.timezone('Asia/Shanghai')
        self.logger = logging.getLogger(__name__)

        # 设置事件监听
        self.scheduler.add_listener(self._job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self._job_error, EVENT_JOB_ERROR)

    def add_weekly_task(self, group_name, template_name, day_of_week, hour, minute):
        """添加每周定时任务"""
        try:
            trigger = CronTrigger(
                day_of_week=day_of_week,  # 0-6 或 mon-sun
                hour=hour,
                minute=minute,
                timezone=self.timezone
            )

            self.scheduler.add_job(
                self._send_signup_message,
                trigger,
                args=[group_name, template_name],
                id=f"{group_name}_weekly",
                replace_existing=True
            )

            self.logger.info(f"已添加定时任务: {group_name} - {day_of_week} {hour}:{minute}")
            return True

        except Exception as e:
            self.logger.error(f"添加定时任务失败: {e}")
            return False

    def remove_task(self, group_name):
        """移除定时任务"""
        try:
            job_id = f"{group_name}_weekly"
            self.scheduler.remove_job(job_id)
            self.logger.info(f"已移除定时任务: {group_name}")
            return True
        except Exception as e:
            self.logger.error(f"移除定时任务失败: {e}")
            return False

    def _send_signup_message(self, group_name, template_name):
        """发送接龙消息"""
        try:
            message = self.template_manager.render_template(template_name)
            success = self.bot.send_group_message(group_name, message)

            if success:
                self.logger.info(f"成功发送接龙消息到: {group_name}")
            else:
                self.logger.error(f"发送接龙消息失败: {group_name}")

        except Exception as e:
            self.logger.error(f"发送接龙消息异常: {e}")

    def _job_executed(self, event):
        """任务执行成功回调"""
        self.logger.info(f"任务执行成功: {event.job_id}")

    def _job_error(self, event):
        """任务执行失败回调"""
        self.logger.error(f"任务执行失败: {event.job_id}, 异常: {event.exception}")

    def start(self):
        """启动调度器"""
        self.scheduler.start()
        self.logger.info("定时任务调度器已启动")

    def shutdown(self):
        """关闭调度器"""
        self.scheduler.shutdown()
        self.logger.info("定时任务调度器已关闭")