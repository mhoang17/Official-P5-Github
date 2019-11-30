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

        # TODO: we need the query analysis phase right here
        new_input = QueryAnalysisCopy.query_processing(name_input)

        print(new_input)

        names = []
        entities_list = []
        predicates = []

        for elem in new_input:
            string = str(elem[0]).lower()
            names.append(string)
            # Get the key values of the entities found in the previous stage
            keys = get_key(string)
            entities_list.append(keys)
            predicates.append(elem[1])

        print(names)
        # List where we save all candidate answers
        candidate_answers = []
        i = 0

        # There are many people or titles that can be named the same, therefore we go through all of them and check
        # which relations they have
        for entities in entities_list:
            for entity in entities:
                # List of already visited notes so we don't re-visit them
                already_visited = [entity]

                # We run the current key through the function that does the graph traversal
                results = KGTraversal.find_all_paths(kg_graph, entity, predicates[i], already_visited, 0)

                # We only want to save those paths which has values, if results is empty then it means
                # that there were no path which had the predicates in the correct order
                if results:
                    # Translate the keys to their names
                    translated_results = []
                    for result in results:
                        # If the result is not a predicate it should be translated into its value
                        if result not in PreEnum.value2member_map_:
                            translated_results.append(dictionary[result])
                        else:
                            translated_results.append(result)

                    candidate_answers.append(translated_results)

            i += 1

        print("Result: ", candidate_answers)

        combined_answer = []
        part = []
        for answer in candidate_answers:
            for i in range(len(answer)):
                if answer[i] == answer[0]:
                    part.append(answer[i])
                    for j in range(i + 1, len(answer)):
                        if answer[j] == answer[0]:
                            break
                        part.append(answer[j])
                    combined_answer.append(part)
                    part = []

        print("Combined Answer: ", combined_answer)

        paths_list = []
        predicate = predicates[0]
        idx = 1

        for elements in combined_answer:
            elements.reverse()
            path = []

            k = len(predicate) - 1

            if len(predicates) > 1:
                if idx < len(predicates) and idx < len(names):
                    if names[idx] in elements[len(elements) - 1]:
                        predicate = predicates[idx]
                        idx += 1

            for l in range(len(elements)):

                if elements[l] == predicate[k]:
                    for j in range(l, len(elements)):
                        if elements[j] == predicate[k]:

                            path.append(elements[j - 1])
                            path.append(elements[j])

                            k -= 1

                        elif j == len(elements) - 1:
                            path.append(elements[j])
                            k = len(predicate) - 1

                if path:
                    path.reverse()
                    paths_list.append(path)
                    path = []

        print(paths_list)

        # This cannot be done here, because eg. there are 5 people that have "Kevin Hart in their name"
        # and 4 of them have not been in a movie with Dwayne Johnson, so intersection of all lists will
        # end up us having no result at all
        '''if "and" in name_input:
            intersection_list = candidate_answers[0]
            for i in range(1, len(candidate_answers)):
                print(candidate_answers[i])
                intersection_list = set(intersection_list).intersection(set(candidate_answers[i]))
            candidate_answers = intersection_list

        # TODO: instead of print "candidate answers" should be the input to the relevance function
        print("Result 2: ", candidate_answers)'''

    except:
        traceback.print_exc()
        continue
