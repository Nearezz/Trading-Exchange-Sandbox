from random import randint
from datetime import datetime

def create_id() -> int: 
    return randint(1,10**9)

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
