def seperate_all_paths(predicates, sec_all_paths, names):
    paths_list = []
    predicate = predicates[0]
    idx = 1

    # TODO: make it so that it will only do this if the entry is like mentioned before
    for elements in sec_all_paths:
        # We reverse the list because it is easier to go backwards, because the end node will only occur once.
        elements.reverse()

        # Here we store the path
        path = []

        # This will be important if we have found a part of the part and need the next predicate to know which
        # path we now need to take
        k = len(predicate) - 1

        # This is only important if there are more entities and we therefore need to switch between predicate lists
        if len(predicates) > 1:
            # This is a fail safe measure so we don't get a out of bounds exception
            if idx < len(predicates) and idx < len(names):
                # If the next element is the name of the next entity, we need to switch to the predicate list
                # that belongs to that specific entity
                if names[idx] in elements[len(elements) - 1]:
                    predicate = predicates[idx]
                    idx += 1

        # We have two for loops that kinda goes through the same. The outer goes through the whole list
        # While the other loop only loops from where the outer loop has reached to the end.
        # This is to find the remaining path which will always lie from l to len(elements)
        for l in range(len(elements)):
            # If we have found the correct predicate, then we know we have found the end of a path.
            if elements[l] == predicate[k]:
                for j in range(l, len(elements)):
                    if elements[j] == predicate[k]:
                        # The entity which the edge goes into will always lie in the index before the index
                        # where the predicate lies
                        path.append(elements[j - 1])
                        path.append(elements[j])

                        # We will now move on to the next predicate
                        k -= 1

                    # If we have reached the end, then we know the path is done
                    elif j == len(elements) - 1:
                        path.append(elements[j])

                        # Reset k to the length of the current predicate list
                        k = len(predicate) - 1

            # If we found a path then we will add it
            if path:
                # Reverse it so it will be in the correct order
                path.reverse()
                paths_list.append(path)

                # Reset path
                path = []

    return paths_list
