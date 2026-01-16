from dataclasses import dataclass
from typing import Literal

Side = Literal['BUY',"SELL"]

@dataclass
class Order: 
    order_id: int
    side: Side
    price: int
    qty: int
    timestamp: int

@dataclass
class Trade: 
    price: int
    qty: int
    take_order_id: int
    maker_order_id: int
    

