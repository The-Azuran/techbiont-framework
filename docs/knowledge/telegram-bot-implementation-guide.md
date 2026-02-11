# Telegram Bot Implementation Guide
**Secure, Self-Hosted Patterns for 2026**

Research compiled: 2026-02-08
Author: Rowan Valle
Organization: Symbiont Systems LLC

---

## Executive Summary

This guide covers secure Telegram Bot implementation patterns for self-hosted deployments in 2026. It synthesizes official Telegram documentation, security best practices, and real-world examples from the Python ecosystem.

**Key findings:**
- Bot API 7.x is current as of 2026 with ongoing adaptive rate limit testing
- Webhook deployments require HTTPS (ports 443, 80, 88, or 8443)
- File limits: 20MB download via Bot API (2GB via direct API), 50MB upload standard
- Rate limits: 30 msg/s free tier, 1000 msg/s with paid broadcasting
- Python ecosystem: `python-telegram-bot` v22.6+ is mature and async-native

---

## 1. Telegram Bot API Fundamentals

### Current API Version
- **Bot API 7.x** (as of Feb 2026)
- Continuous updates tracked at: https://core.telegram.org/bots/api-changelog
- Python library: `python-telegram-bot` v22.6 (Feb 1, 2026 release)

### Update Delivery Methods

Two mutually exclusive methods exist for receiving updates:

#### A. Long Polling (`getUpdates`)
- Pull model: bot requests updates from Telegram servers
- Simpler to set up, no public IP or domain required
- Higher latency, more resource intensive
- Good for: development, personal bots, low-traffic scenarios
- Updates stored server-side for 24 hours max

**Implementation:**
```python
from telegram.ext import Application

app = Application.builder().token("BOT_TOKEN").build()
app.run_polling()  # Starts long polling loop
```

#### B. Webhooks
- Push model: Telegram sends HTTPS POST to your endpoint
- Lower latency, more scalable
- Requires: public IP, domain, valid SSL/TLS certificate
- Good for: production, high-traffic bots, serverless deployments

**Requirements:**
- **Ports:** 443, 80, 88, or 8443 (no others supported)
- **TLS:** Mandatory, no plain HTTP allowed
- **Certificate:** Can use self-signed (upload via `certificate` parameter)

**Implementation:**
```python
from telegram.ext import Application

app = Application.builder().token("BOT_TOKEN").build()
app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="webhook",
    webhook_url="https://yourdomain.com:8443/webhook"
)
```

**References:**
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Marvin's Marvellous Guide to All Things Webhook](https://core.telegram.org/bots/webhooks)
- [python-telegram-bot Documentation v22.6](https://python-telegram-bot.org/)

---

## 2. Security Architecture

### 2.1 Token Storage

**NEVER hardcode tokens.** Use environment variables, encrypted config files, or secret managers.

**Priority ranking:**
1. **Hardware security modules (HSM)** - enterprise deployments
2. **Secret managers** - AWS Secrets Manager, Google Secret Manager, HashiCorp Vault
3. **System keyring** - `python-keyring` library for local storage
4. **Environment variables** - minimum acceptable standard
5. **Encrypted .env files** - mode 600, never commit to git

**Example (environment variables):**
```bash
# .env (mode 600, .gitignored)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Load in Python
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

**Example (keyring):**
```python
import keyring

# Store once
keyring.set_password("telegram_bot", "mybot_token", "1234567890:ABC...")

# Retrieve
BOT_TOKEN = keyring.get_password("telegram_bot", "mybot_token")
```

### 2.2 Token Rotation
- Rotate tokens every 6 months minimum
- Rotate immediately if compromise suspected
- Use @BotFather to revoke and regenerate tokens

### 2.3 User Authentication

**Chat ID Whitelisting** (most common pattern):

```python
ALLOWED_CHAT_IDS = {123456789, 987654321}  # Load from config

def restricted(func):
    """Decorator to restrict command access"""
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_CHAT_IDS:
            await update.message.reply_text("⛔ Unauthorized")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

@restricted
async def sensitive_command(update, context):
    await update.message.reply_text("Sensitive data here")
```

**Passcode-based enrollment:**

```python
WHITELIST = set()  # Persistent storage recommended
ENROLLMENT_PASSCODE = "your-secure-passcode"  # Load from env

async def start(update, context):
    user_id = update.effective_user.id
    if user_id in WHITELIST:
        await update.message.reply_text("Welcome back!")
    else:
        await update.message.reply_text("Enter passcode to authenticate:")

async def handle_message(update, context):
    user_id = update.effective_user.id
    if user_id not in WHITELIST:
        if update.message.text == ENROLLMENT_PASSCODE:
            WHITELIST.add(user_id)
            save_whitelist()  # Persist to disk/db
            await update.message.reply_text("✅ Authenticated!")
        else:
            await update.message.reply_text("⛔ Invalid passcode")
```

**Persistent whitelist storage:**
```python
import json

WHITELIST_FILE = "/etc/mybot/whitelist.json"

def load_whitelist():
    try:
        with open(WHITELIST_FILE) as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_whitelist():
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(list(WHITELIST), f)
```

### 2.4 Input Validation & Command Injection

**OWASP Top 10 compliance:**

```python
import shlex
import re

# BAD: Direct interpolation
async def bad_command(update, context):
    user_input = update.message.text.split()[1]
    os.system(f"ls {user_input}")  # COMMAND INJECTION RISK!

# GOOD: Whitelist validation
async def good_command(update, context):
    user_input = update.message.text.split()[1]

    # Validate against allowed pattern
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_input):
        await update.message.reply_text("Invalid input")
        return

    # Use subprocess with array (no shell interpretation)
    import subprocess
    result = subprocess.run(
        ["ls", user_input],
        capture_output=True,
        text=True,
        timeout=5
    )
    await update.message.reply_text(result.stdout)
