# When the search query is processed we want to convert the entities to their respective ID's
def key_value(val, dictionary):
    key_list = []

    for key, value in dictionary.items():
        # If the input value is contained in one of the names (dictionary value) then the key to the name is saved
        # If the values are converted to lower we add +4 seconds to the search
        if val in value:
            key_list.append(key)

    return key_list
