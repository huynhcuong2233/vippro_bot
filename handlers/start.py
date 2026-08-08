from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


# ==============================
# BANNER
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
BANNER_PATH = BASE_DIR / "banner.jpg"


# ==============================
# /START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    first_name = user.first_name or "Bạn"

    keyboard = [
        [
            InlineKeyboardButton(
                "🎮 LIÊN QUÂN",
                callback_data="lienquan"
            ),
            InlineKeyboardButton(
                "🔥 FREE FIRE",
                callback_data="freefire"
            ),
        ],
        [
            InlineKeyboardButton(
                "💳 NẠP TIỀN",
                callback_data="deposit"
            ),
        ],
        [
            InlineKeyboardButton(
                "📞 LIÊN HỆ ADMIN",
                callback_data="contact"
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = f"""
🌸 <b>HCUONGIOS SIÊU VIP</b> 🌸

👋 Xin chào <b>{first_name}</b>!

💎 Chào mừng bạn đến với hệ thống.

━━━━━━━━━━━━━━━━━━
🎮 <b>LIÊN QUÂN MOBILE</b>
🔥 <b>FREE FIRE</b>
💳 <b>NẠP TIỀN</b>
📞 <b>HỖ TRỢ ADMIN</b>
━━━━━━━━━━━━━━━━━━

⚡ Nhanh chóng
🔐 Uy tín
💰 Giá tốt

👇 <b>CHỌN CHỨC NĂNG BÊN DƯỚI</b>
"""

    try:

        if BANNER_PATH.exists():

            with open(BANNER_PATH, "rb") as photo:

                await update.message.reply_photo(
                    photo=photo,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=reply_markup,
                )

        else:

            print(f"⚠️ Không tìm thấy banner: {BANNER_PATH}")

            await update.message.reply_text(
                caption,
                parse_mode="HTML",
                reply_markup=reply_markup,
            )

    except Exception as e:

        print(f"❌ START ERROR: {repr(e)}")

        await update.message.reply_text(
            caption,
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
