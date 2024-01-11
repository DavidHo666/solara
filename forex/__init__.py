import solara
from typing import *
from solara.util import _combine_classes
T = TypeVar("T")

selected=solara.reactive('')

items = [
    "USD", "EUR", "JPY", "GBP", "AUD", "CAD",
    "CHF", "CNY", "SEK", "NZD", "MXN", "SGD",
    "HKD", "NOK", "KRW", "TRY", "INR",
    "BRL", "ZAR", "DKK", "PLN", "TWD", "THB",
    "IDR", "HUF", "CZK", "ILS", "CLP", "PHP",
    "AED", "COP", "SAR", "MYR", "RON", "ARS",
    "BGN", "HRK", "JOD", "KWD", "LKR", "EGP",
    "VND", "PKR", "BDT", "QAR", "XCD", "OMR",
    "NGN", "BHD"
]

@solara.component_vue("myautocomplete.vue")
def MyAutocomplete(label, values, value, on_value, keyword, on_keyword, dense, class_, disabled, style):
    pass

@solara.component()
def AutoComplete(
    label: str,
    items: List[T],
    value: Union[None, T, solara.Reactive[T], solara.Reactive[Optional[T]]] = None,
    on_value: Union[None, Callable[[T], None], Callable[[Optional[T]], None]] = None,
    dense: bool = False,
    disabled: bool = False,
    classes: List[str] = [],
    style: Union[str, Dict[str, str], None] = None,
) :

    reactive_value = solara.use_reactive(value, on_value)  # type: ignore
    del value, on_value
    style_flat = solara.util._flatten_style(style)
    class_ = _combine_classes(classes)
    def search(keyword, size=1000):
        filtered = []
        if not keyword:
            filtered = items[:size] if len(items) >= size else items
        else:
            for i,item in enumerate(items):
                if keyword.lower() in item.lower():
                    filtered.append(item)
                if len(filtered) >= size:
                    break
        return filtered

    keyword = solara.use_reactive('')
    results = solara.use_memo(lambda: search(keyword.value, 50), dependencies=[keyword.value])
    MyAutocomplete(label=label, values=results, value=reactive_value.value, on_value=reactive_value.set, keyword=keyword.value, on_keyword=keyword.set, dense=dense, disabled=disabled, class_=class_, style=style_flat)


def get_current_forex_price(target_currency, base_currency="USD"):
    import yfinance as yf
    forex_pair = f"{target_currency}{base_currency}=X"
    data = yf.download(forex_pair, period="1mo")
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        today_high = data['Close'].max()
        today_low = data['Close'].min()
        try:
            previous_price = data['Close'].iloc[-2]
        except Exception:
            previous_price=current_price
        return {
            "current_price": current_price,
            "today_high": today_high,
            "today_low": today_low,
            "trend": current_price - previous_price
        }
    else:
        return None