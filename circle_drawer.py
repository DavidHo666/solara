import solara
from math import sqrt
import asyncio

circles = solara.reactive([])  # type: ignore
undo_history = solara.reactive([]) # type: ignore
redo_history = solara.reactive([]) # type: ignore
selected_circle = solara.reactive({})  # type: ignore
popup_menu_visible = solara.reactive(False)
adjust_diameter_visible = solara.reactive(False)
canCreateCircle = solara.reactive(True)

@solara.component
def Page():
    FIXED_DIAMETER = 50
    def handle_click(*args):
        if canCreateCircle.value:
            event = args[2]
            x, y = event['x'], event['y']
            # print('x:', x, 'y:', y)
            new_circle = {
                "x": x,
                "y": y,
                "diameter": FIXED_DIAMETER,
                "selected": False
            }
            new_state = circles.value + [new_circle]
            undo_history.value.append(new_state) # dangerous
            print('undo_history: ', undo_history.value)
            circles.set(new_state)
            redo_history.value.clear()
        else:
            if popup_menu_visible.value:
                popup_menu_visible.set(False)
                selected_circle.set({})
                canCreateCircle.set(True)
            elif adjust_diameter_visible.value:
                pass

    def handle_mouse_move(*args):
        event = args[2]
        mouseX, mouseY = event['x'], event['y']
        updated_circles = []

        for circle in circles.value:
            distance = sqrt((circle['x'] - mouseX) ** 2 + (circle['y'] - mouseY) ** 2)
            is_selected = distance < circle['diameter'] / 2
            updated_circle = {**circle,
                              "selected": is_selected}
            updated_circles.append(updated_circle)

        circles.set(updated_circles)

    def handle_right_click(*args):
        event = args[2]
        selected = [c for c in circles.value if c["selected"]]
        if selected:
            selected_circle.set(selected[0])
            popup_menu_visible.set(True)
            canCreateCircle.set(False)


    def open_adjust_diameter_frame():
        adjust_diameter_visible.set(True)
        popup_menu_visible.set(False)
        canCreateCircle.set(False)

    def adjust_diameter(new_diameter):
        if selected_circle.value:
            updated_circles = []
            for circle in circles.value:
                if circle['x'] == selected_circle.value['x'] and circle['y'] == selected_circle.value['y']:
                    # print('updating diameter')
                    updated_circle = {**circle,
                                      "diameter": new_diameter}
                else:
                    updated_circle = circle
                updated_circles.append(updated_circle)


            circles.set(updated_circles)


    def close_adjust_diameter_frame():
        undo_history.value.append(circles.value)
        print('undo_history: ', undo_history.value)
        redo_history.value.clear()
        adjust_diameter_visible.set(False)
        async def enable_circle_creation():
            await asyncio.sleep(0.1)
            canCreateCircle.set(True)

        asyncio.create_task(enable_circle_creation())

    def undo():
        print('undoing')
        if undo_history.value:
            last_state = undo_history.value.pop()
            print('last_state: ',last_state)
            redo_history.value.append(circles.value)
            print('redo_history: ',redo_history.value)
        circles.set(undo_history.value[-1] if undo_history else [])

    def redo():
        if redo_history.value:
            last_redo_state = redo_history.value.pop()
            undo_history.value.append(circles.value)
            circles.set(last_redo_state)

    with solara.VBox() as main:
        with solara.Columns([1,1]):
            with solara.Card():
                solara.Button("Undo", on_click=undo)
                solara.Button("Redo", on_click=redo)

        with solara.Div(style={'background-color': 'lightgray',
                               'width': '400px', 'height': '400px'}) as canvas:
            for circle in circles.value:
                css = {
                    "border": "solid red 2px",
                    "height": str(circle["diameter"]) + "px",
                    "width": str(circle["diameter"]) + "px",
                    "border-radius": "50%",
                    "left": str(circle["x"] - circle["diameter"] / 2) + "px",
                    "top": str(circle["y"] - circle["diameter"] / 2) + "px",
                    "position": "absolute",
                    "background-color": "blue" if circle["selected"] else "transparent",
                }
                solara.Div(style=css)
                if popup_menu_visible.value:
                    with solara.Div(style={
                        "position": "absolute",
                        "left": str(selected_circle.value["x"]) + "px",
                        "top": str(selected_circle.value["y"]) + "px"}) as popup_menu:
                        solara.Button("Adjust diameter..",
                                      on_click=open_adjust_diameter_frame)

                if adjust_diameter_visible.value:
                    with solara.Div(style={
                        "background-color": "white",
                        "position": "absolute",
                        "left": str(selected_circle.value["x"]) + "px",
                        "top": str(selected_circle.value["y"]) + "px",
                        'width': '400px', 'height': '80px'}) as diameter_adjust_frame:
                        solara.SliderInt(label='Diameter',
                                         value=selected_circle.value["diameter"],
                                         min=10, max=100,
                                         on_value=adjust_diameter)
                        solara.Button("Close",
                                      on_click=close_adjust_diameter_frame)

        solara.v.use_event(canvas, 'click', handle_click)
        solara.v.use_event(canvas, 'mousemove', handle_mouse_move)
        solara.v.use_event(canvas, 'contextmenu', handle_right_click)

    return main

