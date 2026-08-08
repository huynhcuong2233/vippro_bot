from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from database import (
    confirm_deposit,
    add_key,
    count_stock,
)

ADMIN_ID = 8155433329  # Đổi thành Telegram ID của bạn


async def approve_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ Bạn không có quyền."
        )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
            "Cách dùng:\n/duyet MÃ_NẠP"
        )
        return
    content = context.args[0]

    result = confirm_deposit(content)

    if not result:
        await update.message.reply_text(
            "❌ Không tìm thấy mã nạp hoặc đã duyệt."
        )
        return

    user_id, amount = result

    await update.message.reply_text(
        f"""✅ Đã duyệt nạp

👤 User: {user_id}

💰 +{amount:,}đ"""
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=f"""🎉 Nạp tiền thành công!

💰 +{amount:,}đ

Số dư đã được cộng vào tài khoản."""
    )


async def addkey_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Ví dụ:\n/addkey BASIC ABCD-1234\n/addkey PRO XXXX-YYYY"
        )
        return

    plan = context.args[0].upper()
    api_key = context.args[1]

    try:
        add_key(plan, api_key)
        await update.message.reply_text("✅ Thêm API Key thành công.")
    except Exception as e:
        await update.message.reply_text(str(e))


async def stock_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    basic = count_stock("BASIC")
    pro = count_stock("PRO")

    await update.message.reply_text(
        f"""📦 Kho API KEY

BASIC : {basic}

PRO : {pro}
"""
    )


def admin_handlers():

    return [
        CommandHandler("duyet", approve_deposit),
        CommandHandler("addkey", addkey_cmd),
        CommandHandler("stock", stock_cmd),
    ]
