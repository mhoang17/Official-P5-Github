import pandas as pd
from KnowledgeGraph import KGTraversal, PathProcessing, Relevance
from QueryProcesing import QueryAnalysis, WordToKey
from utils import Dictionaries
from gensim.models import Word2Vec
from PredicatesEnum import PredicatesEnum as PreEnum
import traceback


def load_files():

    file = pd.read_csv('wiki-entities_qa_actor_to_movie_dev.csv', header=None, sep="\t")
    return file

file = load_files()

test_results = open("test_results.csv", "w+")

print('[+] Make Dictionaries')
dictionary = Dictionaries.make_dict()
print('     ..Done with Dictionaries\n')
print('[+] Make KG')
kg_graph = KGTraversal.create_kg_dict()
print('     ..Done with KG\n')
print('[+] Make Model')
model = Word2Vec.load('../PrefaceOutput/word2vec.model')
print('     ..Done with Model\n')

answer_idx = 0

for question in file[0]:
    try:
        answers = file[1][answer_idx].split(", ")
        answer_idx += 1
        entity_predicate_list = QueryAnalysis.query_processing(question)
        names = []
        entities_list = []
        predicates = []

        for elem in entity_predicate_list:
            # We know that idx 0 of the a list in the 'entity_predicate_list' is the name of the entity
            string = str(elem[0])
            names.append(string)

            # Get the key values of the entities (tt..... : 'Kevin Hart')
            keys = WordToKey.key_value(string, dictionary)
            entities_list.append(keys)

            # We know that idx 1 of the a list in the 'entity_predicate_list' is the predicates belonging to the entity
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

        # Find the best matching result
        best_results = Relevance.most_relevant_path(paths_list, question, model)

        top_ten = []

        for element in best_results:
            top_ten.append(element[len(element) - 1])

        count = 0

        for answer in answers:
            if answer in top_ten:
                count += 1

        if count != 0:
            percentage = count/len(answers)
        else:
            percentage = 0.0

        print("Percentage: ", percentage, " Question: ", question)
        print("Their answers: ", answers)
        print("Our answers: ", top_ten, "\n")

        test_results.write(question + "\t" + str(len(answers)) + "\t" + str(len(top_ten)) + "\t" + str(percentage) + "\n")

    except:
        traceback.print_exc()
        continue

test_results.close()
