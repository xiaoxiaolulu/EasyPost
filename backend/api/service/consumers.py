import json
import time
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import SuspiciousOperation
from unitrunner.engine.bomb import performance
from utils.logger import logger


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket connection closed with code {close_code}")

    async def receive(self, text_data): # noqa
        try:
            data = json.loads(text_data)
            target_ws_url = data.get('url')
            message = data.get('message')

            if not target_ws_url or not message:
                raise SuspiciousOperation("Invalid input data")

            async with websockets.connect(target_ws_url) as websocket:
                await websocket.send(message)
                response = await websocket.recv()
                await self.send(response)

        except Exception as e:
            print(f"Error forwarding message: {e}")
            await self.send(json.dumps({'error': str(e)}))

    async def receive_bytes(self, bytes_data):
        pass


class PerformanceConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket connection closed with code {close_code}")

    async def receive(self, text_data): # noqa
        try:
            data = json.loads(text_data)
            test_data = data.get('step')
            test_duration_secs = data.get('secs')
            concurrent_requests = data.get('concurrent_requests')
            increase_step = data.get('increase_step')
            increase_interval = data.get('increase_interval')

            if not test_data or not test_duration_secs or not concurrent_requests:
                raise SuspiciousOperation("Invalid input data")

            results = await performance(
                test_data=test_data,
                test_duration_secs=test_duration_secs,
                concurrent_requests=concurrent_requests,
                timeout_secs=15,
                cookie_store_enable=True,
                verbose=False,
                increase_step=increase_step,
                increase_interval=increase_interval
            )

            for item in results:
                if item.get("should_wait"):
                    time.sleep(0.1)
                else:
                    await self.send(str(item))

        except Exception as e:
            print(f"Error forwarding message: {e}")
            await self.send(json.dumps({'error': str(e)}))

    async def receive_bytes(self, bytes_data):
        pass
