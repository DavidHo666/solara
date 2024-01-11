import solara
from datetime import datetime

show_message=solara.reactive(False)
@solara.component()
def Page():
    def invalid_t2(date1, date2):
        try:
            date1=datetime.strptime(date1, '%d.%m.%Y')
            date2=datetime.strptime(date2, '%d.%m.%Y')
            return date2 < date1
        except:
            return False

    def invalid_date(date):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            return False
        except:
            return True

    def generate_message(s):
        if s=='one-way flight': return f"You have booked a {s} on {date1.value}"
        else: return f"You have booked a {s} on {date1.value} and {date2.value}"

    style={'color': 'red'}
    with solara.Card():
        c_values=['one-way flight', 'return flight']
        c=solara.use_reactive('one-way flight')
        t2_disable=(c.value=='one-way flight')
        solara.Select(label='combobox', value=c, values=c_values)
        date1=solara.use_reactive('27.03.2014')
        solara.InputText(label='T1',value=date1, error=invalid_date(date1.value))
        date2=solara.use_reactive('27.03.2014')

        solara.InputText(label='T2', value=date2, disabled=t2_disable, error=invalid_date(date2.value))
        b_disable_t2 = invalid_t2(date1.value, date2.value)
        b_disable_ill_dates=invalid_date(date1.value) or invalid_date(date2.value)

        solara.Button(label='Book', disabled=any([b_disable_t2, b_disable_ill_dates]), on_click=lambda :show_message.set(True))
        if show_message.value:
            solara.Markdown(generate_message(c.value))
