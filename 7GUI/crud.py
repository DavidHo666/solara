import solara

@solara.component
def Page():
    t_prefix=solara.use_reactive('')
    t_name=solara.use_reactive('')
    t_surname=solara.use_reactive('')
    # name_values, set_name_values = solara.use_state([])
    name_values = solara.use_reactive([])
    selected_name=solara.use_reactive('')
    def filter_surname_prefix():
        if not t_prefix.value:
            return name_values.value
        else:
            prefix = t_prefix.value.lower()
            return [name for name in name_values.value if name.split(',')[0].lower().startswith(prefix)]
    filtered_name_values = solara.use_memo(
        filter_surname_prefix,
        [t_prefix.value, name_values.value]
    )
    print("name_values: ", name_values)
    print("filtered_name_values: ", filtered_name_values)

    def create_name():
        new_name = t_surname.value + ','+ t_name.value
        name_values.set(name_values.value + [new_name])
        # name_values.value.append(new_name)
        t_name.set('')
        t_surname.set('')

    def update_name():
        idx=name_values.value.index(selected_name.value)
        new_name = t_surname.value + ','+ t_name.value
        name_values.set(name_values.value[:idx] + [new_name] + name_values.value[idx+1:])
        # name_values[idx] = new_name
        t_name.set('')
        t_surname.set('')

    def delete_name():
        idx=name_values.value.index(selected_name.value)
        name_values.set(name_values.value[:idx] + name_values.value[idx+1:])
        selected_name.set('')
        t_name.set('')
        t_surname.set('')

    with solara.Card():
        with solara.Columns([1,1]):
            with solara.Card():
                solara.InputText(label='Filter prefix', value=t_prefix,
                                 continuous_update=True)
                solara.Select(label='List of names', value=selected_name,
                              values=filtered_name_values)
                solara.Button(label='Create', on_click=create_name)
                solara.Button(label='Update', on_click=update_name)
                solara.Button(label='Delete', on_click=delete_name)
            with solara.Card():
                solara.InputText(label='Name', value=t_name)
                solara.InputText(label='Surname', value=t_surname)


