# products.py

PRODUCTS = {
    "migul_lite": {
        "name": "Migul Lite - VN",
        "price": 100000,
        "description": "Phiên bản Lite."
    },
    "migul_pro": {
        "name": "Migul Pro - VN",
        "price": 200000,
        "description": "Phiên bản Pro."
    },
    "lienquan": {
        "name": "Liên Quân iOS",
        "price": 150000,
        "description": "Hỗ trợ Liên Quân."
    },
    "pubg": {
        "name": "PUBG Dolphin iOS",
        "price": 180000,
        "description": "PUBG Dolphin."
    },
    "global": {
        "name": "Migul Global",
        "price": 250000,
        "description": "Bản Global."
    },
    "flork": {
        "name": "Flork External FF MAX",
        "price": 300000,
        "description": "Flork FF MAX."
    },
    "8ball": {
        "name": "8 Ball Pool iOS",
        "price": 120000,
        "description": "8 Ball Pool."
    }
}

def get_product(key):
    return PRODUCTS.get(key)

def all_products():
    return PRODUCTS
