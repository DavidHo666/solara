import solara

tc = solara.reactive('')
tf = solara.reactive('')


@solara.component()
def input_temp(input: solara.Reactive, name1: str, target: solara.Reactive, func):
    def convert(s):
        if not s:
            target.set('')
        try:
            new_val = func(s)
            if not target.value or abs(new_val - float(target.value)) > 1e-7:
                target.set(str(new_val))
        except Exception:
            pass


    solara.InputText(label=name1, value=input, on_value=lambda s: convert(s), continuous_update=True)


@solara.component()
def Page():
    with solara.Card():
        with solara.ColumnsResponsive(12, medium=6):
            input_temp(tc, 'Celsius', tf, lambda x: float(x) * 9 / 5 + 32)
            input_temp(tf, 'Fahrenheit', tc,  lambda x: (float(x) - 32) * 5 / 9)
