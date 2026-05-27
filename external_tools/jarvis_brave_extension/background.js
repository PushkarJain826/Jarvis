const SERVER_URL = "ws://127.0.0.1:8765";
let socket = null;
let heartbeatInterval = null; // Tracks our anti-sleep timer

function connectToJarvis() {
    console.log("[Jarvis Extension] Attempting to connect to Python Backend...");
    socket = new WebSocket(SERVER_URL);

    socket.onopen = () => {
        console.log("[Jarvis Extension] 🎉 Connected to Python Backend!");
        
        // Start the Heartbeat Loop the exact second we connect
        startHeartbeat();
    };

    socket.onclose = () => {
        console.log("[Jarvis Extension] 🔌 Disconnected. Retrying connection in 3 seconds...");
        
        // Stop the heartbeat timer if the connection drops out
        stopHeartbeat();
        
        setTimeout(() => {
            connectToJarvis();
        }, 3000);
    };

    socket.onerror = (error) => {
        // Suppress terminal logs when Python is shut down
    };

    socket.onmessage = async (event) => {
        try {
            const data = JSON.parse(event.data);
            
            // Ignore incoming ping acknowledgments
            if (data.type === "pong") return;

            if (data.action === "switch_tab") {
                const targetKeyword = data.keyword.toLowerCase().split('.')[0].trim();
                
                chrome.tabs.query({}, (tabs) => {
                    let foundTab = null;
                    for (let tab of tabs) {
                        const urlMatch = tab.url && tab.url.toLowerCase().includes(targetKeyword);
                        const titleMatch = tab.title && tab.title.toLowerCase().includes(targetKeyword);
                        if (urlMatch || titleMatch) {
                            foundTab = tab;
                            break;
                        }
                    }
                    
                    if (foundTab) {
                        chrome.windows.update(foundTab.windowId, { focused: true });
                        chrome.tabs.update(foundTab.id, { active: true });
                        socket.send(JSON.stringify({ status: "success", keyword: data.keyword }));
                    } else {
                        socket.send(JSON.stringify({ status: "not_found", keyword: data.keyword }));
                    }
                });
            }
            else if (data.action === "open_tab") {
                chrome.tabs.create({ url: data.url });
                socket.send(JSON.stringify({ status: "opened", url: data.url }));
            }
        } catch (error) {
            console.error("[Jarvis Extension] Error processing message:", error);
        }
    };
}

// --- ANTI-HIBERNATION HEARTBEAT FUNCTIONS ---
function startHeartbeat() {
    // Send a pulse every 5 seconds to keep the background process awake
    heartbeatInterval = setInterval(() => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ type: "ping" }));
        }
    }, 5000);
}

function stopHeartbeat() {
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
        heartbeatInterval = null;
    }
}

// Kick off the script
connectToJarvis();