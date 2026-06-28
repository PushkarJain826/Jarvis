// ── OFFSCREEN SETUP ───────────────────────────────────────
async function setupOffscreen() {
    const existing = await chrome.offscreen.hasDocument();
    if (!existing) {
        await chrome.offscreen.createDocument({
            url: "offscreen.html",
            reasons: ["BLOBS"],
            justification: "Maintain WebSocket connection to Jarvis Python backend"
        });
    }
}

setupOffscreen();

chrome.alarms.create("jarvis_keepalive", { periodInMinutes: 0.4 });
chrome.alarms.onAlarm.addListener((alarm) => {
    if (alarm.name === "jarvis_keepalive") setupOffscreen();
});

// ── TAB COMMANDS ──────────────────────────────────────────
chrome.runtime.onMessage.addListener((message) => {
    if (message.target !== "background") return;

    const data = message.payload;

    if (data.action === "switch_tab") {
        const keyword = data.keyword.toLowerCase().split('.')[0].trim();

        chrome.tabs.query({}, (tabs) => {
            let foundTab = null;
            for (let tab of tabs) {
                const urlMatch = tab.url && tab.url.toLowerCase().includes(keyword);
                const titleMatch = tab.title && tab.title.toLowerCase().includes(keyword);
                if (urlMatch || titleMatch) {
                    foundTab = tab;
                    break;
                }
            }

            if (foundTab) {
                chrome.windows.update(foundTab.windowId, { focused: true });
                chrome.tabs.update(foundTab.id, { active: true });
                chrome.runtime.sendMessage({
                    target: "offscreen",
                    payload: { status: "success", keyword: data.keyword }
                });
            } else {
                chrome.runtime.sendMessage({
                    target: "offscreen",
                    payload: { status: "not_found", keyword: data.keyword }
                });
            }
        });
    }

    else if (data.action === "open_tab") {
        chrome.tabs.create({ url: data.url });
        chrome.runtime.sendMessage({
            target: "offscreen",
            payload: { status: "opened", url: data.url }
        });
    }

    else if (data.action === "open_window") {
        // Open URL in a completely new browser window
        chrome.windows.create({ url: data.url }, (window) => {
            chrome.runtime.sendMessage({
                target: "offscreen",
                payload: { status: "window_opened", url: data.url, windowId: window.id }
            });
        });
    }
});