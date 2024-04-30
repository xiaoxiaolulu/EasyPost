import json
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import SuspiciousOperation
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
