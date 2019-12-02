import Dictionaries
from KnowledgeGraph import KGTraversal
from PredicatesEnum import PredicatesEnum as PreEnum
import QueryAnalysisCopy
import traceback

# Create the dictionary of all ID's and their names
dictionary = Dictionaries.make_dict()

# Convert the KG csv file to a dictionary
kg_graph = KGTraversal.create_kg_dict()


# When the search query is processed we want to convert the entities to their respective ID's
def get_key(val):
    key_list = []

    for key, value in dictionary.items():
        # If the input value is contained in one of the names (dictionary value) then the key to the name is saved
        if val in value:
            key_list.append(key)

    return key_list


# We have a while loop that runs forever, so we don't need to reload the dictionary every time we search
while True:

    # Right now it's just an exception handler that just continues if there is any error
    # (should probably be fixed later)
    try:
        # User input
        name_input = input("Enter your search: ")

        # Query analysis - output is a list of all entities and which predicates that should be in the path
        # (Eg. [['Tom Hanks', [starred_in]], ['Steven Spielberg',[directed]]])
        entity_predicate_list = QueryAnalysisCopy.query_processing(name_input)

        # TODO: delete this print
        print(entity_predicate_list)

        # List of all the names/entities that occurred in the search
        names = []

        # List of all the IDs of the names/entities (same names/entities as the "names" list".
        entities_list = []

        # List of all predicates. The index of the "predicates" is 1:1 to the "entities" and "names" lists.
        # (Eg. names[0] = 'Tom Hanks' : predicates[0] = ['starred_in']
        #      names[1] = 'Steven Spielberg' : predicates[1] = ['directed'])
        predicates = []

        # Split each element of the entity_predicate_list so they end up in either 'names', 'entities_list'
        # or 'predicates' depending on what they are
        for elem in entity_predicate_list:
            # We know that idx 0 of the a list in the 'entity_predicate_list' is the name of the entity
            string = str(elem[0]).lower()
            names.append(string)

            # Get the key values of the entities (tt..... : 'Kevin Hart')
            keys = get_key(string)
            entities_list.append(keys)

            # We know that idx 1 of the a list in the 'entity_predicate_list' is the predicates belonging to the entity
            predicates.append(elem[1])

        # TODO: delete this prints statement
        print(names)

        # List where we save all paths for all entities that starts from the entities and follows the predicates
        # (Eg. ['Tom Hanks' -> 'starred_in' -> 'Forrest Gump'] is one path that starts from
        # the entity 'Kevin Hart' and follows the predicate(s) 'starred_in' until it finds a result.)
        all_paths = []
        predicate_idx = 0

        # There are many people or titles that can be named the same, therefore we go through all of them and check
        # which relations they have
        for entities in entities_list:
            for entity in entities:
                # List of already visited notes so we don't re-visit them
                already_visited = [entity]

                # We run the current key through the function that does the graph traversal
                results = KGTraversal.find_all_paths(kg_graph, entity, predicates[predicate_idx], already_visited, 0)

                # We only want to save those paths which has values, if results is empty then it means
                # that there were no path which had the predicates in the correct order
                # (Eg. 'Steven Spielberg -> 'starred_in' -> 'movie' is not a valid path if we go with
                #       our previous example.)
                if results:
                    # Translate the keys to corresponding their names/values
                    translated_results = []
                    for result in results:
                        # If the result is a predicate then it should automatically be added to the "translated list".
                        # This is to assure that the "translated list" is exactly that: a translated version of the
                        # list of results where everything is the same order except that instead of IDs it's
                        # the name/value of the id
                        if result not in PreEnum.value2member_map_:
                            translated_results.append(dictionary[result])
                        else:
                            translated_results.append(result)

                    all_paths.append(translated_results)

            # When we have found all paths for one entity, we need to move to the next entry in 'predicates'
            predicate_idx += 1

        # all_paths will look like [['tom hanks', 'starred_in', 'forrest gump',
        #                            'tom hanks', 'starred_in', 'the green mile',...],
        #                           ['steven spielberg', 'directed', 'jurassic park',
        #                            'steven spielberg', 'directed', 'E.T.',...]]

        # TODO: delete this print
        print("Result: ", all_paths)

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

        # TODO: delete print
        print("Combined Answer: ", sec_all_paths)

        # The next part is necessary if paths are longer than three (eg. ['tom hanks', 'starred_in', 'forrest gump'])
        # A path can be longer than three if there are more than one predicate for that entity.
        # Eg. actor who worked with Kevin Hart will result in for example
        # entities_predicate_list = ['Kevin Hart', ['starred_in', 'has_actor']]
        # all_paths = ['Kevin Hart', 'starred_in', 'Central Intelligence',
        #              'Central Intelligence', has_actor, 'Dwayne Johnson',
        #              'Central Intelligence', 'has_actor', 'actor2',...,
        #              'Kevin Hart', 'starred_in', 'Jumanji: Welcome to the Jungle',
        #              'Jumanji: Welcome to the Jungle', 'has_actor', 'Dwayne Johnson',
        #              'Jumanji: Welcome to the Jungle', 'has_actor', 'actor3',...]
        # sec_all_paths = [['Kevin Hart', 'starred_in', 'Central Intelligence',
        #                   'Central Intelligence', has_actor, 'Dwayne Johnson',
        #                   'Central Intelligence', 'has_actor', 'actor2',...],
        #                  ['Kevin Hart', 'starred_in', 'Jumanji: Welcome to the Jungle',
        #                   'Jumanji: Welcome to the Jungle', 'has_actor', 'Dwayne Johnson',
        #                   'Jumanji: Welcome to the Jungle', 'has_actor', 'actor3'],...]
        # This we cannot use when calculating the relevance and we need to reformat it
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

        # TODO: change this print to be the input parameter for the relevance function
        print(paths_list)

    # TODO: change this except to catch specific expcetions
    except:
        traceback.print_exc()
        continue
