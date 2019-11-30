import Dictionaries
from KnowledgeGraph import KGTraversal

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
        name_input = input("Enter your search: ").lower()
        predicate_input = input("Enter the predicate").lower()

        # TODO: we need the query analysis phase right here

        # Get the key values of the entities found in the previous stage
        keys = get_key(name_input)
        print(keys)

        # Here the predicates found at the query analysis phase will be placed instead of hardcoded
        predicates = [predicate_input]

        # List where we save all candidate answers
        candidate_answers = []

        # There are many people or titles that can be named the same, therefore we go through all of them and check
        # which relations they have
        for node in keys:

            # List of already visited notes so we don't re-visit them
            already_visited = [node]

            # We run the current key through the function that does the graph traversal
            results = KGTraversal.find_all_paths(kg_graph, node, predicates, already_visited, 0)

            # We only want to save those paths which has values, if results is empty then it means
            # that there were no path which had the predicates in the correct order
            if results:
                # Translate the keys to their names
                translated_results = []
                for result in results:
                    translated_results.append(dictionary[result])

                candidate_answers.append(translated_results)

        # TODO: instead of print "candidate answers" should be the input to the relevance function
        print(candidate_answers)

    except:
        continue
