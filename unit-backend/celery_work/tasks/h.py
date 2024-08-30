import asyncio
from celery_work.worker import celery


@celery.task
async def send(a, b):
    # 具体要执行的任务
    print("开始")
    print(a, b)
    await asyncio.sleep(4)
    print("结束")
    return 1
