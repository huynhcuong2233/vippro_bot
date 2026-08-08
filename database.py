import sqlite3
from config import DATABASE_NAME


# ==========================
# KẾT NỐI DATABASE
# ==========================

def connect():
    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


# ==========================
# TẠO BẢNG
# ==========================

def setup_database():

    conn = connect()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        fullname TEXT,
        balance INTEGER DEFAULT 0,
        total_deposit INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # DEPOSITS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        content TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ORDERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product TEXT,
        price INTEGER,
        api_key TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # API KEYS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS keys(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key TEXT UNIQUE,
        plan TEXT,
        used INTEGER DEFAULT 0,
        buyer_id INTEGER,
        sold_time TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# ==========================
# USER
# ==========================

def add_user(user_id, username, fullname):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO users(
        user_id,
        username,
        fullname
    )
    VALUES(?,?,?)
    """,
    (
        user_id,
        username,
        fullname
    ))

    conn.commit()
    conn.close()



def get_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cur.fetchone()

    conn.close()

    return user



# ==========================
# SỐ DƯ
# ==========================

def get_balance(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (user_id,)
    )

    row = cur.fetchone()

    conn.close()


    if row:
        return row[0]

    return 0



def add_balance(user_id, amount):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET
        balance = balance + ?,
        total_deposit = total_deposit + ?
    WHERE user_id=?
    """,
    (
        amount,
        amount,
        user_id
    ))

    conn.commit()
    conn.close()



def remove_balance(user_id, amount):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE user_id=?
    """,
    (
        amount,
        user_id
    ))

    conn.commit()
    conn.close()



# ==========================
# ĐƠN HÀNG
# ==========================

def create_order(user_id, product, price, api_key):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO orders(
        user_id,
        product,
        price,
        api_key
    )
    VALUES(?,?,?,?)
    """,
    (
        user_id,
        product,
        price,
        api_key
    ))

    conn.commit()
    conn.close()



def get_orders(user_id):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT product, price, created_at
    FROM orders
    WHERE user_id=?
    ORDER BY id DESC
    """,
    (
        user_id,
    ))


    rows = cur.fetchall()

    conn.close()

    return rows



# ==========================
# NẠP TIỀN MOMO
# ==========================

def create_deposit(user_id, amount, content):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    INSERT INTO deposits(
        user_id,
        amount,
        content,
        status
    )
    VALUES(?,?,?,'pending')
    """,
    (
        user_id,
        amount,
        content
    ))


    conn.commit()
    conn.close()



def deposit_exists(content):

    conn = connect()
    cur = conn.cursor()


    cur.execute(
        """
        SELECT id
        FROM deposits
        WHERE content=?
        """,
        (
            content,
        )
    )


    row = cur.fetchone()

    conn.close()


    return row is not None



def confirm_deposit(content):

    conn = connect()
    cur = conn.cursor()


    cur.execute("""
    SELECT user_id, amount
    FROM deposits
    WHERE content=?
    AND status='pending'
    """,
    (
        content,
    ))


    row = cur.fetchone()


    if not row:

        conn.close()

        return False



    user_id, amount = row


    cur.execute("""
    UPDATE users
    SET
        balance = balance + ?,
        total_deposit = total_deposit + ?
    WHERE user_id=?
    """,
    (
        amount,
        amount,
        user_id
    ))


    cur.execute("""
    UPDATE deposits
    SET status='done'
    WHERE content=?
    """,
    (
        content,
    ))


    conn.commit()
    conn.close()

    return (user_id, amount)

# ==========================
# API KEY
# ==========================

def add_key(plan, api_key):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO keys(
        api_key,
        plan
    )
    VALUES(?,?)
    """, (api_key, plan))

    conn.commit()
    conn.close()


# ==========================
# LẤY KEY CHƯA BÁN
# ==========================

def get_available_key(plan):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, api_key
        FROM keys
        WHERE plan=? AND used=0
        LIMIT 1
        """,
        (plan,)
    )

    row = cur.fetchone()

    conn.close()

    return row



# ==========================
# ĐÁNH DẤU KEY ĐÃ BÁN
# ==========================

def use_key(key_id, buyer_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE keys
        SET used=1,
            buyer_id=?,
            sold_time=datetime('now')
        WHERE id=?
        """,
        (
            buyer_id,
            key_id
        )
    )

    conn.commit()
    conn.close()


def count_stock(plan):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT COUNT(*)
    FROM keys
    WHERE plan=?
    AND used=0
    """, (plan,))

    total = cur.fetchone()[0]

    conn.close()

    return total


def get_my_keys(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT api_key, plan, sold_time
    FROM keys
    WHERE buyer_id=?
    ORDER BY id DESC
    """, (user_id,))

    rows = cur.fetchall()

    conn.close()

    return rows
    
