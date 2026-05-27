import webbrowser
import json
import asyncio
from bridge import browser_bridge

def open_browser(url: str, keyword: str, force_new: bool = False):
    ext = browser_bridge.connected_extension

    if ext:
        async def _send_command():
            if force_new:
                # Tell extension to open new tab directly
                await ext.send(json.dumps({
                    "action": "open_tab",
                    "url": url
                }))
            else:
                # Ask extension to switch to existing tab
                await ext.send(json.dumps({
                    "action": "switch_tab",
                    "keyword": keyword
                }))

            try:
                while True:
                    data = await asyncio.wait_for(
                        browser_bridge.response_queue.get(),
                        timeout=3.0
                    )
                    print(f"[DEBUG] Extension response: {data}")
                    return data

            except asyncio.TimeoutError:
                print("[DEBUG] Timed out waiting for extension response")
                return None

        try:
            future = asyncio.run_coroutine_threadsafe(
                _send_command(), browser_bridge.bridge_loop
            )
            result = future.result(timeout=5.0)

            if result and result.get("status") == "success":
                print(f"[Jarvis] Switched to existing tab → {keyword}")
                return

            if result and result.get("status") == "opened":
                print(f"[Jarvis] Opened new tab via extension → {url}")
                return

            # Tab not found via extension, fallback
            print(f"[Jarvis] Tab not found, opening new tab → {url}")

        except Exception as e:
            print(f"[Jarvis Bridge] Failed: {e}")

    # Fallback if extension not connected
    webbrowser.open_new_tab(url)
    print(f"[Jarvis] Opened new tab → {url}")