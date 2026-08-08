from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


# ==========================================
# BANNER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
BANNER_PATH = BASE_DIR / "banner.jpg"


# ==========================================
# /START
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user
    first_name = user.first_name or "Bạn"

    # ======================================
    # MENU
    # callback_data phải khớp buttons.py
    # ======================================

    keyboard = [
        [
            InlineKeyboardButton(
                "⚔️ LIÊN QUÂN",
                callback_data="product_lq"
            ),
            InlineKeyboardButton(
                "🔥 FREE FIRE",
                callback_data="product_ff"
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
                "🛒 CỬA HÀNG",
                callback_data="shop"
            ),
            InlineKeyboardButton(
                "☎️ HỖ TRỢ",
                callback_data="support"
            ),
        ],

        [
            InlineKeyboardButton(
                "👤 TÀI KHOẢN",
                callback_data="account"
            ),
            InlineKeyboardButton(
                "📜 LỊCH SỬ",
                callback_data="history"
            ),
        ],

        [
            InlineKeyboardButton(
                "📥 TẢI FILE",
                callback_data="download"
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # ======================================
    # NỘI DUNG
    # ======================================

    caption = f"""
🌸 <b>HCUONGIOS PREMIUM</b> 🌸

👋 Xin chào <b>{first_name}</b>!

💎 Chào mừng bạn đến với hệ thống
<b>HCUONGIOS PREMIUM</b>

━━━━━━━━━━━━━━━━━━

🎮 Liên Quân Mobile
🔥 Free Fire
🛒 Cửa hàng
💳 Nạp tiền
🔑 Quản lý KEY
📥 Tải file

━━━━━━━━━━━━━━━━━━

⚡ <b>Giao hàng nhanh</b>
🔐 <b>Uy tín</b>
💰 <b>Giá tốt</b>

👇 <b>CHỌN CHỨC NĂNG</b>
"""

    # ======================================
    # GỬI BANNER
    # ======================================

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

            print(
                f"⚠️ Không tìm thấy banner: {BANNER_PATH}"
            )

            await update.message.reply_text(
                text=caption,
                parse_mode="HTML",
                reply_markup=reply_markup,
            )

    except Exception as e:

        print(
            f"❌ START ERROR: {repr(e)}"
        )

        await update.message.reply_text(
            text=caption,
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
