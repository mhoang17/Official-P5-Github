# When the search query is processed we want to convert the entities to their respective ID's
def key_value(val, dictionary):
    key_list = []

    for key, value in dictionary.items():
        # If the input value is contained in one of the names (dictionary value) then the key to the name is saved
        if val.lower() in value.lower():
            key_list.append(key)

    return key_list
