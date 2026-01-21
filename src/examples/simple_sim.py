from exchange.book import OrderBook
from exchange.matcher import MatchingEngine
from exchange.models import Order, Trade
from exchange.utility import create_id,now_str
import time

# ---------- Helpers ----------

def make_engine():
    book = OrderBook()
    engine = MatchingEngine(book)
    return engine, book


def show_book(book: OrderBook, engine: MatchingEngine):
    print("Top of book:", engine.top_of_book())
    print("Last trade:", engine.last_trade())
    print("Levels:", {"bids": book.get_bids(), "asks": book.get_asks()})
    print()


# ---------- Test cases ----------

def test_add_one_order():
    engine, book = make_engine()

    order = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )

    engine.submit_order(order)
    show_book(book, engine)


def test_exact_match():
    engine, book = make_engine()

    order_a = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_a)
    show_book(book, engine)

    print("----------- next order -----------\n")
    time.sleep(1)

    order_b = Order(
        order_id=create_id(),
        side="SELL",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_b)
    show_book(book, engine)


def test_no_cross_two_buys():
    engine, book = make_engine()

    order_a = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_a)
    show_book(book, engine)

    print("----------- next order -----------\n")
    time.sleep(1)

    order_b = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_b)
    show_book(book, engine)


def test_price_priority():
    engine, book = make_engine()

    order_a = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    order_b = Order(
        order_id=create_id(),
        side="BUY",
        price=110,
        qty=10,
        timestamp=now_str()
    )

    engine.submit_order(order_a)
    engine.submit_order(order_b)

    print("----------- showing book -----------\n")
    show_book(book, engine)


def test_last_trade_price() -> int:
    engine, book = make_engine()

    order_a = Order(
        order_id=create_id(),
        side="BUY",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_a)

    print("---- after BUY ----\n")
    show_book(book, engine)

    order_b = Order(
        order_id=create_id(),
        side="SELL",
        price=100,
        qty=10,
        timestamp=now_str()
    )
    engine.submit_order(order_b)

    print("---- after SELL ----\n")
    show_book(book, engine)

    trade: Trade = engine.last_trade()
    return trade.price


# ---------- Run all ----------

if __name__ == "__main__":
    print("\n===== TEST 1: Add single order =====\n")
    test_add_one_order()

    print("\n===== TEST 2: Exact match =====\n")
    test_exact_match()

    print("\n===== TEST 3: No cross (2 buys) =====\n")
    test_no_cross_two_buys()

    print("\n===== TEST 4: Price priority =====\n")
    test_price_priority()

    print("\n===== TEST 5: Last trade price =====\n")
    price = test_last_trade_price()
    print("Returned last trade price:", price)
