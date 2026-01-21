from .models import Order
from collections import deque

class OrderBook:
    """
    OrderBook stores limit orders grouped by price level.

    Data structure
    -------------
    - _bids: dict[price -> deque[Order]]
        BUY orders keyed by price. Each price level is FIFO (deque).
    - _asks: dict[price -> deque[Order]]
        SELL orders keyed by price. Each price level is FIFO (deque).

    Notes
    -----
    - This OrderBook does NOT do matching. It only stores orders and provides views.
    - FIFO within a price level is preserved by using deque.

    Public API
    ----------
    add_order(order):
        Add a new Order into the correct side (bids or asks) at its price level.

    get_bids() / get_asks():
        Return aggregated levels:
            { price: total_quantity_at_that_price }

    get_raw_bids() / get_raw_asks():
        Return raw orders grouped by price level (debug / inspection view):
            { price: [ {order fields...}, ... ] }

    best_bid() / best_ask():
        Return the best price level as:
            (best_price, total_quantity_at_that_price)
        - best bid = highest bid price
        - best ask = lowest ask price
        Returns None if that side is empty.
    """

    def __init__(self):
        """Initialize an empty order book with no bids and no asks."""
        self._bids = {}
        self._asks = {}

    def add_order(self, order: Order) -> None:
        """
        Add a new order to the order book.

        - BUY orders go into _bids at their price level.
        - SELL orders go into _asks at their price level.
        - Orders at the same price are stored FIFO using a deque.
        """
        if order.side == "BUY":
            try:
                self._bids[order.price].append(order)
            except KeyError:
                self._bids[order.price] = deque([order])
        elif order.side == "SELL":
            try:
                self._asks[order.price].append(order)
            except KeyError:
                self._asks[order.price] = deque([order])  # price -> deque of orders

    def get_raw_bids(self):
        """
        Return a raw, detailed snapshot of all bid orders grouped by price.

        Output format:
            { price: [ {order_id, side, price, qty, timestamp}, ... ], ... }

        This is mainly useful for debugging/inspection.
        """
        return {
            price: [
                {
                    'order_id': o.order_id,
                    'side': o.side,
                    'price': o.price,
                    'qty': o.qty,
                    'timestamp': o.timestamp
                }
                for o in level
            ]
            for price, level in self._bids.items()
        }

    def get_raw_asks(self):
        """
        Return a raw, detailed snapshot of all ask orders grouped by price.

        Output format:
            { price: [ {order_id, side, price, qty, timestamp}, ... ], ... }

        This is mainly useful for debugging/inspection.
        """
        return {
            price: [
                {
                    'order_id': o.order_id,
                    'side': o.side,
                    'price': o.price,
                    'qty': o.qty,
                    'timestamp': o.timestamp
                }
                for o in level
            ]
            for price, level in self._asks.items()
        }

    def get_bids(self):
        """
        Return aggregated bid levels (Level 2 view), sorted high -> low.

        Output format:
            { price: total_quantity_at_price, ... }
        """
        d = {
            price: sum(order.qty for order in level)
            for price, level in self._bids.items()
        }
        return dict(sorted(d.items(), reverse=True))


    def get_asks(self):
        """
        Return aggregated ask levels (Level 2 view), sorted low -> high.

        Output format:
            { price: total_quantity_at_price, ... }
        """
        d = {
            price: sum(order.qty for order in level)
            for price, level in self._asks.items()
        }
        return dict(sorted(d.items()))
    def get_best_bid(self) -> tuple[int, int] | None:
        """
        Return the best bid level (highest bid price).

        Returns:
            (best_bid_price, total_quantity_at_that_price)
        or:
            None if there are no bids.
        """
        prices = self._bids.keys()
        if len(prices) == 0:
            return None

        highest_price = max(prices)
        highest_price_level = self._bids[highest_price]  # deque of orders

        best_bid_quantity = 0
        for order in highest_price_level:
            best_bid_quantity += order.qty

        return (highest_price, best_bid_quantity)

    def get_best_ask(self) -> tuple[int, int] | None:
        """
        Return the best ask level (lowest ask price).

        Returns:
            (best_ask_price, total_quantity_at_that_price)
        or:
            None if there are no asks.
        """
        prices = self._asks.keys()
        if len(prices) == 0:
            return None

        lowest_price = min(prices)
        lowest_price_level = self._asks[lowest_price]  # deque of orders

        best_ask_quantity = 0
        for order in lowest_price_level:
            best_ask_quantity += order.qty

        return (lowest_price, best_ask_quantity)
