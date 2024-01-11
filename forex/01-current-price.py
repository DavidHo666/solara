import solara
from collections import defaultdict
from forex import items, selected
from typing import Union
import yfinance as yf
import time



tick= solara.reactive(0)
items = items[1:]


@solara.component()
def Page():
    def ticking():
        while True:
            time.sleep(60)
            tick.set(int(not tick.value))

    tick_result = solara.use_thread(ticking, dependencies=[])

    watching= solara.use_reactive([])
    print('watching.value', watching.value)
    unwatching= solara.use_reactive(items[:])
    def add_watch(ticker_symbol):
        # print('add_watch', ticker_symbol)
        if ticker_symbol and ticker_symbol not in watching.value:
            watching.set(watching.value + [ticker_symbol])
            unwatching.set([item for item in unwatching.value if item != ticker_symbol])

    def get_current_forex_price(target_currency, base_currency="USD"):
        forex_pair = f"{target_currency}{base_currency}=X"
        data = yf.download(forex_pair, period="1mo")
        if not data.empty:
            current_price = data['Close'].iloc[-1]
            today_high = data['Close'].max()
            today_low = data['Close'].min()
            previous_price = data['Close'].iloc[-2]
            return {
                "current_price": current_price,
                "today_high": today_high,
                "today_low": today_low,
                "trend": current_price - previous_price
            }
        else:
            return None

    results = {}
    with solara.Card('Watchlist'):
        with solara.ColumnsResponsive(6, large=4):
            for currency in watching.value:
                if not currency: continue
                results[currency]=solara.use_thread(
                    lambda cancel_event, symbol=currency: get_current_forex_price(symbol),
                    dependencies=[tick.value])
                if results[currency].state == solara.ResultState.FINISHED:
                    current_price = results[currency].value['current_price']
                    today_high = results[currency].value['today_high']
                    today_low = results[currency].value['today_low']
                    trend = results[currency].value['trend']
                    tab= '        '
                    content=f"{currency}: {current_price:.4f}, High: {today_high:.4f}, Low: {today_low:.4f}"
                    if trend>=0:
                        solara.Success(content)

                    else:
                        solara.Error(content)
                else:
                    solara.Info(f"{currency}: loading...")

    solara.Markdown("## All Currencies:")
    with solara.Column(style={
        "max-width": "300px"}):
        for ticker_symbol in unwatching.value:
            with solara.Row(style={"align-items": "center"}):
                solara.Text(ticker_symbol)
                solara.v.Spacer()
                solara.Button(icon_name="mdi-note-plus-outline",
                              on_click=lambda current_symbol=ticker_symbol: add_watch(current_symbol),
                              icon=True)