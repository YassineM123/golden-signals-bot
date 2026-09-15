# Golden Signals Bot

A powerful Telegram bot built with **Telethon** to automatically forward, reformat, and enhance trading signal messages.

**Features**: Signal forwarding • Media handling • Branding customization • Hashtag injection • Channel management

## Overview

Golden Signals Bot is designed to streamline trading signal distribution across Telegram channels. It:
- Detects trading signal messages from a source channel
- Enriches them with branding, hashtags, and call-to-action buttons
- Copies media (images, documents) automatically
- Maintains message thread relationships
- Ensures no duplicates through hashing

Perfect for trading communities, signal providers, and crypto/forex traders who want automated, professional signal distribution.

## Features

### Message Processing
- ✅ Automatic signal detection and forwarding
- ✅ Custom text replacements (e.g., handle normalization)
- ✅ Media copying (photos, documents, files)
- ✅ Hashtag injection (global + custom tags)
- ✅ Header and footer branding
- ✅ Action button with channel link

### State Management
- ✅ Message mapping (source → destination)
- ✅ Duplicate detection via content hashing
- ✅ Open signals tracking
- ✅ Persistent state files (JSON)
- ✅ Auto-recovery on restart

### Reliability
- ✅ Error handling and logging
- ✅ Automatic retry on failures
- ✅ Graceful shutdown
- ✅ Session management

## Tech Stack

