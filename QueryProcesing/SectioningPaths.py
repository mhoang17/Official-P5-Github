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
