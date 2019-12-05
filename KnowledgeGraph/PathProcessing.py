def path_sectioning(all_paths):
    # This is a list where the list of all paths is sectioned up into pieces.
    # (Eg. [['tom hanks', 'starred_in', 'forrest gump'], ['tom hanks', 'starred_in', 'the green mile'],...]
    # This is necessary to do in order for all paths to be separated and therefore we are easier able to find the
    # relevance of the path in the later stages.
    sec_all_paths = []

    # 'Part' represents a part of all paths
    part = []

    # 'entity_paths' is one entry in the 'all_paths' aka. all paths for one entity
    for entity_paths in all_paths:
        for i in range(len(entity_paths)):
            # If we find the name of the entity, we know that this is the beginning of a path.
            if entity_paths[i] == entity_paths[0]:

                part.append(entity_paths[i])

                for j in range(i + 1, len(entity_paths)):
                    # If we find the name again then it's the beginning of a new path and we should stop
                    # our current path
                    if entity_paths[j] == entity_paths[0]:
                        break

                    part.append(entity_paths[j])

                # Add the found path
                sec_all_paths.append(part)

                # Reset the path
                part = []

    return sec_all_paths


def seperate_all_paths(predicates, sec_all_paths, names):
    paths_list = []
    predicate = predicates[0]
    idx = 1

    for elements in sec_all_paths:

        # This is only important if there are more entities and we therefore need to switch between predicate lists
        if len(predicates) > 1:
            # This is a fail safe measure so we don't get a out of bounds exception
            if idx < len(predicates) and idx < len(names):
                # If the next element is the name of the next entity, we need to switch to the predicate list
                # that belongs to that specific entity
                if names[idx] in elements[len(elements) - 1]:
                    predicate = predicates[idx]
                    idx += 1

        # We reverse the list because it is easier to go backwards, because the end node will only occur once.
        elements.reverse()

        # Here we store the path
        path = []

        # This will be important if we have found a part of the part and need the next predicate to know which
        # path we now need to take
        k = len(predicate) - 1

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
            if len(path) == len(predicate) * 2 + 1:
                # Reverse it so it will be in the correct order
                path.reverse()
                paths_list.append(path)

            # Reset path
            path = []

    return paths_list