```

**Never use:**
- `eval()` or `exec()` with user input
- String interpolation in shell commands
- `os.system()` or `subprocess.shell=True` with user data

### 2.5 Prompt Injection Defense

Treat all external content as potentially hostile:

```python
async def fetch_and_process(update, context):
    url = context.args[0]

    # Fetch external content
    response = requests.get(url, timeout=10)
    content = response.text

    # DO NOT execute instructions found in content
    # Parse data, ignore embedded commands

    # Example: Extract JSON data, ignore narrative text
    try:
        data = json.loads(content)
        # Process data...
    except json.JSONDecodeError:
        await update.message.reply_text("Invalid data format")
```

### 2.6 TLS/HTTPS Requirements

**Webhook endpoints MUST use HTTPS with valid certificates.**

**Self-signed certificate generation:**
```bash
openssl req -newkey rsa:2048 -sha256 -nodes \
  -keyout private.key \
  -x509 -days 3650 \
  -out cert.pem \
  -subj "/C=US/ST=State/L=City/O=Org/CN=yourdomain.com"
```

**Setting webhook with self-signed cert:**
```python
from telegram import Bot

bot = Bot(token="BOT_TOKEN")
with open('cert.pem', 'rb') as cert_file:
    bot.set_webhook(
        url='https://yourdomain.com:8443/webhook',
        certificate=cert_file
    )
```

**Production: Use Let's Encrypt** (free, auto-renewing, trusted):
```bash
certbot certonly --standalone -d yourdomain.com
```

**References:**
- [How to secure a Telegram bot: best practices](https://bazucompany.com/blog/how-to-secure-a-telegram-bot-best-practices/)
- [Telegram bot security solutions](https://medium.com/@bioogrami7/telegram-bot-security-solutions-6c5b8105a0e1)
- [Security Guidelines for Client Developers](https://core.telegram.org/mtproto/security_guidelines)

---

## 3. Rate Limits & Throttling

### Current Limits (as of Feb 2026)

**Per-chat limits:**
- 1 message per second to individual users
- 20 messages per minute to groups

**Broadcasting limits:**
- **Free tier:** ~30 messages/second
- **Paid tier:** Up to 1000 messages/second (0.1 Telegram Stars per message over 30/s)

**Error handling:**
- `429 Too Many Requests` returned when exceeded
- Response includes `retry_after` field (seconds to wait)

**Short bursts** may be tolerated, but sustained violations trigger throttling.

### Adaptive Rate Windows (2026 Beta)

Telegram is testing **reputation-based rate limits**:
- Bot score: hidden integer 0-1000
- Higher score → larger rate window
- Factors: uptime, user reports, compliance history

**Implication:** Build for 30 msg/s, but architect for dynamic scaling.

### Throttling Strategies

**Strategy 1: Aggressive (low-latency use cases)**
- 25 msg/s burst
- 0.5s max retry delay
- Drop messages on second 429 error
- Use case: live gaming, real-time alerts

**Strategy 2: Resilient (reliability-critical)**
- 10 msg/s sustained
- 3-step exponential backoff (1s, 4s, 16s)
- Persist failed messages to queue
- Use case: invoice receipts, compliance notifications

**Implementation (basic throttling):**
```python
import asyncio
from collections import deque
from time import time

class RateLimiter:
    def __init__(self, max_per_second=25):
        self.max_per_second = max_per_second
        self.timestamps = deque()

    async def acquire(self):
        now = time()
        # Remove timestamps older than 1 second
        while self.timestamps and self.timestamps[0] < now - 1:
            self.timestamps.popleft()

        if len(self.timestamps) >= self.max_per_second:
            sleep_time = 1 - (now - self.timestamps[0])
            await asyncio.sleep(sleep_time)

        self.timestamps.append(time())

limiter = RateLimiter(max_per_second=25)

async def send_throttled(bot, chat_id, text):
    await limiter.acquire()
    await bot.send_message(chat_id=chat_id, text=text)
