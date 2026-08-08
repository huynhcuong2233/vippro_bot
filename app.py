import os
import asyncio
from flask import Flask, request

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes,
)

from handlers.start import start
from handlers.buttons import buttons
from handlers.admin import admin_handlers
from database import setup_database

setup_database()

TOKEN = os.environ["BOT_TOKEN"]

app = Flask(__name__)

@app.route("/")
def home():
    return "HCUONGIOS VIP BOT ONLINE"

tg = Application.builder().token(TOKEN).build()


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 <b>HCUONGIOS VIP</b>\n\n"
        "/start - Mở menu\n"
        "/help - Trợ giúp\n"
        "/id - Lấy ID\n"
        "/ping - Kiểm tra bot\n"
        "/shop - Cửa hàng\n"
        "/contact - Liên hệ",
        parse_mode="HTML",
    )


async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 ID Telegram:\n{update.effective_user.id}")


async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!\n✅ Bot đang online")


async def shop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 MUA API KEY", callback_data="shop")],
        [
            InlineKeyboardButton("💳 THANH TOÁN", callback_data="deposit"),
            InlineKeyboardButton("👤 HỖ TRỢ", callback_data="support"),
        ],
    ]
    await update.message.reply_text(
        "⭐ HCUONGIOS VIP ⭐\n\n"
        "🚀 Premium API Services\n"
        "🔐 Key chất lượng cao\n"
        "⚡ Kích hoạt nhanh",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def contact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Admin:\n@thuynhcuong2510")


async def welcome_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.chat_member:
        return

    member = update.chat_member
    old = member.old_chat_member.status
    new = member.new_chat_member.status

    if old in ("left", "kicked") and new == "member":
        user = member.new_chat_member.user
        await context.bot.send_message(
            chat_id=member.chat.id,
            text=(
                "🎉 <b>CHÀO MỪNG THÀNH VIÊN MỚI</b>\n\n"
                f"👤 Xin chào {user.first_name}\n"
                "🔥 Chào mừng đến với HCUONGIOS VIP\n\n"
                "👉 Gõ /start để mở menu"
            ),
            parse_mode="HTML",
        )


tg.add_handler(CommandHandler("start", start))
tg.add_handler(CommandHandler("help", help_cmd))
tg.add_handler(CommandHandler("id", id_cmd))
tg.add_handler(CommandHandler("ping", ping_cmd))
tg.add_handler(CommandHandler("shop", shop_cmd))
tg.add_handler(CommandHandler("contact", contact_cmd))
tg.add_handler(CallbackQueryHandler(buttons))

for handler in admin_handlers():
    tg.add_handler(handler)

tg.add_handler(
    ChatMemberHandler(welcome_member, ChatMemberHandler.CHAT_MEMBER)
)

_bot_lock = asyncio.Lock()
_bot_initialized = False


async def initialize_bot():
    global _bot_initialized

    async with _bot_lock:
        if not _bot_initialized:
            await tg.initialize()
            await tg.start()
            _bot_initialized = True


@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        await initialize_bot()

        data = request.get_json(force=True)
        if not data:
            return "bad request", 400

        print("📩 TELEGRAM UPDATE:", data)

        update = Update.de_json(data, tg.bot)
        await tg.process_update(update)

        print("✅ UPDATE PROCESSED")
        return "ok", 200

    except Exception as e:
        print("❌ WEBHOOK ERROR:", repr(e))
        return "error", 500


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
