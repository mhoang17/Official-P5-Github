from KnowledgeGraph import KGTraversal, PathProcessing
from PredicatesEnum import PredicatesEnum as PreEnum
from QueryProcesing import WordToKey

# Find all paths
def find_all_paths(en_pred_list, dictionary, kg_graph):
    # List of all the names/entities that occurred in the search
    names = []

    # List of all the IDs of the names/entities (same names/entities as the "names" list".
    entities_list = []

    # List of all predicates. The index of the "predicates" is 1:1 to the "entities" and "names" lists.
    # (Eg. names[0] = 'Tom Hanks' : predicates[0] = ['starred_in']
    #      names[1] = 'Steven Spielberg' : predicates[1] = ['directed'])
    predicates = []

    # Split each element of the en_pred_list so they end up in either 'names', 'entities_list'
    # or 'predicates' depending on what they are
    for elem in en_pred_list:
        # We know that idx 0 of the a list in the 'en_pred_list' is the name of the entity
        string = str(elem[0])
        names.append(string)

        # Get the key values of the entities (nm..... : 'Kevin Hart')
        keys = WordToKey.key_value(string, dictionary)
        entities_list.append(keys)

        # We know that idx 1 of the a list in the 'en_pred_list' is the predicates belonging to the entity
        predicates.append(elem[1])

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
                    if result not in PreEnum._value2member_map_:
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
    sec_all_paths = PathProcessing.path_sectioning(all_paths)

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
    paths_list = PathProcessing.seperate_all_paths(predicates, sec_all_paths, names)

    return paths_list

