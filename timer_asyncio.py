import asyncio
import solara
from typing import cast, Union

elapsed_time=solara.reactive(0)
duration=solara.reactive(60)
@solara.component
def timer_component(elapsed_time, duration, duration_change_callback, reset_callback):
    progress_value = (elapsed_time.value / duration.value) * 100 if duration.value > 0 else 0
    with solara.Card():
        solara.ProgressLinear(value=progress_value,
                              style={'color': 'blue', 'background-color': 'white'})
        solara.Markdown(f'{elapsed_time}s')
        solara.SliderInt(label='Duration', value=duration, min=0, max=100,
                         on_value=lambda x: duration_change_callback(x))
        solara.Button(label='Reset', on_click= reset_callback)

@solara.component
def Page() -> None:
    # timer_task=None
    timer_task=solara.use_ref(cast(Union[asyncio.Task, None], None))
    # print("running page", duration.value)
    async def timer_tick():
        while elapsed_time.value < duration.value:
            await asyncio.sleep(1)
            new_val=elapsed_time.value+1
            elapsed_time.set(new_val)

    def start_timer() -> None:
        if timer_task.current:
            timer_task.current.cancel()
        timer_task.current = asyncio.create_task(timer_tick())

    def on_duration_change(new_duration):
        # duration.set(new_duration)
        start_timer()

    def on_reset():
        elapsed_time.set(0)
        start_timer()

    start_timer()
    timer_component(elapsed_time,duration, on_duration_change, on_reset)
