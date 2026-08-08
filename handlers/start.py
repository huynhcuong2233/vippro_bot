from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes


# =========================================================
# ĐƯỜNG DẪN PROJECT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# File banner phải nằm tại:
# src/banner.jpg
BANNER_PATH = BASE_DIR / "banner.jpg"


# =========================================================
# /START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Tên người dùng
    first_name = user.first_name or "bạn"

    # =====================================================
    # MENU
    # =====================================================

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

    # =====================================================
    # NỘI DUNG START
    # =====================================================

    caption = f"""
🌸 <b>HCUONGIOS SIÊU VIP</b> 🌸

👋 Xin chào <b>{first_name}</b>!

💎 Chào mừng bạn đến với hệ thống HCUONGIOS.

🎮 <b>DỊCH VỤ</b>
━━━━━━━━━━━━━━━━━━
🎮 Liên Quân Mobile
🔥 Free Fire
💳 Nạp tiền tự động
📞 Hỗ trợ khách hàng
━━━━━━━━━━━━━━━━━━

⚡ <b>Hệ thống hoạt động tự động</b>
🔐 Nhanh chóng • Uy tín • An toàn

👇 <b>Vui lòng chọn chức năng:</b>
"""

    # =====================================================
    # GỬI BANNER
    # =====================================================

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

            # Không có banner thì vẫn cho bot chạy
            await update.message.reply_text(
                caption,
                parse_mode="HTML",
                reply_markup=reply_markup,
            )

    except Exception as e:

        print(f"[START ERROR] {e}")

        # Nếu gửi ảnh lỗi thì gửi dạng text
        await update.message.reply_text(
            caption,
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
