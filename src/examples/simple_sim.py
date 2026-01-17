# examples/simple_sim.py

from exchange.models import Order
from exchange.book import OrderBook
from exchange.matcher import MatchingEngine
import time

def print_state(label: str, engine: MatchingEngine, trades):
    print(f"\n--- {label} ---")
    print("trades:", trades)
    print("top_of_book:", engine.top_of_book())
    print("last_trade:", engine.last_trade())

def main():
    book = OrderBook()
    engine = MatchingEngine(book)

    o1 = Order(order_id=1, side="BUY",  price=100, qty=10, timestamp=1)
    t1 = engine.submit_order(o1)
    print_state("BUY 10 @ 100", engine, t1)
    
    time.sleep(1)

    o2 = Order(order_id=2, side="SELL", price=105, qty=10, timestamp=2)
    t2 = engine.submit_order(o2)
    print_state("SELL 10 @ 105", engine, t2)
    
    time.sleep(1)


    o3 = Order(order_id=3, side="BUY",  price=105, qty=10, timestamp=3)
    t3 = engine.submit_order(o3)
    print_state("BUY 10 @ 105 (crosses)", engine, t3)
    
    time.sleep(1)
    
    o4 = Order(order_id=3, side="SELL",  price=100, qty=10, timestamp=3)
    t4 = engine.submit_order(o4)
    print_state("SELL 10 @ 100 (crosses)", engine, t4)


if __name__ == "__main__":
    main()
