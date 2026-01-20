from exchange.book import OrderBook
from exchange.matcher import MatchingEngine
from exchange.models import Order
from exchange.models import Trade
from exchange.id_gen import next_id
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
        "bids": book.get_bids(),
        "asks": book.get_asks()
    })

def add_order():
    engine,book = make_engine()
    order_A = Order(order_id=next_id(),side='BUY',price=100,qty=10,timestamp=int(time.time()))
    
    trade_A = engine.submit_order(order=order_A)
    show_book(book=book,engine=engine)
    
    
def exact_match():
    engine,book = make_engine()
    
    order_A = Order(order_id=next_id(),side='BUY',price=100,qty=10,timestamp=int(time.time()))
    trade_A = engine.submit_order(order_A)
    show_book(book=book,engine=engine)
    
    print('-----------next order------------------')
    time.sleep(2)
    
    order_B = Order(order_id=next_id(),side='SELL',price=100,qty=10,timestamp=int(time.time()))
    trade_B = engine.submit_order(order_B)
    show_book(book=book,engine=engine)
    
def no_cross(): 
    engine,book = make_engine()
    order_A = Order(order_id=next_id(),side='BUY',price=100,qty=10,timestamp=int(time.time()))
    trade_A = engine.submit_order(order_A)
    
    show_book(book=book,engine=engine)
    print('-----------next order------------------')
    time.sleep(2)
    
    order_B = Order(order_id=next_id(),side='BUY',price=100,qty=10,timestamp=int(time.time()))
    trade_B = engine.submit_order(order_B)
    show_book(book=book,engine=engine)
    
def price_priority(): 
    engine,book = make_engine()
    order_A = Order(order_id=next_id(),side='BUY',price=100,qty=10,timestamp=int(time.time()))
    order_B = Order(order_id=next_id(),side='BUY',price=110,qty=10,timestamp=int(time.time()))
    engine.submit_order(order_A)
    engine.submit_order(order_B)
    print('-----------showing book------------------')
    show_book(book=book,engine=engine)

def last_trade_price(): 
    engine, book = make_engine()

    order_A = Order(order_id=next_id(), side="BUY", price=100, qty=10, timestamp=int(time.time()))
    engine.submit_order(order_A)

    print("---- after BUY ----")
    show_book(book, engine)

    order_B = Order(order_id=next_id(), side="SELL", price=100, qty=10, timestamp=int(time.time()))
    engine.submit_order(order_B)

    print("---- after ASK ----")
    show_book(book, engine)
    trade:Trade = engine.last_trade()
    
    return trade.price


price = last_trade_price()
print(price)