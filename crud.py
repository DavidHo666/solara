import solara

@solara.component
def Page():
    # t_prefix, set_t_prefix = solara.use_state('')
    t_prefix=solara.use_reactive('')
    print('t_prefix',t_prefix)
    # t_name, set_t_name = solara.use_state('')
    t_name=solara.use_reactive('')
    # t_surname, set_t_surname = solara.use_state('')
    t_surname=solara.use_reactive('')
    name_values, set_name_values = solara.use_state([])
    # name_values=solara.use_reactive([])
    print('name_values2:',name_values)
    # selected_name, set_selected_name = solara.use_state('')
    selected_name=solara.use_reactive('')
    def filter_surname_prefix():
        print('t_prefix: ', t_prefix.value)
        if not t_prefix.value:
            print('not filtering')
            return name_values
        else:
            print(f'filtering: {t_prefix}')
            prefix = t_prefix.value.lower()
            return [name for name in name_values if name.split(',')[0].lower().startswith(prefix)]
    filtered_name_values = solara.use_memo(
        filter_surname_prefix,
        [t_prefix.value, name_values]
    )


    print("name_values: ", name_values)
    print("filtered_name_values: ", filtered_name_values)

    # def filter_surname_prefix(prefix):
    #     if not prefix:
    #         set_filtered_name_values(name_values)
    #     else:
    #         prefix = prefix.lower()
    #         set_filtered_name_values([name for name in name_values if name.split(',')[0].lower().startswith(prefix)])
    #         set_t_prefix(prefix)

    def create_name():
        new_name = t_surname.value + ','+ t_name.value
        print("calling set_name_values")
        # name_values.append(new_name)
        # set_name_values(name_values+[new_name])
        name_values.append(new_name)
        print("name_values1: ", name_values)
        print('filtered_name_values1', filtered_name_values)

        # set_t_name('')
        t_name.value=''
        t_surname.value=''


    def update_name():
        idx=name_values.index(selected_name.value)
        new_name = t_surname.value + ','+ t_name.value
        name_values[idx] = new_name
        # set_t_name('')
        t_name.value = ''
        t_surname.value=''

    def delete_name():
        name_values.remove(selected_name.value)
        # set_selected_name('')
        selected_name.value=''
        # set_t_name('')
        t_name.value = ''
        t_surname.value=''




    with solara.Card():
        with solara.Columns([1,1]):
            with solara.Card():
                solara.InputText(label='Filter prefix', value=t_prefix,
                                 continuous_update=True)
                solara.Select(label='List of names', value=selected_name, values=filtered_name_values)
                solara.Button(label='Create', on_click=create_name)
                solara.Button(label='Update', on_click=update_name)
                solara.Button(label='Delete', on_click=delete_name)
            with solara.Card():
                solara.InputText(label='Name', value=t_name)
                solara.InputText(label='Surname', value=t_surname)


