from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)

from telegram.ext import ContextTypes

import os
import qrcode

from database import (
    get_balance,
    remove_balance,
    create_order,
    get_available_key,
    use_key,
)

from momo import create_deposit_code


# ==========================
# TẠO QR
# ==========================

def create_qr(user_id):

    momo_number = "0375942325"
    name = "THACH HUYNH CUONG"

    content = f"HCUONGIOS {user_id}"

    qr_data = f"""
MoMo
PHONE:{momo_number}
NAME:{name}
CONTENT:{content}
"""

    qr = qrcode.make(qr_data)

    os.makedirs("assets", exist_ok=True)

    path = f"assets/momo_{user_id}.png"

    qr.save(path)

    return path


# ==========================
# MENU CHÍNH
# ==========================

async def main_menu(update, context):

    keyboard = [

    [
        InlineKeyboardButton(
            "👤 Tài khoản",
            callback_data="account"
        ),

        InlineKeyboardButton(
            "🛒 Cửa hàng",
            callback_data="shop"
        )
    ],

    [
        InlineKeyboardButton(
            "💳 Nạp tiền",
            callback_data="deposit"
        ),

        InlineKeyboardButton(
            "🔑 KEY của tôi",
            callback_data="mykey"
        )
    ],

    [
        InlineKeyboardButton(
            "📜 Lịch sử",
            callback_data="history"
        ),

        InlineKeyboardButton(
            "📥 Tải file",
            callback_data="download"
        )
    ],

    [
        InlineKeyboardButton(
            "☎️ Hỗ trợ",
            callback_data="support"
        )
    ]
]

    text = f"""
🏪 <b>HCUONGIOS PREMIUM</b>

━━━━━━━━━━━━━━━━━━

👋 Hcuongios Premium Xin chào
<b>{update.effective_user.first_name or 'Bạn'}</b>

💎 Bán mọi loại hack
⚡ Shop tự động
🛡️ Nhanh Gọn Lẹ
🔥 Giá tốt mỗi ngày

━━━━━━━━━━━━━━━━━━

👇 Chọn chức năng bên dưới.
"""

    if update.message:

        await update.message.reply_text(
            text=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    else:

        await update.callback_query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
# ==========================
# CALLBACK BUTTON
# ==========================

async def buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    # ==========================
    # TÀI KHOẢN
    # ==========================

    if query.data == "account":

        balance = get_balance(
            query.from_user.id
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            f"""
👤 <b>TÀI KHOẢN</b>

━━━━━━━━━━━━━━

🆔 ID:
<code>{query.from_user.id}</code>

💰 Số dư:
<b>{balance:,}đ</b>

━━━━━━━━━━━━━━
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    elif query.data == "shop":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔥 FF MIGUL • VN",
                    callback_data="product_ff"
                )
            ],
            [
                InlineKeyboardButton(
                    "⚔️ Liên Quân iOS",
                    callback_data="product_lq"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎮 PUBG iOS",
                    callback_data="product_pubg"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎱 8 Ball Pool",
                    callback_data="product_8ball"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            """
🛒 <b>CỬA HÀNG HCUONGIOS</b>

👇 Chọn sản phẩm:
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # FF MIGUL
    # ==========================

    elif query.data == "product_ff":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⭐ Migul Lite - VN",
                    callback_data="product_migul_lite"
                )
            ],
            [
                InlineKeyboardButton(
                    "👑 Migul Pro - VN",
                    callback_data="product_migul_pro"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="shop"
                )
            ]
        ]

        await query.edit_message_text(
            """
🔥 <b>FF MIGUL • VN</b>

📦 <b>DANH MỤC: Migul FreeFire</b>

Chọn sản phẩm:
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==========================
    # MIGUL LITE
    # ==========================

    elif query.data == "product_migul_lite":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⏱️ 1 ngày | 50.000đ",
                    callback_data="buy_migul_lite_1d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱️ 7 ngày | 150.000đ",
                    callback_data="buy_migul_lite_7d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱️ 30 ngày | 350.000đ",
                    callback_data="buy_migul_lite_30d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="product_ff"
                )
            ]
        ]

        await query.edit_message_text(
            """
⭐ <b>MIGUL LITE - VN</b>

🔥 Migul FF Lite dành cho khách hàng VN

📱 Cài đặt IPA
✅ Hỗ trợ iOS 16 - 26.6

🚀 Giao hàng: Tự động

💰 Chọn thời hạn:
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # MIGUL PRO
    # ==========================

    elif query.data == "product_migul_pro":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⏱️ 1 giờ | 10.000đ",
                    callback_data="buy_migul_pro_1h"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱️ 1 ngày | 65.000đ",
                    callback_data="buy_migul_pro_1d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱️ 7 ngày | 215.000đ",
                    callback_data="buy_migul_pro_7d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏱️ 30 ngày | 450.000đ",
                    callback_data="buy_migul_pro_30d"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="product_ff"
                )
            ]
        ]

        await query.edit_message_text(
            """
👑 <b>MIGUL PRO - VN</b>

🔥 Migul FF Pro dành cho khách hàng VN

📱 Cài đặt IPA
✅ Hỗ trợ iOS 16 - 26.6

🚀 Giao hàng: Tự động

💰 Chọn thời hạn:
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # LIÊN QUÂN
    # ==========================

    elif query.data == "product_lq":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⚔️ Liên Quân iOS | 150.000đ",
                    callback_data="buy_lq"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="shop"
                )
            ]
        ]

        await query.edit_message_text(
            """
⚔️ <b>LIÊN QUÂN iOS</b>

💰 Giá: <b>150.000đ</b>

🛡️ Bảo hành
⚡ Kích hoạt tự động
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # PUBG
    # ==========================

    elif query.data == "product_pubg":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎮 PUBG Dolphin | 180.000đ",
                    callback_data="buy_pubg"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="shop"
                )
            ]
        ]

        await query.edit_message_text(
            """
🎮 <b>PUBG DOLPHIN iOS</b>

💰 Giá: <b>180.000đ</b>

⚡ Hỗ trợ iPhone
🛡️ Bảo hành
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # 8 BALL
    # ==========================

    elif query.data == "product_8ball":

        keyboard = [
            [
                InlineKeyboardButton(
                    "🎱 8 Ball Pool | 120.000đ",
                    callback_data="buy_8ball"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="shop"
                )
            ]
        ]

        await query.edit_message_text(
            """
🎱 <b>8 BALL POOL iOS</b>

💰 Giá: <b>120.000đ</b>
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    # ==========================
    # NẠP TIỀN MOMO
    # ==========================

    elif query.data == "deposit":

        user_id = query.from_user.id

        code = create_deposit_code(user_id)

        text = f"""

💰 <b>NẠP TIỀN QUA MOMO</b>

📱 Ví MoMo:

0375942325

👤 Chủ ví:

THACH HUYNH CUONG

💵 Nội dung chuyển khoản:

<code>{code}</code>

⚠️ Vui lòng ghi đúng nội dung.

"""

        keyboard = [

            [

                InlineKeyboardButton(

                    "✅ Tôi đã chuyển tiền",

                    callback_data="check_payment"

                )

            ],

            [

                InlineKeyboardButton(

                    "⬅️ Quay lại",

                    callback_data="home"

                )

            ]

        ]

        qr_path = create_qr(user_id)

        with open(qr_path, "rb") as photo:

            await query.message.reply_photo(

                photo=photo,

                caption=text,

                parse_mode="HTML",

                reply_markup=InlineKeyboardMarkup(keyboard)

            )

        await query.delete_message()
    # ==========================
    # KIỂM TRA THANH TOÁN
    # ==========================

    elif query.data == "check_payment":

        await query.answer(
            "⏳ Đã gửi yêu cầu kiểm tra. Chờ admin xác nhận.",
            show_alert=True
        )

    # ==========================
    # LỊCH SỬ
    # ==========================

    elif query.data == "history":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            """
📜 <b>LỊCH SỬ GIAO DỊCH</b>

━━━━━━━━━━━━━━

❌ Chưa có giao dịch.

━━━━━━━━━━━━━━
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ==========================
    # HỖ TRỢ
    # ==========================

    elif query.data == "support":

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="home"
                )
            ]
        ]

        await query.edit_message_text(
            """
☎️ <b>HỖ TRỢ KHÁCH HÀNG</b>

👤 Admin:
@thuynhcuong2510

⏰ Online mỗi ngày.
""",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ==========================
    # HOME
    # ==========================

    elif query.data == "home":

        await main_menu(update, context)


    # ==========================
    # MUA SẢN PHẨM
    # ==========================

    elif query.data.startswith("buy_"):

        products = {
            "buy_lq": ("Liên Quân iOS", 150000),
            "buy_pubg": ("PUBG Dolphin iOS", 180000),
            "buy_8ball": ("8 Ball Pool iOS", 120000),
            "buy_migul_lite_1d": ("Migul Lite VN - 1 ngày", 50000),
            "buy_migul_lite_7d": ("Migul Lite VN - 7 ngày", 150000),
            "buy_migul_lite_30d": ("Migul Lite VN - 30 ngày", 350000),
            "buy_migul_pro_1h": ("Migul Pro VN - 1 giờ", 10000),
            "buy_migul_pro_1d": ("Migul Pro VN - 1 ngày", 65000),
            "buy_migul_pro_7d": ("Migul Pro VN - 7 ngày", 215000),
            "buy_migul_pro_30d": ("Migul Pro VN - 30 ngày", 450000),
        }

        if query.data not in products:
            await query.answer(
                "❌ Sản phẩm không tồn tại",
                show_alert=True
            )
            return

        product_name, price = products[query.data]
        balance = get_balance(
            query.from_user.id
        )

        if balance < price:

            await query.answer(
                "❌ Số dư không đủ.",
                show_alert=True
            )
            return


        remove_balance(
            query.from_user.id,
            price
        )


        # Xác định loại key

        if "Migul Pro" in product_name:
            plan = "PRO"

        else:
            plan = "BASIC"


        key_data = get_available_key(plan)


        if not key_data:

            await query.answer(
                "❌ Sản phẩm đã hết key.",
                show_alert=True
            )

            return


        key_id, api_key = key_data


        use_key(
            key_id,
            query.from_user.id
        )


        create_order(
            query.from_user.id,
            product_name,
            price,
            api_key
        )


        await query.edit_message_text(
            f"""
✅ <b>MUA THÀNH CÔNG</b>

📦 Sản phẩm:
<b>{product_name}</b>

💰 Giá:
<b>{price:,}đ</b>

🔑 API KEY:

<code>{api_key}</code>
""",
            parse_mode="HTML"
        )
    elif query.data == "download":

        text = """
    📥 <b>TRUNG TÂM TẢI FILE</b>

    🎮 Chọn game cần tải:
    """

        keyboard = [
            [InlineKeyboardButton("🔥 Free Fire", callback_data="ff")],
            [InlineKeyboardButton("🎯 PUBG Mobile", callback_data="pubg")],
            [InlineKeyboardButton("⚔️ Liên Quân Mobile", callback_data="lq")],
            [InlineKeyboardButton("⬅️ Quay lại", callback_data="home")],
        ]

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


    elif query.data == "ff":

        await query.edit_message_text(
            """
    🔥 <b>FREE FIRE</b>

    📥 Link tải:

    https://link-cua-ban.com/FreeFire.ipa
    """,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📥 Tải ngay",
                        url="https://link-cua-ban.com/FreeFire.ipa"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Quay lại",
                        callback_data="download"
                    )
                ]
            ])
        )


    elif query.data == "pubg":

        await query.edit_message_text(
        """
    🎯 <b>PUBG MOBILE</b>

    📥 Link tải:

    https://link-cua-ban.com/PUBG.ipa
    """,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📥 Tải ngay",
                    url="https://link-cua-ban.com/PUBG.ipa"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="download"
                )
            ]
        ])
    )


    elif query.data == "lq":

        await query.edit_message_text(
        """
    ⚔️ <b>LIÊN QUÂN MOBILE</b>

    📥 Link tải:

    https://link-cua-ban.com/LienQuan.ipa
    """,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📥 Tải ngay",
                    url="https://link-cua-ban.com/LienQuan.ipa"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Quay lại",
                    callback_data="download"
                )
            ]
        ])
    )

    else:

        await query.answer(
            "🚧 Chức năng đang cập nhật.",
            show_alert=True
        )
