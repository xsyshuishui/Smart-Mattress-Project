# server.py  —— 适配 websockets ≥ 12 / Python 3.12
import asyncio
import json
import re
from pathlib import Path

import websockets
from websockets.exceptions import ConnectionClosed

DATA_FILE = Path(__file__).with_name("json.txt")
HOST = "127.0.0.1"   # 若需跨系统/跨设备访问，可改为 "0.0.0.0"
PORT = 8000
SEND_INTERVAL = 1.5  # 秒

def load_data(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    # 提取每个 {...} JSON 对象
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)
    return [json.loads(m) for m in matches]

FRAMES = load_data(DATA_FILE)

async def send_frames(websocket):
    """循环发送帧；到末尾后从头继续。"""
    i = 0
    while True:
        frame = FRAMES[i % len(FRAMES)]
        await websocket.send(json.dumps(frame))
        i += 1
        await asyncio.sleep(SEND_INTERVAL)

async def receive_commands(websocket):
    """接收前端命令，仅打印日志（必要时可在此落库/转发到硬件）。"""
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print(f"[RX] 非 JSON：{message!r}")
            continue
        print(f"[RX] 命令：{data}")

async def websocket_handler(websocket):
    """新版 websockets 的处理函数只接受一个参数：websocket。"""
    print("[WS] client connected")
    send_task = asyncio.create_task(send_frames(websocket))
    recv_task = asyncio.create_task(receive_commands(websocket))
    try:
        done, pending = await asyncio.wait(
            {send_task, recv_task}, return_when=asyncio.FIRST_EXCEPTION
        )
        for t in done:
            # 触发异常时打印出来
            exc = t.exception()
            if exc:
                raise exc
    except ConnectionClosed:
        print("[WS] client disconnected")
    finally:
        send_task.cancel()
        recv_task.cancel()
        with contextlib.suppress(Exception):
            await asyncio.gather(send_task, recv_task)

async def main():
    async with websockets.serve(websocket_handler, HOST, PORT):
        print(f"[WS] server listening on ws://{HOST}:{PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    import contextlib
    asyncio.run(main())
