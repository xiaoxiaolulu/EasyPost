import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

host = 'localhost'
port = 8889

app = FastAPI()

# 初始化测试界面
html = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html">
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
<!--            <input type="text" id="messageText" autocomplete="off"/>-->
            <textarea rows="5" id="messageText"></textarea>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://%s:%s/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>""" % (host, port)


# 请求初始页面
@app.get("/")
async def get():
    return HTMLResponse(html)


# websocket接口
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    while True:
        data = await websocket.receive_text()
        i = i + 1
        await websocket.send_text(f" This is {i} recept, Message text was: {data}")


if __name__ == '__main__':
    uvicorn.run('websocket:app', host=host, port=port, reload=True, workers=1)
