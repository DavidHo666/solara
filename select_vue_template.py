import uuid
import solara

@solara.component_vue("myautotemplate.vue")
def MyAutocomplete(label, values):
    pass

@solara.component
def Page():
    N = 1_000_000  # 1 million items
    items = solara.use_reactive([str(uuid.uuid4()) for _ in range(N)])
    # selected_item = solara.use_reactive('')

    with solara.Card():
        MyAutocomplete(label='My autocomplete', values=items.value)

