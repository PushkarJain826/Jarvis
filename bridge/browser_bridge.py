import asyncio
import json
import websockets

connected_extension = None
bridge_loop = None
response_queue = None  # ← queue for extension responses

async def _handler(websocket):
    global connected_extension, response_queue
    connected_extension = websocket
    response_queue = asyncio.Queue()
    print("[Jarvis Bridge] Brave extension connected.")

    async for message in websocket:
        data = json.loads(message)

        # Handle heartbeat
        if data.get("type") == "ping":
            await websocket.send(json.dumps({"type": "pong"}))
            continue

        # Put all other responses into queue for tools to read
        await response_queue.put(data)

    # Extension disconnected
    connected_extension = None
    response_queue = None
    print("[Jarvis Bridge] Extension disconnected.")

async def start_bridge():
    global bridge_loop
    bridge_loop = asyncio.get_event_loop()
    async with websockets.serve(_handler, "127.0.0.1", 8765):
        print("[Jarvis Bridge] Server running on ws://127.0.0.1:8765")
        await asyncio.Future()