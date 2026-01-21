import streamlit as st
import pandas as pd

from exchange.book import OrderBook
from exchange.matcher import MatchingEngine
from exchange.models import Order
from exchange.utility import create_id, now_str

# -----------------------------
# State
# -----------------------------
def init_engine_state():
    if "engine" not in st.session_state:
        book = OrderBook()
        engine = MatchingEngine(book)
        st.session_state.book = book
        st.session_state.engine = engine

    if "order_log" not in st.session_state:
        st.session_state.order_log = []

    # UI-only
    if "ticker" not in st.session_state:
        st.session_state.ticker = "BTC-USD"

    return st.session_state.book, st.session_state.engine


def reset_engine_state():
    book = OrderBook()
    engine = MatchingEngine(book)
    st.session_state.book = book
    st.session_state.engine = engine
    st.session_state.order_log = []


# -----------------------------
# UI Components
# -----------------------------
def order_form():
    with st.form("order_form"):
        st.subheader("Order Ticket")

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            side = st.selectbox("Side", ["BUY", "SELL"])
        with c2:
            price = st.number_input("Price", min_value=1, step=1)
        with c3:
            qty = st.number_input("Quantity", min_value=1, step=1)

        submitted = st.form_submit_button("Submit Limit Order")

    return side, int(price), int(qty), submitted


def handle_submit(side, price, qty, submitted, engine: MatchingEngine):
    if not submitted:
        return

    order = Order(
        order_id=create_id(),
        side=side,
        price=price,
        qty=qty,
        timestamp=now_str()
    )

    trades = engine.submit_order(order)

    # log it
    st.session_state.order_log.append({
        "timestamp": order.timestamp,
        "order_id": order.order_id,
        "side": order.side,
        "price": order.price,
        "qty": order.qty,
        "traded": len(trades) > 0
    })

    if trades:
        st.success(f"Trade executed: price={trades[0].price}, qty={trades[0].qty}")
    else:
        st.info("📌 Order added to book (no match).")


def render_top_of_book(engine: MatchingEngine):
    top = engine.top_of_book()
    bid = top.get("bid")
    ask = top.get("ask")

    st.subheader("Top of Book")

    c1, c2 = st.columns(2)

    if bid is None:
        c1.metric("Best Bid", "—")
        c1.metric("Bid Size", "—")
    else:
        c1.metric("Best Bid", bid[0])
        c1.metric("Bid Size", bid[1])

    if ask is None:
        c2.metric("Best Ask", "—")
        c2.metric("Ask Size", "—")
    else:
        c2.metric("Best Ask", ask[0])
        c2.metric("Ask Size", ask[1])


def _levels_to_df(levels: dict) -> pd.DataFrame:
    if not levels:
        return pd.DataFrame(columns=["price", "qty"])
    rows = [{"price": p, "qty": q} for p, q in levels.items()]
    return pd.DataFrame(rows)


def render_order_book_ladder(book: OrderBook):
    st.subheader("Order Book")

    bids = book.get_bids()
    asks = book.get_asks()

    bids_df = _levels_to_df(bids).sort_values("price", ascending=False).reset_index(drop=True)
    asks_df = _levels_to_df(asks).sort_values("price", ascending=True).reset_index(drop=True)

    n = max(len(bids_df), len(asks_df))
    bids_df = bids_df.reindex(range(n))
    asks_df = asks_df.reindex(range(n))

    ladder = pd.DataFrame({
        "Bid Qty": bids_df["qty"],
        "Bid Px": bids_df["price"],
        "Ask Px": asks_df["price"],
        "Ask Qty": asks_df["qty"],
    })

    st.dataframe(
        ladder,
        use_container_width=True,
        hide_index=True,
        height=420
    )

    c1, c2 = st.columns(2)
    with c1:
        st.caption("Bids (high → low)")
    with c2:
        st.caption("Asks (low → high)")


def render_last_trade(engine: MatchingEngine):
    st.subheader("Last Trade")
    trade = engine.last_trade()

    if trade is None:
        st.write("No trades yet.")
        return

    # Exchange-style summary row
    c1, c2, c3 = st.columns(3)
    c1.metric("Price", trade.price)
    c2.metric("Qty", trade.qty)
    c3.metric("Value", trade.price * trade.qty)

    # compact “tape” details (no object dump)
    st.caption("Trade Details")
    st.dataframe(
        pd.DataFrame([{
            "price": trade.price,
            "qty": trade.qty,
            "taker_order_id": trade.taker_order_id,
            "maker_order_id": trade.maker_order_id,
        }]),
        use_container_width=True,
        hide_index=True
    )



def render_order_log():
    st.subheader("Order Log")

    if not st.session_state.order_log:
        st.write("No orders submitted yet.")
        return

    df = pd.DataFrame(st.session_state.order_log)
    st.dataframe(df, use_container_width=True, hide_index=True, height=420)


def quick_actions(engine: MatchingEngine):
    st.subheader("Quick Actions")

    c1, c2, c3 = st.columns(3)

    if c1.button("BUY 100 x10", use_container_width=True):
        handle_submit("BUY", 100, 10, True, engine)
        st.rerun()

    if c2.button("SELL 100 x10", use_container_width=True):
        handle_submit("SELL", 100, 10, True, engine)
        st.rerun()

    if c3.button("BUY 110 x10", use_container_width=True):
        handle_submit("BUY", 110, 10, True, engine)
        st.rerun()


# -----------------------------
# App
# -----------------------------
def main():
    st.set_page_config(page_title="Toy Exchange", layout="wide")

    # tighter spacing + more “terminal” feel
    st.markdown(
        """
        <style>
          .block-container {
            padding-top: 1.1rem;
            padding-left: 2rem;
            padding-right: 2rem;
          }
          h1, h2, h3 {
            margin-bottom: 0.4rem;
          }
          [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px;
          }
        </style>
        """,
        unsafe_allow_html=True
    )

    book, engine = init_engine_state()

    # ---------- Header Bar ----------
    header = st.columns([1.3, 1.2, 0.7])
    with header[0]:
        st.title("Toy Exchange")
        st.caption("Limit-order toy exchange with top-of-book matching.")

    with header[1]:
        st.markdown("**Ticker**")
        tickers = ["BTC-USD", "ETH-USD", "SPY", "AAPL", "TSLA"]
        st.session_state.ticker = st.selectbox(
            label="Ticker",
            options=tickers,
            index=tickers.index(st.session_state.ticker),
            label_visibility="collapsed",
        )

    with header[2]:
        st.markdown("**Actions**")
        if st.button("Reset Book", use_container_width=True):
            reset_engine_state()
            st.toast("Reset complete ✅")
            st.rerun()

    st.divider()

    # ---------- Main Grid ----------
    left, middle, right = st.columns([1.05, 1.35, 1.1], gap="large")

    with left:
        with st.container(border=True):
            st.markdown("### Order Entry")
            side, price, qty, submitted = order_form()
            handle_submit(side, price, qty, submitted, engine)

        st.write("")

        with st.container(border=True):
            quick_actions(engine)

    with middle:
        with st.container(border=True):
            st.markdown("### Market Depth")
            render_top_of_book(engine)
            render_order_book_ladder(book)

    with right:
        with st.container(border=True):
            st.markdown("### Tape")
            render_last_trade(engine)

        st.write("")

        with st.container(border=True):
            render_order_log()


if __name__ == "__main__":
    main()
