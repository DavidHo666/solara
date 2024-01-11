import solara
from forex import items, selected, AutoComplete, get_current_forex_price

balance=solara.reactive({x:1000.0 for x in items})

@solara.component
@solara.component()
def AmountInput(label: str, input: solara.Reactive, target: solara.Reactive,
                rate:float, error=False, disabled=False):
    def convert(s):
        if not s:
            target.set('')
        try:
            new_val = float(s)*rate
            if not target.value or abs(new_val - float(target.value)) > 1e-7:
                target.set(str(new_val))
        except Exception:
            pass


    solara.InputText(label=label, value=input, on_value=lambda s: convert(s),
                     continuous_update=True, error=error, disabled=disabled)

@solara.component
def Page():
    def insufficient_funds(currency, amount):
        if not currency or not amount: return False
        return balance.value[currency] < float(amount)
    def exchange(buy_currency, sell_currency, buy_amount, sell_amount):
        if not buy_currency or not sell_currency or not buy_amount or not sell_amount: return
        balance.set({**balance.value, buy_currency: balance.value[buy_currency] + float(buy_amount),
                     sell_currency: balance.value[sell_currency] - float(sell_amount)})

    with solara.Columns([2,1]):
        with solara.Card('Transaction'):
            buy_currency=solara.use_reactive('Transaction:')
            AutoComplete(label='Buy', value=buy_currency, items=items)
            sell_currency=solara.use_reactive('')
            AutoComplete(label='Sell', value=sell_currency, items=items)
            data=None
            if buy_currency.value and sell_currency.value:
                data=get_current_forex_price(buy_currency.value, sell_currency.value)
            rate=data['current_price'] if data else 1
            buy_amount=solara.use_reactive('')
            sell_amount=solara.use_reactive('')
            is_insufficient=insufficient_funds(sell_currency.value, sell_amount.value)
            AmountInput(label='Buy Amount', input=buy_amount, target=sell_amount, rate=rate,
                        disabled=not (buy_currency.value and sell_currency.value))
            AmountInput(label='Sell Amount', input=sell_amount, target=buy_amount, rate=1/rate,
                        error=is_insufficient, disabled=not (buy_currency.value and sell_currency.value))
            solara.Button(label='Exchange', disabled=is_insufficient,
                          on_click= lambda: exchange(buy_currency.value, sell_currency.value, buy_amount.value, sell_amount.value))


        with solara.Card('Balance'):
            for currency in items:
                solara.Markdown(f'{currency}: {balance.value[currency]}')

