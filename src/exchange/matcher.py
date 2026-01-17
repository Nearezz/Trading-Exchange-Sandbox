from .models import Order, Trade
from .book import OrderBook
from collections import deque

class MatchingEngine:
    def __init__(self,book:OrderBook):
        self._last_trade : Trade | None = None
        self.book: OrderBook = book
    
    def submit_order(self,order:Order) -> list[Trade]:
        if order.side == "BUY": 
            best_ask = self.book.best_ask()
            if best_ask is None: 
                self.book.add(order)
                return []
            
            best_ask_price = best_ask[0]
            if order.price >= best_ask_price:
                best_ask_level:deque = self.book._asks[best_ask_price]
                best_ask_order:Order = best_ask_level[0]
                
                if order.qty == best_ask_order.qty:    
                    taker_order_id = order.order_id
                    maker_order_id = best_ask_order.order_id
                    trade = Trade(price=best_ask_order.price,qty=order.qty,taker_order_id=taker_order_id,maker_order_id=maker_order_id)
                    self._last_trade = trade
                    best_ask_level.popleft()
                elif order.qty != best_ask_order.qty: 
                    self.book.add(order)
                    return []
                
                if len(best_ask_level) == 0: 
                    del self.book._asks[best_ask_price]
                return [trade]
            
            elif order.price < best_ask_price:
                self.book.add(order)
                return []
            
        elif order.side == "SELL": 
            best_bid = self.book.best_bid()
            if best_bid is None: 
                self.book.add(order)
                return []
            
            best_bid_price = best_bid[0]
            if order.price <= best_bid_price: 
                best_bid_level: deque = self.book._bids[best_bid_price]
                best_bid_order: Order = best_bid_level[0]
            
                if order.qty == best_bid_order.qty: 
                    taker_order_id = order.order_id
                    maker_order_id = best_bid_order.order_id
                    trade = Trade(price=best_bid_price,qty=order.qty,taker_order_id=taker_order_id,maker_order_id=maker_order_id)
                    self._last_trade = trade
                    best_bid_level.popleft()
                elif order.qty != best_bid_order.qty: 
                    self.book.add(order)
                    return []
                
                if len(best_bid_level) == 0: 
                    del self.book._bids[best_bid_price]
                return [trade]
            elif order.price > best_bid_price: 
                self.book.add(order)
                return []
    def top_of_book(self) -> dict:
        return {
            'bid': self.book.best_bid(),
            'ask': self.book.best_ask()
        }
    def last_trade(self):
        return self._last_trade
            
    