```

**Advanced: Distributed rate limiting**
For multi-instance deployments, use Redis:

```python
import redis
import time

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def distributed_rate_limit(key, max_per_second=25):
    now = time.time()
    window_key = f"ratelimit:{key}:{int(now)}"

    # Increment counter for current second
    current = redis_client.incr(window_key)
    redis_client.expire(window_key, 2)  # Cleanup after 2 seconds

    if current > max_per_second:
        await asyncio.sleep(1)
        return await distributed_rate_limit(key, max_per_second)
```

**References:**
- [Bots FAQ - Rate Limits](https://core.telegram.org/bots/faq)
- [How to solve rate limit errors from Telegram Bot API](https://gramio.dev/rate-limits)
- [Scaling Up IV: Flood Limits](https://grammy.dev/advanced/flood)

---

## 4. File Handling

### Size Limits

**Download (Bot API):**
- Standard: 20 MB
- Undocumented increase: up to 2 GB (observed, not guaranteed)

**Upload:**
- Standard Bot API: 50 MB
- Custom Bot API server: up to 2 GB (requires self-hosting telegram-bot-api)

**Note:** Limits vary by implementation method (official Bot API vs direct TDLib).

### Media Handling Patterns

**Downloading files:**
```python
async def handle_document(update, context):
    document = update.message.document

    # Check file size (optional)
    if document.file_size > 20 * 1024 * 1024:  # 20 MB
        await update.message.reply_text("File too large")
        return

    # Download file
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive('downloads/myfile.pdf')

    await update.message.reply_text("File downloaded!")
```

**Uploading files:**
```python
async def send_file(update, context):
    with open('report.pdf', 'rb') as f:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=f,
            filename="report.pdf",
            caption="Monthly report"
        )
```

**Streaming large files (chunked upload):**
```python
async def upload_large_file(bot, chat_id, file_path):
    file_size = os.path.getsize(file_path)

    if file_size > 50 * 1024 * 1024:
        await bot.send_message(
            chat_id,
            f"File too large ({file_size / 1024 / 1024:.1f} MB). Uploading to cloud..."
        )
        # Use external storage (S3, Drive) and send link
        upload_url = await upload_to_s3(file_path)
        await bot.send_message(chat_id, f"Download: {upload_url}")
    else:
        with open(file_path, 'rb') as f:
            await bot.send_document(chat_id=chat_id, document=f)
```

**Media types supported:**
- Photos (10 MB max)
- Videos (50 MB max via Bot API)
- Audio files
- Voice messages
- Documents (generic files)
- Stickers

**References:**
- [Telegram Limits](https://limits.tginfo.me/en)
- [Uploading and Downloading Files](https://core.telegram.org/api/files)
- [Bots FAQ](https://core.telegram.org/bots/faq)

---

## 5. Bot Hosting Architectures

### A. Self-Hosted (Long Polling)

**Simplest deployment pattern.**

**Pros:**
- No public IP required
- No domain/TLS setup
- Easy to develop and debug

**Cons:**
- Higher resource usage (constant polling)
- Slightly higher latency
- Must handle bot process management

**Example (systemd service):**

```ini
# /etc/systemd/system/mybot.service
[Unit]
Description=My Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/mybot
Environment="TELEGRAM_BOT_TOKEN=your_token_here"
ExecStart=/usr/bin/python3 /opt/mybot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mybot
sudo systemctl start mybot
sudo systemctl status mybot
```

### B. Self-Hosted (Webhook + FastAPI)

**Production-grade self-hosted deployment.**

**Stack:**
- FastAPI (webhook receiver)
- Nginx (reverse proxy, TLS termination)
- Let's Encrypt (certificates)

**Example FastAPI webhook handler:**

```python
from fastapi import FastAPI, Request, HTTPException
from telegram import Update
from telegram.ext import Application
import uvicorn

app = FastAPI()
telegram_app = Application.builder().token("BOT_TOKEN").build()

# Add handlers to telegram_app here
# telegram_app.add_handler(CommandHandler("start", start))

@app.post("/webhook")
async def webhook(request: Request):
    # Security: verify request came from Telegram
    # (check X-Telegram-Bot-Api-Secret-Token header if set)

    json_data = await request.json()
    update = Update.de_json(json_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await telegram_app.bot.set_webhook(
        url="https://yourdomain.com/webhook",
        drop_pending_updates=True
    )
    await telegram_app.initialize()
    await telegram_app.start()

@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.stop()
    await telegram_app.shutdown()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Nginx configuration:**

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location /webhook {
        proxy_pass http://127.0.0.1:8000/webhook;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        return 404;  # Hide other endpoints
    }
}
```

**Security enhancement (IP whitelisting):**

Telegram webhook requests come from specific IP ranges. Add to nginx config:

```nginx
# Allow Telegram servers only
allow 149.154.160.0/20;
allow 91.108.4.0/22;
deny all;
```

**References:**
- [fastapi-security-telegram-webhook](https://github.com/b0g3r/fastapi-security-telegram-webhook)
- [Hosting multiple Telegram bots with NGINX](https://madhead.me/posts/nginx-tg-bots/)
- [Telegram echo bot with FastAPI](https://salaivv.com/2023/01/04/telegram-bot-fastapi)

### C. Serverless (AWS Lambda, Google Cloud Functions)

**For low-traffic bots with sporadic usage.**

**Pros:**
- Pay per invocation
- Auto-scaling
- No server maintenance

**Cons:**
- Cold start latency
- Complexity in state management
- Vendor lock-in

**AWS Lambda example (Python):**

```python
import json
from telegram import Update, Bot
from telegram.ext import Application

