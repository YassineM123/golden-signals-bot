# Golden Signals Bot (safe public version)
# ------------------------------------------------------------
# Before running: create a config.json file based on config.example.json
# ------------------------------------------------------------

import os, json, re, hashlib, contextlib
from telethon import TelegramClient, events, Button

# ============ CONFIG ============
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

API_ID = cfg["API_ID"]
API_HASH = cfg["API_HASH"]
SESSION  = cfg["SESSION"]
SOURCE_ID = cfg["SOURCE_ID"]
DEST_ID   = cfg["DEST_ID"]
BRAND_HANDLE = cfg["BRAND_HANDLE"]
CHANNEL_URL  = cfg["CHANNEL_URL"]

HEADER = f"🟡 TRADING FUTURE · {BRAND_HANDLE}"
FOOTER = f"🔔 Rejoindre : {CHANNEL_URL}"

REPLACEMENTS = {
    "@eufxadmin": "@Trading_Futuree",
    "@eufxfeedback": "@Trading_Futuree",
    "Lifetime VIP $35 only": "",
    "membership @eufxadmin": "@Trading_Futuree",
}

GLOBAL_TAGS = ["#Gold", "#XAUUSD", "#Signals"]
UTM = ""

MAP_FILE    = "message_map.json"
HASH_FILE   = "seen_hashes.json"
STATE_FILE  = "open_signals.json"
FLUSH_EVERY = 20
DOWNLOAD_DIR = "tmp_media"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

client = TelegramClient(SESSION, API_ID, API_HASH)
message_map, seen_hashes, open_signals = {}, {}, {}
_since_flush = 0

# ---------- Persistence ----------
def _load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_state():
    global message_map, seen_hashes, open_signals
    message_map  = {int(k): int(v) for k, v in _load_json(MAP_FILE, {}).items()}
    seen_hashes  = _load_json(HASH_FILE, {})
    open_signals = _load_json(STATE_FILE, {})

def flush_state(force=False):
    global _since_flush
    if not force and _since_flush < FLUSH_EVERY: return
    _save_json(MAP_FILE, {str(k): v for k, v in message_map.items()})
    _save_json(HASH_FILE, seen_hashes)
    _save_json(STATE_FILE, open_signals)
    _since_flush = 0

# ---------- Utils ----------
def apply_replacements(text: str) -> str:
    if not text: return ""
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    return text

def append_tags(text: str, extra=None) -> str:
    tags = GLOBAL_TAGS[:] + (extra or [])
    tline = " ".join(dict.fromkeys(tags))
    body = (text or "").rstrip()
    if body.endswith(tline): return body
    sep = "\n\n" if body else ""
    return f"{body}{sep}{tline}"[:4096]

async def send_with_brand(text: str, reply_to_id=None, file_path=None):
    buttons = [[Button.url("🔔 Join Channel", CHANNEL_URL)]]
    if file_path:
        return await client.send_file(DEST_ID, file_path, caption=text[:1024], buttons=buttons, reply_to=reply_to_id)
    return await client.send_message(DEST_ID, text[:4096], buttons=buttons, link_preview=False, reply_to=reply_to_id)

# ---------- Event Handler ----------
@client.on(events.NewMessage(chats=SOURCE_ID))
async def on_new(event):
    global _since_flush
    src = event.message
    dest_reply_id = message_map.get(src.reply_to_msg_id) if src.reply_to_msg_id else None
    original = (getattr(src, "caption", None) or src.message or "")
    cleaned = apply_replacements(original)
    text = append_tags(cleaned)
    if src.media:
        file_path = await client.download_media(src.media, file=DOWNLOAD_DIR)
        sent = await send_with_brand(text, reply_to_id=dest_reply_id, file_path=file_path)
        os.remove(file_path)
    else:
        sent = await send_with_brand(text, reply_to_id=dest_reply_id)
    message_map[src.id] = sent.id
    _since_flush += 1
    flush_state(False)

def main():
    load_state()
    print("🚀 Golden Signals Bot started...")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    try:
        main()
    finally:
        flush_state(True)
