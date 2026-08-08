from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("💳 Nạp tiền", callback_data="deposit"),
            InlineKeyboardButton("🛒 Mua KEY", callback_data="buy_key")
        ],
        [
            InlineKeyboardButton("📥 Tải file", callback_data="download"),
            InlineKeyboardButton("👑 VIP STORE", callback_data="vip_store")
        ],
        [
            InlineKeyboardButton("☎️ Liên hệ", callback_data="contact")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = """
👑 <b>HCUONGIOS VIP STORE</b>

🔥 Shop dịch vụ iOS Gaming Premium

🍎 iOS
💳 Nạp tiền tự động
🛒 Mua KEY
📥 Tải file

🟢 <b>ONLINE 24/7</b>

Chọn chức năng bên dưới 👇
"""

    with open("banner.jpg", "rb") as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
