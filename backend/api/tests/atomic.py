import asyncio
import time
import atomic_bomb_engine
from atomic_bomb_engine import server
from unitrunner.engine.bomb import AtomicBombEngine


@server.ui(port=8880)
async def main():
    engine = AtomicBombEngine(
        test_duration_secs=10,
        concurrent_requests=1,
        timeout_secs=15,
        cookie_store_enable=True,
        verbose=False,
        increase_step=1,
        increase_interval=3
    )
    validators = [{
        "jsonpath": "$.msg",
        "reference_object": "操作成功"
    }]
    runner = engine.run(data={
        "name": "test-1",
        "url": "https://www.baidu.com/",
        "method": "POST",
        "form_data": {"name": "{{api-test-msg-1}}", "number": "{{api-test-num}}"},
        "validators": validators,
    })
    # runner = atomic_bomb_engine.BatchRunner()
    # step = getattr(atomic_bomb_engine, 'endpoint')
    # runner.run(
    #     test_duration_secs=10,
    #     concurrent_requests=1,
    #     step_option=atomic_bomb_engine.step_option(increase_step=1, increase_interval=3),
    #     timeout_secs=15,
    #     cookie_store_enable=True,
    #     verbose=False,
    #     api_endpoints=[
    #         step(
    #             name="test-1",
    #             url="https://www.baidu.com/",
    #             method="POST",
    #             form_data={"name": "{{api-test-msg-1}}", "number": "{{api-test-num}}"},
    #             weight=100,
    #             assert_options=[
    #                 atomic_bomb_engine.assert_option(jsonpath="$.msg", reference_object="操作成功"),
    #             ],
    #         ),
    #     ])
    return runner


if __name__ == '__main__':
    results = asyncio.run(main())
    a = []
    for res in results:
        if res.get("should_wait"):
            time.sleep(0.1)
        a.append(res)
        print(res)
    print(a)
