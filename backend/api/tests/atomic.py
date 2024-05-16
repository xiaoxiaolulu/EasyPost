import asyncio
import time
import atomic_bomb_engine


async def main():
    runner = atomic_bomb_engine.BatchRunner()
    runner.run(
        test_duration_secs=1,
        concurrent_requests=1,
        # step_option=atomic_bomb_engine.step_option(increase_step=3, increase_interval=3),
        timeout_secs=15,
        cookie_store_enable=True,
        verbose=False,
        api_endpoints=[
            atomic_bomb_engine.endpoint(
                name="test-1",
                url="https://www.baidu.com/",
                method="get",
                weight=100,
                # assert_options=[
                #     atomic_bomb_engine.assert_option(jsonpath="$.msg", reference_object="操作成功"),
                # ],
            ),
        ])
    return runner


if __name__ == '__main__':
    results = asyncio.run(main())
    for res in results:
        if res.get("should_wait"):
            time.sleep(0.1)
        print(res)
