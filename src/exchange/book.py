from .models import Order

from collections import deque

class OrderBook: 
    def __init__(self):
        self._bids = {}
        self._asks = {}
    
    def add(self,order:Order) -> None: 
        if order.side == "BUY": 
            try: 
                self._bids[order.price].append(order)
            except KeyError: 
                self._bids[order.price] = deque([order])
        elif order.side == "SELL": 
            try: 
                self._asks[order.price].append(order)
            except KeyError: 
                self._asks[order.price] = deque([order]) # price -> dequeue of orders
                
    def best_bid(self) -> tuple[int,int] | None: 
        prices = self._bids.keys()
        if len(prices) == 0: 
            return None
        
        highest_price = max(prices)
        
        highest_price_level = self._bids[highest_price] #deque of orders
        best_bid_quantity = 0 
        
        for order in highest_price_level: 
            best_bid_quantity += order.qty
        
        return (highest_price,best_bid_quantity)
    
    def best_ask(self) -> tuple[int,int] | None: 
        prices = self._asks.keys()
        if len(prices) == 0: 
            return None
        lowest_price = min(prices)
        
        lowest_price_level = self._asks[lowest_price] 
        best_ask_quantity = 0 
        
        for order in lowest_price_level: 
            best_ask_quantity+= order.qty
        
        return (lowest_price,best_ask_quantity)

    

        