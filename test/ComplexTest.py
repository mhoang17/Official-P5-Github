import time
from gensim.models import Word2Vec
from KnowledgeGraph import Relevance, KGTraversal, PathProcessing
from PredicatesEnum import PredicatesEnum as PreEnum
from QueryProcesing import WordToKey
from utils import Dictionaries


# The main run through
def run_main(en_pred_list):

    names = []
    entities_list = []
    predicates = []

    for elem in en_pred_list:
        # We know that idx 0 of the a list in the 'en_pred_list' is the name of the entity
        string = str(elem[0])
        names.append(string)

        # Get the key values of the entities (tt..... : 'Kevin Hart')
        keys = WordToKey.key_value(string, dictionary)
        entities_list.append(keys)

        # We know that idx 1 of the a list in the 'en_pred_list' is the predicates belonging to the entity
        predicates.append(elem[1])

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

            if results:
                # Translate the keys to corresponding their names/values
                translated_results = []
                for result in results:

                    if result not in PreEnum._value2member_map_:
                        translated_results.append(dictionary[result])
                    else:
                        translated_results.append(result)

                all_paths.append(translated_results)

        # When we have found all paths for one entity, we need to move to the next entry in 'predicates'
        predicate_idx += 1

    sec_all_paths = PathProcessing.path_sectioning(all_paths)
    paths_list = PathProcessing.seperate_all_paths(predicates, sec_all_paths, names)

    return paths_list


# Load model
print('[+] Make Model')
model = Word2Vec.load('../PrefaceOutput/word2vec.model')
print('     ..Done with Model\n')

# Load dictionaries
print('[+] Make Dictionaries')
dictionary = Dictionaries.make_dict()
print('     ..Done with Dictionaries\n')

# Load knowledge graph
print('[+] Make KG')
kg_graph = KGTraversal.create_kg_dict()
print('     ..Done with KG\n')

# Our search query and the result our search query analysis phase should have output
question = "movies with X-Men actor who worked with M. Night"
entity_predicates = [["M. Night", [PreEnum.DIRECTED.value, PreEnum.HAS_ACTOR.value, PreEnum.STARRED_IN.value]],
                     ["X-Men", [PreEnum.HAS_ACTOR.value, PreEnum.STARRED_IN.value]]]

# Find all paths
paths = run_main(entity_predicates)

# Find the best results
best_results = Relevance.most_relevant_path(paths, question, model)

# Only the last element answers the search query
top_results = []

for element in best_results:
    top_results.append(element[len(element) - 1])

print(top_results)
