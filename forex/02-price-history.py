import uuid
import solara
import yfinance as yf
import plotly.express as px
from forex import items, selected, AutoComplete
from typing import *
from solara.util import _combine_classes
T = TypeVar("T")

items= items[1:]

@solara.component
def Page():
    @solara.memoize
    def fetch_forex_history_data(target_currency, base_currency="USD"):
        forex_pair = f"{target_currency}{base_currency}=X"
        historical_data = yf.download(forex_pair, period="1y")
        return historical_data

    AutoComplete(label='Search forex', items=items, value=selected)
    if selected.value:
        result=fetch_forex_history_data.use_thread(selected.value)
        if result.state == solara.ResultState.FINISHED:
            data = result.value
            fig = px.line(data, x=data.index, y='Close', title=f'{selected.value} Currency Price Over the Past Year')
            fig.update_xaxes(title_text='Date')
            fig.update_yaxes(title_text='Close Price (USD)')
            solara.FigurePlotly(fig)
        else:
            solara.Markdown('Loading...')
    else:
        solara.Markdown('Select a currency from the dropdown above')

