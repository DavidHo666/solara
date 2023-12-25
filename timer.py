import asyncio
import solara

@solara.component
def Page():
    elapsed_time, set_elapsed_time = solara.use_state(0.0)
    duration, set_duration = solara.use_state(60.0)

    async def timer_tick():
        nonlocal elapsed_time
        while elapsed_time < duration:
            await asyncio.sleep(1)
            set_elapsed_time(elapsed_time + 1)
            # elapsed_time+=1

    # Start the timer task
    timer_task = asyncio.create_task(timer_tick())

    progress_value = (elapsed_time / duration) * 100 if duration > 0 else 0
    with solara.Card():
        solara.ProgressLinear(value=progress_value, style={'color': 'blue', 'background-color': 'white'})
        solara.Markdown(f'{elapsed_time}s')

