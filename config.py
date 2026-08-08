import os
# =========================
# TELEGRAM
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Telegram ID của admin
ADMIN_ID = int(os.getenv("ADMIN_ID", "8155433329"))
# =========================
# DATABASE
# =========================
DATABASE_NAME = "database.db"
# =========================
# VIETCOMBANK
# =========================
BANK_NAME = "VIETCOMBANK"
BANK_CODE = "VCB"
ACCOUNT_NUMBER = "1052960029"
ACCOUNT_NAME = "THACH HUYNH CUONG"
# =========================
# SEPAY
# =========================
SEPAY_API_KEY = os.getenv("SEPAY_API_KEY", "")
SEPAY_WEBHOOK_SECRET = os.getenv("SEPAY_WEBHOOK_SECRET", "")
# =========================
# SHOP
# =========================
SHOP_NAME = "HCUONGIOS STORE"
SUPPORT = "@thuynhcuong2510"
CHANNEL = "https://t.me/hcuongiosvip"
MIN_DEPOSIT = 10000
# =========================
# SẢN PHẨM
# =========================
PRODUCTS = {
    "migul_lite": {
        "name": "Migul Lite - VN",
        "price": 100000,
    },
    "migul_pro": {
        "name": "Migul Pro - VN",
        "price": 200000,
    },
    "lienquan": {
        "name": "Liên Quân iOS",
        "price": 150000,
    },
    "pubg": {
        "name": "PUBG Dolphin iOS",
        "price": 180000,
    },
    "global": {
        "name": "Migul Global",
        "price": 250000,
    },
    "flork": {
        "name": "Flork External FF MAX",
        "price": 300000,
    },
    "8ball": {
        "name": "8 Ball Pool iOS",
        "price": 120000,
    }
}
