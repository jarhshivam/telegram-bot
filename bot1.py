# ==========================================
# 🌈 ALL IN ONE COLORFUL PREMIUM BOT
# 👑 Made by Shivam Yaduvanshi
# For Python IDLE (PC/Laptop)
# Install first:
# pip install python-telegram-bot requests qrcode[pil]
# ==========================================

import logging
import requests
import qrcode
from io import BytesIO

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

# ==========================================
# 🎯 CONFIG
# ==========================================
BOT_TOKEN = "8348259289:AAFP-9Z9aRJQl7A-FHhDi5GBJv5ciGb5Nmw"
IP_API = "http://ip-api.com/json/"
CHANNEL_LINK = "https://t.me/+zkQo51W4z3VkNjRl"

# ==========================================
# 📘 LOGGING
# ==========================================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==========================================
# CHANNEL BUTTON
# ==========================================
def channel_button():
    keyboard = [
        [InlineKeyboardButton("📢 Join Official Channel", url=CHANNEL_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)

# ==========================================
# 🚀 START
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = """
🌈🔥 WELCOME TO PREMIUM BOT 🔥🌈

👑 Owner: Shivam Yaduvanshi

🛠 Commands:

🌍 /ip 8.8.8.8
🔳 /qr hello
🧮 /calc 5+5*2
📘 /help

📢 Join our official channel below.
"""
    await update.message.reply_text(
        txt,
        reply_markup=channel_button()
    )

# ==========================================
# 📘 HELP
# ==========================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
📌 COMMAND LIST

🌍 /ip <ip>
🔳 /qr <text>
🧮 /calc <math>
🚀 /start
"""
    )

# ==========================================
# 🌍 IP LOOKUP
# ==========================================
async def ip_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /ip 8.8.8.8")
        return

    ip = context.args[0]
    msg = await update.message.reply_text("🔍 Scanning IP...")

    try:
        r = requests.get(IP_API + ip, timeout=10)
        data = r.json()

        text = f"""
🌍 IP INFORMATION

🧾 IP: {data.get("query")}
🌎 Country: {data.get("country")}
🏙 City: {data.get("city")}
📍 Region: {data.get("regionName")}
📡 ISP: {data.get("isp")}
⏰ Timezone: {data.get("timezone")}
✅ Status: {data.get("status")}
"""
        await msg.edit_text(text)

    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")

# ==========================================
# 🔳 QR GENERATOR
# ==========================================
async def make_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /qr hello")
        return

    text = " ".join(context.args)

    img = qrcode.make(text)

    bio = BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)

    await update.message.reply_photo(
        photo=bio,
        caption="🔳 Your QR Code is Ready!"
    )

# ==========================================
# 🧮 CALCULATOR
# ==========================================
async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /calc 5+5")
        return

    exp = "".join(context.args)

    try:
        result = eval(exp)
        await update.message.reply_text(
            f"""
🧮 RESULT

📥 Expression: {exp}
✅ Answer: {result}
"""
        )
    except:
        await update.message.reply_text("❌ Invalid Expression")

# ==========================================
# 💬 NORMAL MESSAGE
# ==========================================
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌈 Use commands.\n📘 Type /help",
        reply_markup=channel_button()
    )

# ==========================================
# 🔥 MAIN
# ==========================================
def main():
    print("🌈 Premium Bot Running in IDLE...")
    print("👑 Made by Shivam Yaduvanshi")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ip", ip_lookup))
    app.add_handler(CommandHandler("qr", make_qr))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

# ==========================================
# ▶ RUN
# ==========================================
if __name__ == "__main__":
    main()