bot = Bot(token="BOT_TOKEN")
app = Application.builder().token("BOT_TOKEN").build()

# Add handlers...

def lambda_handler(event, context):
    # Parse Telegram update from API Gateway
    body = json.loads(event['body'])
    update = Update.de_json(body, bot)

    # Process update
    app.process_update(update)

    return {
        'statusCode': 200,
        'body': json.dumps({'ok': True})
    }
```

**API Gateway integration:**
- Create REST API in API Gateway
- Set POST method route to Lambda function
- Configure webhook URL: `https://your-api-id.execute-api.region.amazonaws.com/prod/webhook`

---

## 6. Advanced Features

### 6.1 Inline Keyboards & Callback Queries

Inline keyboards provide interactive buttons within messages.

**Creating inline keyboard:**

```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def show_menu(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='opt1'),
            InlineKeyboardButton("Option 2", callback_data='opt2')
        ],
        [InlineKeyboardButton("Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Choose an option:',
        reply_markup=reply_markup
    )
```

**Handling callbacks:**

```python
from telegram.ext import CallbackQueryHandler

async def button_callback(update, context):
    query = update.callback_query

    # CRITICAL: Must acknowledge callback to stop loading animation
    await query.answer()

    # Handle different button presses
    if query.data == 'opt1':
        await query.edit_message_text("You chose Option 1")
    elif query.data == 'opt2':
        await query.edit_message_text("You chose Option 2")
    elif query.data == 'cancel':
        await query.edit_message_text("Cancelled")

# Register handler
app.add_handler(CallbackQueryHandler(button_callback))
```

**Important:** Always call `query.answer()` even if you don't show a notification. Otherwise, Telegram clients display a loading spinner indefinitely.

