import uuid
import solara
from typing import *
from solara.util import _combine_classes
T = TypeVar("T")


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
    """Select a single value from a list of values.

    ### Basic example:

    ```solara
    import solara

    foods = ["Kiwi", "Banana", "Apple"]
    food = solara.reactive("Banana")


    @solara.component
    def Page():
        solara.AutoComplete(label="Food", value=food, values=foods)
        solara.Markdown(f"**Selected**: {food.value}")
    ```

    ## Arguments

     * `label`: Label to display next to the select.
     * `value`: The currently selected value.
     * `values`: List of values to select from.
     * `on_value`: Callback to call when the value changes.
     * `dense`: Whether to use a denser style.
     * `disabled`: Whether the select widget allow user interaction
     * `classes`: List of CSS classes to apply to the select.
     * `style`: CSS style to apply to the select.

    """
    # next line is very hard to get right with typing
    # might need an overload on use_reactive, when value is None
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
    results = solara.use_memo(lambda: search(keyword.value, 10), dependencies=[keyword.value])
    MyAutocomplete(label=label, values=results, value=reactive_value.value, on_value=reactive_value.set, keyword=keyword.value, on_keyword=keyword.set, dense=dense, disabled=disabled, class_=class_, style=style_flat)



@solara.component
def Page():
    N = 1_000_000
    items = solara.use_memo(lambda :[str(i) for i in range(N)], dependencies=[])
    selected = solara.use_reactive('')
    AutoComplete(label='My autocomplete', items=items, value=selected)

    # def search(keyword, size=1000):
    #     filtered = []
    #     if not keyword:
    #         filtered = items[:size] if len(items) >= size else items
    #     else:
    #         for i,item in enumerate(items):
    #             if keyword.lower() in item.lower():
    #                 filtered.append(item)
    #             if len(filtered) >= size:
    #                 break
    #     return filtered
    #
    #
    # keyword = solara.use_reactive('')
    # results = solara.use_memo(lambda: search(keyword.value,10), dependencies=[keyword.value])
    # selected=solara.use_reactive('')
    # print('selected:', selected.value)
    # print('results:', results)
    # print('keyword:', keyword.value)
    # def debug(value):
    #     print('keyword_debug1:', value)
    #     keyword.value=value
    #     print('keyword_debug2:', value)
    # with solara.Card():
    #     MyAutocomplete(label='My autocomplete', values=results, value=selected.value, on_value=selected.set, keyword=keyword.value, on_keyword=debug)
