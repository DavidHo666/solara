import asyncio
import solara
import time

elapsed_time=solara.reactive(0)
duration=solara.reactive(60)
@solara.component
def TimerComponent(elapsed_time, duration):
    progress_value = (elapsed_time.value / duration.value) * 100 if duration.value > 0 else 0
    with solara.Card():
        solara.ProgressLinear(value=progress_value,
                              style={'color': 'blue', 'background-color': 'white'})
        solara.Markdown(f'{elapsed_time}s')
        solara.SliderInt(label='Duration', value=duration, min=0, max=100)
        solara.Button(label='Reset', on_click= lambda : elapsed_time.set(0))

@solara.component
def Page():
    def timer_work():
        while elapsed_time.value<duration.value:
            time.sleep(1)
            elapsed_time.value=elapsed_time.value+1
            # elapsed_time.set(new_time)

    result: solara.Result[bool]=solara.use_thread(timer_work, dependencies=[duration.value])


    TimerComponent(elapsed_time,duration)
