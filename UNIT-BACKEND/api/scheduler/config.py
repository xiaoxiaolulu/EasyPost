from api.scheduler.sqlalchemy_store import SQLAlchemyJobStore
from config.settings import DATABASES as DB


config = {
    'apscheduler.jobstores': {
        'default': SQLAlchemyJobStore(
            url=f'mysql://{DB["default"]["USER"]}:'
                f'{DB["default"]["PASSWORD"]}@'
                f'{DB["default"]["HOST"]}:'
                f'{DB["default"]["PORT"]}/'
                f'{DB["default"]["NAME"]}?charset=utf8'
        )},
    # 执行器配置 使用线程池执行器，最大10个线程
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '10'
    },
    # Job配置，为新任务关闭合并模式
    'apscheduler.job_defaults.coalesce': 'false',
    # Job配置，同一个任务同一时间最多只能有3个实例在运行
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'Asia/Shanghai',
}
