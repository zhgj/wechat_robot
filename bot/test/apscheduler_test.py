from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    # BlockingScheduler
    scheduler = BlockingScheduler()
    # date: 特定的时间点触发
    # interval: 固定时间间隔触发
    # cron: 在特定时间周期性地触发
    scheduler.add_job(job, "cron", hour=15, minute=28)
    # scheduler.add_job(job, 'interval', seconds=1)
    scheduler.start()