- **Python** 3.8+
- **Telethon** 1.36.0 - Telegram client library
- **JSON** - Lightweight state storage

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram account
- API credentials from [my.telegram.org](https://my.telegram.org)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/YassineM123/golden-signals-bot.git
cd golden-signals-bot
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Get Telegram API credentials**
   - Visit [my.telegram.org](https://my.telegram.org)
   - Go to "API development tools"
   - Create a new application
   - Copy `API_ID` and `API_HASH`

5. **Create config file**
```bash
cp config.example.json config.json
```

6. **Edit `config.json` with your values**
```json
{
  "API_ID": 123456,
  "API_HASH": "your_api_hash_here",
  "SESSION": "golden_signals_bot",
  "SOURCE_ID": -1001234567890,
  "DEST_ID": -1001234567890,
  "BRAND_HANDLE": "@YourBrandHandle",
  "CHANNEL_URL": "https://t.me/YourChannelURL"
}
```

## Configuration

### config.json Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `API_ID` | int | Your Telegram API ID from my.telegram.org |
| `API_HASH` | string | Your Telegram API Hash from my.telegram.org |
| `SESSION` | string | Session name (creates a .session file) |
| `SOURCE_ID` | int | Source channel ID (negative number) |
| `DEST_ID` | int | Destination channel ID (negative number) |
| `BRAND_HANDLE` | string | Your brand handle (e.g., @YourHandle) |
| `CHANNEL_URL` | string | Public channel URL for action button |

### Finding Channel IDs

To find a channel's ID:
1. Forward a message from the channel to [@userinfobot](https://t.me/userinfobot)
2. Bot will show the channel ID (usually starts with -100)

### Customization

Edit `bot.py` to customize:

**Text Replacements** (line 24-29):
```python
REPLACEMENTS = {
    "@old_handle": "@new_handle",
    "remove this text": "",
}
```

**Global Hashtags** (line 31):
```python
GLOBAL_TAGS = ["#Gold", "#XAUUSD", "#Signals"]
```

**Other Settings** (line 33-37):
```python
HEADER = f"🟡 TRADING FUTURE · {BRAND_HANDLE}"
FOOTER = f"🔔 Join: {CHANNEL_URL}"
FLUSH_EVERY = 20  # Save state every N messages
DOWNLOAD_DIR = "tmp_media"  # Temp media storage
```

## Usage

### Run the Bot

```bash
python bot.py
```

**Expected output**:
```
🚀 Golden Signals Bot started...
```

The bot will now:
- Listen for new messages in the source channel
- Process and forward them to the destination channel
- Save state periodically
- Handle media automatically

### Stop the Bot

Press `Ctrl+C` to stop. State is automatically saved.

## How It Works

### Signal Detection & Processing

```
SOURCE CHANNEL
      ↓
  [New Message]
      ↓
  [Extract text + media]
      ↓
  [Apply replacements]
      ↓
  [Add header + tags + footer]
      ↓
DESTINATION CHANNEL
  [Enhanced message sent]
```

### State Files

The bot creates three JSON state files:

1. **`message_map.json`** - Maps source message IDs to destination IDs
2. **`seen_hashes.json`** - Content hashes to prevent duplicates
3. **`open_signals.json`** - Currently active signals

These files allow recovery after restart.

## Workflow Example

### Original Message (Source Channel)
```
EURUSD BUY Signal
Entry: 1.0850
TP: 1.0950
SL: 1.0750

Membership @eufxadmin
```

### Processed Message (Destination Channel)
```
🟡 TRADING FUTURE · @YourBrandHandle

EURUSD BUY Signal
Entry: 1.0850
TP: 1.0950
SL: 1.0750

Membership @Trading_Futuree

#Gold #XAUUSD #Signals

[Join Channel Button]

🔔 Join: https://t.me/YourChannelURL
```

## Advanced Features

### Message Threading
If a signal has replies in the source channel, they are automatically grouped in the destination with the same thread relationship.

### Media Handling
- Photos: Automatically copied and attached to destination message
- Documents: Downloaded, forwarded, then cleaned up
- Caption text: Preserved and processed like regular messages

### Duplicate Prevention
- Content hashing detects identical or near-identical messages
- Prevents spam if the same signal is sent multiple times

### Graceful Shutdown
- Saves all state before closing
- Resumes exactly where it left off on restart

## Security

### Important Guidelines

⚠️ **NEVER:**
- Commit `config.json` to version control
- Commit `.session` files (contain authentication tokens)
- Share your API credentials with anyone
- Leave credentials in environment variables without protection

✅ **DO:**
- Keep `config.json` in `.gitignore` (already done)
- Rotate API credentials if ever exposed
- Use `.env` files for sensitive data in production
- Limit channel access to trusted accounts only

## Troubleshooting

### Bot doesn't start
```
Error: Failed to connect to Telegram
Solution:
- Verify API_ID and API_HASH are correct
- Check internet connection
- Try creating a new session (delete .session file)
```

### Messages not forwarding
```
Error: Access denied to channel
Solution:
- Ensure SOURCE_ID and DEST_ID are correct (negative numbers)
- Verify the bot account has permission to read source channel
- Verify the bot account has permission to post in destination channel
```

### Session not found
```
Error: No session file
Solution:
- Delete SESSION_NAME.session if it exists
- Re-run the bot to create a new session
- You'll need to authenticate again
```

### Duplicates appearing
```
Solution:
- Duplicate detection is automatic via hashing
- If still seeing duplicates, check REPLACEMENTS settings
- Clear seen_hashes.json if needed (will reprocess old messages)
```

## Project Structure

```
golden-signals-bot/
├── bot.py                    # Main bot script
├── config.example.json       # Configuration template
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
│
├── config.json              # Your config (gitignored)
├── golden_signals_bot.session  # Session file (gitignored)
│
├── message_map.json         # State: message ID mappings
├── seen_hashes.json         # State: content hashes
├── open_signals.json        # State: active signals
└── tmp_media/               # Temporary media files
```

## Dependencies

```
telethon==1.36.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Performance

- **Latency**: ~1-2 seconds per message (network dependent)
- **CPU Usage**: Minimal, runs in low-power environments
- **Memory**: ~50-100 MB typical
- **Storage**: State files are small (<10 MB each)

## Resources

- **Telethon Docs**: https://docs.telethon.dev
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **my.telegram.org**: https://my.telegram.org

## Roadmap

- [ ] Multi-source channel support
- [ ] Custom template system for message formatting
- [ ] Database backend (instead of JSON)
- [ ] Web dashboard for monitoring
- [ ] Analytics/reporting features
- [ ] Scheduled message support

## Support

**Issues?**
- Check troubleshooting section above
- Review Telethon documentation
- Open an issue on GitHub

**Questions?**
- Create a GitHub discussion
- Review code comments

## License

MIT License - Free to use and modify

---

**Made with ❤️ for traders** | [YassineM123](https://github.com/YassineM123)
