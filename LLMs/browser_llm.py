from groq import Groq
from tools.browser_tools import open_browser
import os
import json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def extract_keyword(url):
    try:
        domain = url.split("//")[-1]
        domain = domain.split("/")[0]
        domain = domain.replace("www.", "")
        keyword = domain.split(".")[0]
        return keyword
    except:
        return url

def browser_agent(user_command):

    if not user_command or len(user_command.strip()) < 3:
        print("[Jarvis] Command too short or empty, ignoring.")
        return False

    prompt = f"""
    Analyze the user's command and return a JSON object.

    Rules:
    - Return ONLY valid JSON, nothing else
    - No explanation, no extra words
    - "url" must be a valid full URL
    - "force_new" is true only if user explicitly wants a new tab
    - "force_new_window" is true only if user explicitly wants a new browser window

    force_new is TRUE when user says things like:
    - "open a new tab of youtube"
    - "open another youtube"
    - "new tab youtube"
    - "open youtube in new tab"

    force_new_window is TRUE when user says things like:
    - "open youtube in a new window"
    - "open github in a new browser window"
    - "open spotify in a separate window"

    force_new and force_new_window are both FALSE when user says things like:
    - "open youtube"
    - "go to github"
    - "open spotify"

    Examples:
    open youtube -> {{"url": "https://youtube.com", "force_new": false, "force_new_window": false}}
    open new tab of youtube -> {{"url": "https://youtube.com", "force_new": true, "force_new_window": false}}
    open youtube in a new window -> {{"url": "https://youtube.com", "force_new": false, "force_new_window": true}}
    open another github -> {{"url": "https://github.com", "force_new": true, "force_new_window": false}}
    go to google -> {{"url": "https://google.com", "force_new": false, "force_new_window": false}}

    Command:
    {user_command}

    JSON:
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60,
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()

    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)

        url = result.get("url", "")
        force_new = result.get("force_new", False)
        force_new_window = result.get("force_new_window", False)

        if not url.startswith(("http://", "https://")):
            print("[Jarvis] Invalid URL returned by LLM, ignoring.")
            return False

        keyword = extract_keyword(url)
        print(f"[LLM decided]: {url} | keyword: {keyword} | force_new: {force_new} | force_new_window: {force_new_window}")

        open_browser(url, keyword, force_new=force_new, force_new_window=force_new_window)
        return url

    except json.JSONDecodeError:
        print(f"[Jarvis] Could not parse LLM response: {raw}")
        return False