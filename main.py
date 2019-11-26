import Dictionaries
from KnowledgeGraph import KGTraversal

dictionary = Dictionaries.make_dict()
kg_graph = KGTraversal.create_kg_dict()


def get_key(val):
    key_list = []
    for key, value in dictionary.items():
        if val in value:
            key_list.append(key)

    return key_list


while True:

    try:
        val = input("Enter your search: ").lower()
        keys = get_key(val)
        predicates = ['has_actor']
        candidate_answers = []

        for node in keys:
            already_visited = [node]
            results = KGTraversal.find_all_paths(kg_graph, node, predicates, already_visited, 0)
            if results:
                for result in results:
                    candidate_answers.append(dictionary[result])

        print(candidate_answers)

    except:
        continue
