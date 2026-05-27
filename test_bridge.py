import asyncio
import json
import websockets

# Keep track of the active browser connection
connected_browser = None


async def handle_connection(websocket):
    """This function runs whenever Brave connects or sends a message."""
    global connected_browser
    connected_browser = websocket
    print("\n[Python] 🎉 Brave browser extension connected successfully!")

    try:
        # Keep the connection alive and listen for any replies from Brave
        async for message in websocket:
            data = json.loads(message)
            print(f"\n[Python] Received reply from Brave: {data}")

    except websockets.exceptions.ConnectionClosed:
        print("\n[Python] 🔌 Brave browser disconnected.")
    finally:
        connected_browser = None


async def send_command():
    """This loop lets you type keywords into the terminal to test tab switching."""
    global connected_browser
    while True:
        # Give the async loop a moment to breathe
        await asyncio.sleep(0.1)

        if connected_browser is not None:
            # Get input from you in the terminal
            keyword = input(
                "\nEnter a website keyword to switch to (e.g., youtube): "
            )

            if keyword.strip():
                # Format the command into JSON for the extension
                payload = {"action": "switch_tab", "keyword": keyword}

                print(f"[Python] Sending command to Brave: {payload}")
                await connected_browser.send(json.dumps(payload))
        else:
            # If the browser isn't connected yet, wait quietly
            await asyncio.sleep(1)


async def main():
    print("[Python] Starting local server on ws://localhost:8765...")
    # Start the WebSocket server
    server = await websockets.serve(handle_connection, "localhost", 8765)

    # Run both the server loop and your terminal input loop together
    await asyncio.gather(server.wait_closed(), send_command())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Python] Server stopped.")