import random


def create_deposit_code(user_id):
    code = f"NAP{user_id}{random.randint(100,999)}"
    return code
