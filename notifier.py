import time
import requests

from config import get_notifier_api_key
from logger import Logger


class Notifier:
    REFRESH_FAILURE_REPORT_TIME = 180

    def __init__(self):
        self.name = "Notifier"
        self.status = "off"
        self.log = Logger(self.name)

        self.username = None
        self.last_reported_refresh_time = -1

    def _do_notif(self, msg):
        print(msg, self.status)
        if self.status == "on":
            try:
                res = requests.get(
                    f"https://sctapi.ftqq.com/{get_notifier_api_key()}.send?title={msg}"
                )
                res.raise_for_status()
            except Exception as e:
                print(e)
                self.log("error", f"notif error: {type(e)} {str(e)}")

    def report_success_choice(self, course_name):
        self.log("success", f"REPORTING success choice: {course_name}")
        self._do_notif(f"选课成功：{course_name}")

    def report_failed_choice(self, course_name, reason):
        self.log("warning", f"failed choice: {course_name}, {reason}")
        self._do_notif(f"选课失败：{course_name}（{reason}）")

    def report_refresh_failure(self, last_succ_time):
        self.log("debug", f"refresh failed since {last_succ_time}")
        if last_succ_time == self.last_reported_refresh_time:  # already reported
            return

        if time.time() - last_succ_time > self.REFRESH_FAILURE_REPORT_TIME:
            self.last_reported_refresh_time = last_succ_time
            self.log("warning", f"refresh failed since {last_succ_time}")
            self._do_notif(f"从 {last_succ_time} 以后刷新失败")

    def report_bot_fatal(self, n_bot_left):
        self.log("warning", f"bot fatal error, # left = {n_bot_left}")
        self._do_notif(f"Bot 失效，剩余数量 {n_bot_left}")

    def report_startup(self):
        self.log("info", "startup")
        self._do_notif("服务已启动")


if __name__ == "__main__":
    notifier = Notifier()
    notifier.status = "on"
    notifier.report_success_choice("test course")
    notifier.report_failed_choice("test course", "test reason")
    notifier.report_refresh_failure(123)
    notifier.report_bot_fatal(123)
    notifier.report_startup()

    exit()