**References:**
- [Telegram Bot API - Inline Keyboards](https://core.telegram.org/bots/api#inlinekeyboardmarkup)
- [Buttons](https://core.telegram.org/api/bots/buttons)
- [python-telegram-bot inline keyboard example](https://docs.python-telegram-bot.org/en/stable/examples.inlinekeyboard.html)

### 6.2 Bot Commands & Menu Interfaces

**Setting bot commands (shown in chat menu):**

```python
from telegram import BotCommand

async def set_commands(bot):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help message"),
        BotCommand("status", "Check system status"),
        BotCommand("settings", "Configure settings")
    ]
    await bot.set_my_commands(commands)

# Call during initialization
await set_commands(app.bot)
```

**Command handlers:**

```python
from telegram.ext import CommandHandler

async def start(update, context):
    await update.message.reply_text("Welcome! Use /help for commands.")

async def help_command(update, context):
    help_text = """
Available commands:
/start - Start the bot
/help - Show this message
/status - Check status
    """
    await update.message.reply_text(help_text)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
```

### 6.3 Conversation Handlers (Multi-Step Dialogs)

For interactive workflows requiring multiple steps:

```python
from telegram.ext import ConversationHandler, MessageHandler, filters

# States
CHOOSING, TYPING_REPLY = range(2)

async def start_conversation(update, context):
    await update.message.reply_text(
        "What's your name?",
    )
    return CHOOSING

async def received_name(update, context):
    user_name = update.message.text
    context.user_data['name'] = user_name

    await update.message.reply_text(
        f"Nice to meet you, {user_name}! What's your age?"
    )
    return TYPING_REPLY

async def received_age(update, context):
    age = update.message.text
    name = context.user_data['name']

    await update.message.reply_text(
        f"Got it! {name}, age {age}. Thanks!"
    )
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Register conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('register', start_conversation)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_name)],
        TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_age)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

app.add_handler(conv_handler)
```

---

## 7. Real-World Implementation Examples

### 7.1 Home Automation Bot

**Use case:** Control home devices, receive sensor alerts

**Features:**
- Command relay (toggle lights, set temperature)
- Status queries (current temperature, door status)
- Async notifications (motion detected, temperature threshold)

**Example (minimal):**

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

ALLOWED_USERS = {123456789}  # Your Telegram user ID

async def lights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        return

    action = context.args[0] if context.args else "status"

    if action == "on":
        # Call home automation API
        turn_on_lights()
        await update.message.reply_text("💡 Lights ON")
    elif action == "off":
        turn_off_lights()
        await update.message.reply_text("💡 Lights OFF")
    else:
        status = get_light_status()
        await update.message.reply_text(f"💡 Lights: {status}")

async def send_alert(app, chat_id, message):
    """Background task for sending alerts"""
    await app.bot.send_message(chat_id=chat_id, text=f"🚨 {message}")

# Monitor sensors in background
async def sensor_monitor(app):
    while True:
        if motion_detected():
            for user_id in ALLOWED_USERS:
                await send_alert(app, user_id, "Motion detected in living room")
        await asyncio.sleep(5)

if __name__ == '__main__':
    app = Application.builder().token("BOT_TOKEN").build()
    app.add_handler(CommandHandler("lights", lights))

    # Start sensor monitoring in background
    app.job_queue.run_repeating(
        lambda context: asyncio.create_task(sensor_monitor(app)),
        interval=5,
        first=0
    )

    app.run_polling()
```

**References:**
- [GitHub - HA4IoT: Home Automation for .NET](https://github.com/chkr1011/HA4IoT)
- [Telegram bot - Home Assistant](https://www.home-assistant.io/integrations/telegram_bot/)

### 7.2 Notification Bot

**Use case:** Send alerts from scripts, cronjobs, CI/CD pipelines

**Pattern:**

```python
# notification_bot.py (runs as service)
from telegram.ext import Application

app = Application.builder().token("BOT_TOKEN").build()
app.run_polling()

# send_notification.py (called by cron/scripts)
import requests

BOT_TOKEN = "your_token"
CHAT_ID = "your_chat_id"

def send_notification(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    })

# Usage in scripts
send_notification("✅ Backup completed successfully")
send_notification("❌ Error: Database connection failed")
```

**Cron integration:**

```bash
# /etc/cron.daily/backup
#!/bin/bash
if /opt/scripts/backup.sh; then
    python3 /opt/scripts/send_notification.py "✅ Daily backup completed"
else
    python3 /opt/scripts/send_notification.py "❌ Backup failed"
fi
```

### 7.3 Command Relay Bot (MESO Use Case)

**Use case:** Remote access to Claude Code CLI via Telegram

**Architecture:**
```
Telegram Client → Telegram API → Webhook/Polling → FastAPI → Claude CLI → Response
```

**Security considerations:**
1. **Strict chat_id whitelist** (single user)
2. **Passcode re-authentication** for sensitive commands
3. **Command logging** (audit trail)
4. **Rate limiting** (prevent abuse)
5. **Session timeout** (auto-logout after inactivity)

**Minimal proof of concept:**

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import subprocess
import shlex

OWNER_ID = 123456789  # Your Telegram user ID
SESSION_TIMEOUT = 3600  # 1 hour

# Simple session management
active_sessions = {}

async def authenticate(update, context):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("⛔ Unauthorized")
        return False

    # Check session timeout
    import time
    last_activity = active_sessions.get(user_id, 0)
    if time.time() - last_activity > SESSION_TIMEOUT:
        await update.message.reply_text("🔒 Session expired. Use /auth")
        return False

    active_sessions[user_id] = time.time()
    return True

async def auth(update, context):
    if update.effective_user.id != OWNER_ID:
        return

    passcode = " ".join(context.args)
    if passcode == "your-secure-passcode":  # Load from env
        import time
        active_sessions[update.effective_user.id] = time.time()
        await update.message.reply_text("✅ Authenticated")
    else:
        await update.message.reply_text("⛔ Invalid passcode")

async def claude(update, context):
    if not await authenticate(update, context):
        return

    # Parse command
    command_args = " ".join(context.args)

    # Execute Claude CLI (with safety checks)
    try:
        result = subprocess.run(
            ["claude", "-c", command_args],
            capture_output=True,
            text=True,
            timeout=60,  # 1 minute max
            cwd="/home/user/projects"  # Safe working directory
        )

        response = result.stdout if result.returncode == 0 else result.stderr

        # Telegram message limit: 4096 chars
        if len(response) > 4000:
            # Send as file
            with open("/tmp/claude_output.txt", "w") as f:
                f.write(response)
            await update.message.reply_document(
                document=open("/tmp/claude_output.txt", "rb"),
                filename="output.txt"
            )
        else:
            await update.message.reply_text(f"```\n{response}\n```", parse_mode="Markdown")

    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏱️ Command timeout")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

if __name__ == '__main__':
    app = Application.builder().token("BOT_TOKEN").build()
    app.add_handler(CommandHandler("auth", auth))
    app.add_handler(CommandHandler("claude", claude))

    app.run_polling()
```

**Production hardening:**
- Use proper secret management (not hardcoded passcodes)
- Implement 2FA (TOTP via pyotp)
- Add command whitelist (restrict dangerous operations)
- Encrypt session storage
- Add comprehensive audit logging
- Implement automatic session cleanup

---

## 8. MTProto & End-to-End Encryption

### Understanding MTProto

**MTProto** is Telegram's proprietary protocol for client-server communication.

**Architecture:**
1. **High-level component**: API query language (TL)
2. **Cryptographic layer**: Authorization and encryption
3. **Transport component**: Data delivery

### Server-Client Encryption (Cloud Chats)

**NOT end-to-end encrypted** — Telegram servers can read messages.

**Encryption details:**
- 2048-bit authorization key (Diffie-Hellman exchange)
- AES-256 in IGE mode (Infinite Garble Extension)
- Perfect Forward Secrecy (PFS)

**Bot API implications:**
- Bots use server-client encryption (same as cloud chats)
- Bots CANNOT access Secret Chats (E2EE)
- All bot messages stored on Telegram servers

### End-to-End Encryption (Secret Chats)

**Only available in 1-to-1 Secret Chats, NOT available to bots.**

**Encryption details:**
- 256-bit AES-IGE
- Key held only by participants (never on servers)
- Perfect Forward Secrecy
- Self-destruct timers

### Security Analysis

**Strengths:**
- Formally verified authentication and integrity properties
- PFS in both cloud and secret chats
- Resistant to chosen ciphertext attacks (IND-CCA)

**Weaknesses:**
- Rekeying protocol vulnerable to Unknown Key-Share (UKS) attacks
- Non-standard cryptography (not audited to same extent as Signal Protocol)
- Metadata not encrypted (who talks to whom, when)

### Practical Implications for Bots

**Bots cannot:**
- Access Secret Chats
- Implement true E2EE
- Read encrypted messages

**Security model:**
- Trust Telegram servers not to read messages
- Use additional encryption layer if needed (e.g., PGP for sensitive data)

**Example (PGP layer for sensitive data):**

```python
import gnupg

gpg = gnupg.GPG()

async def send_encrypted(update, context):
    message = " ".join(context.args)

    # Encrypt with recipient's public key
    encrypted = gpg.encrypt(message, recipients=['user@example.com'])

    await update.message.reply_text(f"🔒 Encrypted:\n```\n{encrypted}\n```")

async def decrypt_message(update, context):
    encrypted_text = update.message.text

    # Decrypt with bot's private key
    decrypted = gpg.decrypt(encrypted_text)

    if decrypted.ok:
        await update.message.reply_text(f"🔓 Decrypted:\n{decrypted.data.decode()}")
    else:
        await update.message.reply_text("❌ Decryption failed")
```

**References:**
- [MTProto Mobile Protocol](https://core.telegram.org/mtproto)
- [End-to-End Encryption, Secret Chats](https://core.telegram.org/api/end-to-end)
- [Security Analysis of Telegram](https://mtpsym.github.io/)

---

## 9. Complete Self-Hosted Implementation Checklist

### Development Phase

- [ ] Create bot via @BotFather, save token securely
- [ ] Set up development environment (Python 3.10+, virtualenv)
- [ ] Install `python-telegram-bot`: `pip install python-telegram-bot[webhooks]`
- [ ] Create `.env` file (mode 600, add to `.gitignore`)
- [ ] Implement basic long polling bot for testing
- [ ] Add command handlers and test locally
- [ ] Implement chat_id whitelist with your user ID
- [ ] Test authentication and authorization

### Security Hardening

- [ ] Move token to environment variable or keyring
- [ ] Implement passcode-based authentication (if multi-user)
- [ ] Add input validation for all user inputs
- [ ] Implement command whitelist (restrict dangerous operations)
- [ ] Add rate limiting (per-user throttling)
- [ ] Set up audit logging (all commands, errors, auth attempts)
- [ ] Review OWASP Top 10 compliance
- [ ] Test with malicious inputs (command injection, path traversal)

### Production Deployment (Webhook)

- [ ] Obtain domain name and point DNS to server
- [ ] Set up server (Ubuntu 22.04 LTS recommended)
- [ ] Install dependencies: Python, nginx, certbot
- [ ] Generate Let's Encrypt certificate: `certbot certonly --standalone -d yourdomain.com`
- [ ] Create FastAPI webhook receiver
- [ ] Configure nginx reverse proxy with TLS
- [ ] Restrict nginx to Telegram IP ranges (optional but recommended)
- [ ] Create systemd service for FastAPI app
- [ ] Set webhook URL via Telegram API
- [ ] Test webhook with Telegram's webhook tester
- [ ] Monitor logs: `journalctl -u mybot -f`

### Monitoring & Maintenance

- [ ] Set up log rotation (logrotate)
- [ ] Configure alerts for service failures (systemd email notifications)
- [ ] Implement health check endpoint (`/health`)
- [ ] Monitor disk space, memory usage
- [ ] Set up automated backups (whitelist, config, logs)
- [ ] Schedule token rotation (every 6 months)
- [ ] Review and update dependencies monthly
- [ ] Test disaster recovery procedure

### Optional Enhancements

- [ ] Implement conversation state persistence (Redis, SQLite)
- [ ] Add inline keyboard menus
- [ ] Implement file upload/download handlers
- [ ] Add multi-language support (i18n)
- [ ] Integrate with external services (home automation, CI/CD)
- [ ] Implement metrics collection (Prometheus, Grafana)
- [ ] Add unit tests and integration tests
- [ ] Set up CI/CD pipeline for bot updates

---

## 10. Recommended Libraries & Tools

### Core Libraries

**python-telegram-bot** (official recommendation)
- Version: 22.6+ (async-native)
- Install: `pip install python-telegram-bot[webhooks]`
- Docs: https://docs.python-telegram-bot.org/
- GitHub: https://github.com/python-telegram-bot/python-telegram-bot

**Alternative: pyTelegramBotAPI**
- Lighter weight, simpler API
- Install: `pip install pyTelegramBotAPI`
- Good for simple bots

### Web Frameworks (Webhook)

**FastAPI** (recommended for modern async bots)
- Install: `pip install fastapi uvicorn`
- Excellent performance, automatic docs

**Flask** (simpler, more mature)
- Install: `pip install flask`
- Good for straightforward webhooks

### Security & Secrets

**python-dotenv** (environment variables)
- Install: `pip install python-dotenv`

**keyring** (system keyring integration)
- Install: `pip install keyring`

**cryptography** (encryption utilities)
- Install: `pip install cryptography`

### Utilities

**Redis** (distributed rate limiting, session storage)
- Install: `pip install redis`

**SQLAlchemy** (persistent storage)
- Install: `pip install sqlalchemy`

**APScheduler** (task scheduling)
- Install: `pip install apscheduler`

---

## 11. Common Pitfalls & Solutions

### Pitfall 1: Forgetting to answer callback queries

**Problem:** Inline keyboard buttons show infinite loading spinner.

**Solution:** Always call `await query.answer()` in callback handlers.

```python
async def button_callback(update, context):
    query = update.callback_query
    await query.answer()  # <- CRITICAL
    # ... rest of handler
```

### Pitfall 2: Webhook and polling active simultaneously

**Problem:** Bot receives duplicate updates or no updates.

**Solution:** Choose ONE method. If switching, delete webhook first.

```python
# Switching from webhook to polling
await bot.delete_webhook()
app.run_polling()

# Switching from polling to webhook
# Stop polling process first, then:
await bot.set_webhook(url="https://yourdomain.com/webhook")
```

### Pitfall 3: Ignoring rate limits

**Problem:** Bot gets throttled, messages fail to send.

**Solution:** Implement rate limiting (see Section 3).

### Pitfall 4: Large messages truncated

**Problem:** Messages over 4096 characters silently fail or error.

**Solution:** Split long messages or send as file.

```python
async def send_long_message(update, context, text):
    if len(text) <= 4096:
        await update.message.reply_text(text)
    else:
        # Send as file
        import io
        file = io.BytesIO(text.encode())
        file.name = "output.txt"
        await update.message.reply_document(document=file)
```

### Pitfall 5: Hardcoded tokens in git

**Problem:** Token exposed in version control.

**Solution:**
1. Revoke compromised token via @BotFather
2. Generate new token
3. Add token file to `.gitignore`
4. Use environment variables or keyring

```bash
# .gitignore
.env
*.env
config/secrets.json
```

### Pitfall 6: No error handling

**Problem:** Bot crashes on unexpected input.

**Solution:** Wrap handlers in try-except, log errors.

```python
async def safe_handler(update, context):
    try:
        # Handler logic
        pass
    except Exception as e:
        logger.error(f"Error in handler: {e}", exc_info=True)
        await update.message.reply_text("An error occurred. Please try again.")
```

### Pitfall 7: Webhook not receiving updates

**Checklist:**
- [ ] Webhook URL uses HTTPS
- [ ] Port is 443, 80, 88, or 8443
- [ ] Certificate is valid (or uploaded if self-signed)
- [ ] Firewall allows incoming traffic on webhook port
- [ ] Nginx/proxy correctly forwards to backend
- [ ] No long polling active simultaneously
- [ ] Check webhook info: `await bot.get_webhook_info()`

```python
info = await bot.get_webhook_info()
print(f"Webhook URL: {info.url}")
print(f"Pending updates: {info.pending_update_count}")
print(f"Last error: {info.last_error_message}")
```

---

## 12. Testing & Debugging

### Local Testing

**Use long polling for development:**

```python
if __name__ == '__main__':
    app = Application.builder().token("BOT_TOKEN").build()

    # Add handlers...

    # Development: long polling
    app.run_polling()
```

**Enable debug logging:**

```python
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
```

### Webhook Testing

**Use ngrok for local webhook testing:**

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Start your bot locally on port 8000
python bot.py &

# Expose port 8000
ngrok http 8000

# Use the HTTPS URL from ngrok
# Example: https://abc123.ngrok.io
```

```python
await bot.set_webhook(url="https://abc123.ngrok.io/webhook")
```

### Manual API Testing

**Send test message via curl:**

```bash
curl -X POST https://api.telegram.org/bot<TOKEN>/sendMessage \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "YOUR_CHAT_ID", "text": "Test message"}'
```

**Get webhook info:**

```bash
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```

**Delete webhook:**

```bash
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
```

---

## 13. Resources & Further Reading

### Official Documentation

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Bots FAQ](https://core.telegram.org/bots/faq)
- [Webhook Guide](https://core.telegram.org/bots/webhooks)
- [Bot API Changelog](https://core.telegram.org/bots/api-changelog)
- [MTProto Protocol](https://core.telegram.org/mtproto)

### Python Libraries

- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [python-telegram-bot GitHub](https://github.com/python-telegram-bot/python-telegram-bot)
- [python-telegram-bot Examples](https://docs.python-telegram-bot.org/en/stable/examples.html)
- [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)

### Security Resources

- [How to secure a Telegram bot](https://bazucompany.com/blog/how-to-secure-a-telegram-bot-best-practices/)
- [Telegram bot security solutions](https://medium.com/@bioogrami7/telegram-bot-security-solutions-6c5b8105a0e1)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Security Guidelines for Client Developers](https://core.telegram.org/mtproto/security_guidelines)

### Implementation Examples

- [fastapi-security-telegram-webhook](https://github.com/b0g3r/fastapi-security-telegram-webhook)
- [Hosting multiple bots with NGINX](https://madhead.me/posts/nginx-tg-bots/)
- [Telegram bot with FastAPI](https://salaivv.com/2023/01/04/telegram-bot-fastapi)
- [Home Assistant Telegram integration](https://www.home-assistant.io/integrations/telegram_bot/)

### Community & Support

- [python-telegram-bot Telegram Group](https://t.me/pythontelegrambotgroup)
- [r/TelegramBots](https://www.reddit.com/r/TelegramBots/)
- Stack Overflow: `[telegram-bot]` tag

---

## Appendix A: Quick Reference

### Common Bot Methods

```python
# Send text message
await bot.send_message(chat_id=123, text="Hello")

# Send message with Markdown
await bot.send_message(chat_id=123, text="*Bold* _italic_", parse_mode="Markdown")

# Send photo
await bot.send_photo(chat_id=123, photo=open('image.jpg', 'rb'))

# Send document
await bot.send_document(chat_id=123, document=open('file.pdf', 'rb'))

# Edit message
await bot.edit_message_text(
    chat_id=123,
    message_id=456,
    text="Updated text"
)

# Delete message
await bot.delete_message(chat_id=123, message_id=456)

# Set webhook
await bot.set_webhook(url="https://example.com/webhook")

# Delete webhook
await bot.delete_webhook()

# Get webhook info
info = await bot.get_webhook_info()
```

### Handler Types

```python
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

# Command handler (/start, /help, etc.)
app.add_handler(CommandHandler("start", start_callback))

# Message handler (all text messages)
app.add_handler(MessageHandler(filters.TEXT, text_callback))

# Photo handler
app.add_handler(MessageHandler(filters.PHOTO, photo_callback))

# Document handler
app.add_handler(MessageHandler(filters.Document.ALL, document_callback))

# Callback query handler (inline keyboard buttons)
app.add_handler(CallbackQueryHandler(button_callback))

# Conversation handler (multi-step dialogs)
app.add_handler(ConversationHandler(...))
```

### Common Filters

```python
from telegram.ext import filters

filters.TEXT           # Text messages (not commands)
filters.COMMAND        # Commands (/start, /help)
filters.PHOTO          # Photos
filters.Document.ALL   # All documents
filters.VIDEO          # Videos
filters.VOICE          # Voice messages
filters.Regex(r'^\d+$')  # Regex pattern matching
filters.User(user_id=123)  # Specific user
filters.ChatType.PRIVATE   # Private chats only
filters.ChatType.GROUPS    # Group chats only
```

---

## Appendix B: Environment Variables Template

```bash
# .env
# Bot configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BOT_OWNER_ID=123456789
ALLOWED_CHAT_IDS=123456789,987654321

# Authentication
ENROLLMENT_PASSCODE=your-secure-passcode-here
SESSION_TIMEOUT=3600

# Webhook configuration (if using webhook)
WEBHOOK_URL=https://yourdomain.com/webhook
WEBHOOK_PORT=8443

# External services (if applicable)
DATABASE_URL=sqlite:///bot.db
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/mybot/bot.log
```

**Load in Python:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_ID = int(os.getenv("BOT_OWNER_ID"))
ALLOWED_IDS = set(map(int, os.getenv("ALLOWED_CHAT_IDS").split(',')))
```

---

## Appendix C: Systemd Service Template

```ini
# /etc/systemd/system/telegram-bot.service

[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=botuser
Group=botuser
WorkingDirectory=/opt/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
EnvironmentFile=/opt/telegram-bot/.env
ExecStart=/opt/telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/telegram-bot/data

[Install]
WantedBy=multi-user.target
```

**Commands:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable telegram-bot

# Start service
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f

# Restart service
sudo systemctl restart telegram-bot

# Stop service
sudo systemctl stop telegram-bot
```

---

**End of Guide**

Authored by Rowan Valle
Executed by Claude Code
Symbiont Systems LLC
2026-02-08
