from exchange.book import OrderBook
from exchange.matcher import MatchingEngine
from exchange.models import Order
from exchange.models import Trade
import time


#helper methods
def make_engine():
    book = OrderBook()
    return MatchingEngine(book), book


def show_book(book: OrderBook, engine: MatchingEngine):
    print("Top of the book:", {
        "bid": book.best_bid(),
        "ask": book.best_ask()
    })

    print("Last Trade:", engine.last_trade())

    print("Remaining levels:", {
        "bids": book._bids,
        "asks": book._asks
    })


def exact_match():
    engine,book = make_engine()
    
    order_A = Order(order_id=1,side='BUY',price=100,qty=10,timestamp=int(time.time()))
    trade_A = engine.submit_order(order_A)
    show_book(book=book,engine=engine)
    
    print("Waiting for order to get filled....")
    time.sleep(2)
    
    order_B = Order(order_id=2,side='SELL',price=100,qty=10,timestamp=int(time.time()))
    trade_B = engine.submit_order(order_B)
    show_book(book=book,engine=engine)
    
exact_match()
    
    