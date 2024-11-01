import asyncio

from atomic_bomb_engine import atomic_bomb_engine


async def batch_async():
  runner = atomic_bomb_engine.BatchRunner()
  runner.run(
    test_duration_secs=30,
    concurrent_requests=30,
    step_option=atomic_bomb_engine.step_option(increase_step=3, increase_interval=3),
    timeout_secs=0,
    cookie_store_enable=True,
    verbose=False,
    api_endpoints=[
      atomic_bomb_engine.endpoint(
        name="test-1",
        url="https://www.baidu.com/",
        method="POST",
        json={"name": "test-1", "number": 1},
        weight=100,
        assert_options=[
          atomic_bomb_engine.assert_option(jsonpath="$.message", reference_object="操作成功"),
        ],
      ),
    ])
  return runner


async def main():
  results = await batch_async()
  for res in results:
    print(res)

if __name__ == '__main__':
  asyncio.run(main())