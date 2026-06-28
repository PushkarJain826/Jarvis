const SERVER_URL = "ws://127.0.0.1:8765";
let socket = null;

function connect() {
    socket = new WebSocket(SERVER_URL);

    socket.onopen = () => {
        console.log("[Jarvis Offscreen] Connected to Python backend.");
    };

    socket.onclose = () => {
        console.log("[Jarvis Offscreen] Disconnected. Retrying in 3s...");
        setTimeout(connect, 3000);
    };

    socket.onerror = () => {};

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "pong") return;

        // Forward incoming commands to background for tab handling
        chrome.runtime.sendMessage({
            target: "background",
            payload: data
        });
    };
}

// Listen for responses from background to send back to Python
chrome.runtime.onMessage.addListener((message) => {
    if (message.target !== "offscreen") return;
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message.payload));
    }
});

connect();