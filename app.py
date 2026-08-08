import os
import asyncio

from flask import Flask, request

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ChatMemberHandler,
    ContextTypes
)

from handlers.start import start
from handlers.buttons import buttons
from handlers.admin import admin_handlers

from database import setup_database


# ==========================
# DATABASE
# ==========================

setup_database()


# ==========================
# TOKEN
# ==========================

TOKEN = os.environ["BOT_TOKEN"]


# ==========================
# FLASK
# ==========================

app = Flask(__name__)


@app.route("/")
def home():
    return "✅ HCUONGIOS VIP BOT ONLINE"


# ==========================
# TELEGRAM APPLICATION
# ==========================

tg = Application.builder().token(TOKEN).build()


# ==========================
# WELCOME MEMBER
# ==========================

async def welcome_member(update, context):

    if not update.chat_member:
        return

    member = update.chat_member

    old = member.old_chat_member.status
    new = member.new_chat_member.status

    if old in ["left", "kicked"] and new == "member":

        user = member.new_chat_member.user

        await context.bot.send_message(
            chat_id=member.chat.id,
            text=(
                "🎉 <b>CHÀO MỪNG THÀNH VIÊN MỚI</b>\n\n"
                f"👤 Xin chào {user.first_name}\n"
                "🔥 Chào mừng đến với HCUONGIOS VIP\n\n"
                "👉 Gõ /start để mở menu"
            ),
            parse_mode="HTML"
        )


# ==========================
# COMMANDS
# ==========================

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📌 <b>HCUONGIOS VIP</b>\n\n"
        "/start - Mở menu\n"
        "/help - Trợ giúp\n"
        "/id - Lấy ID\n"
        "/ping - Kiểm tra bot\n"
        "/shop - Cửa hàng\n"
        "/contact - Liên hệ",
        parse_mode="HTML"
    )


async def id_cmd(update: Update, context):

    await update.message.reply_text(
        f"🆔 ID Telegram:\n{update.effective_user.id}"
    )


async def ping_cmd(update: Update, context):

    await update.message.reply_text(
        "🏓 Pong!\n✅ Bot đang online"
    )


async def shop_cmd(update: Update, context):

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 MUA API KEY",
                callback_data="shop"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 THANH TOÁN",
                callback_data="deposit"
            ),
            InlineKeyboardButton(
                "👤 HỖ TRỢ",
                callback_data="support"
            )
        ]
    ]

    await update.message.reply_text(
        "⭐ HCUONGIOS VIP ⭐\n\n"
        "🚀 Premium API Services\n"
        "🔐 Key chất lượng cao\n"
        "⚡ Kích hoạt nhanh",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def contact_cmd(update: Update, context):

    await update.message.reply_text(
        "👤 Admin:\n@thuynhcuong2510"
    )


# ==========================
# ADD HANDLER
# ==========================

tg.add_handler(
    CommandHandler(
        "start",
        start
    )
)


tg.add_handler(
    CommandHandler(
        "help",
        help_cmd
    )
)


tg.add_handler(
    CommandHandler(
        "id",
        id_cmd
    )
)


tg.add_handler(
    CommandHandler(
        "ping",
        ping_cmd
    )
)


tg.add_handler(
    CommandHandler(
        "shop",
        shop_cmd
    )
)


tg.add_handler(
    CommandHandler(
        "contact",
        contact_cmd
    )
)


tg.add_handler(
    CallbackQueryHandler(buttons)
)


for handler in admin_handlers():
    tg.add_handler(handler)


tg.add_handler(
    ChatMemberHandler(
        welcome_member,
        ChatMemberHandler.CHAT_MEMBER
    )
)


# ==========================
# INIT BOT
# ==========================

@app.before_request
def init_bot():

    if not getattr(app, "bot_ready", False):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(
            tg.initialize()
        )

        loop.run_until_complete(
            tg.start()
        )

        app.bot_ready = True


# ==========================
# WEBHOOK
# ==========================

@app.route(
    "/webhook",
    methods=["POST"]
)
async def webhook():

    try:

        data = request.get_json(force=True)

        print(
            "📩 TELEGRAM UPDATE:",
            data
        )

        update = Update.de_json(
            data,
            tg.bot
        )

        await tg.process_update(update)

        print(
            "✅ UPDATE PROCESSED"
        )

        return "ok", 200


    except Exception as e:

        print(
            "❌ WEBHOOK ERROR:",
            repr(e)
        )

        return "error", 500



# ==========================
# RUN
# ==========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )
