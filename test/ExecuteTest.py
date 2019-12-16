import time
import pandas as pd
import traceback
from random import choice
from KnowledgeGraph import KGTraversal, PathProcessing, Relevance
from QueryProcesing import QueryAnalysis, WordToKey
from utils import Dictionaries
from gensim.models import Word2Vec
from PredicatesEnum import PredicatesEnum as PreEnum


# Load training data
def load_files():
    file = pd.read_csv('wiki-entities_qa_actor_to_movie_dev.csv', header=None, sep="\t")
    return file


# The main run through
def run_main(en_pred_list):

    names = []
    entities_list = []
    predicates = []

    for elem in en_pred_list:
        # We know that idx 0 of the a list in the 'en_pred_list' is the name of the entity
        string = str(elem[0])
        names.append(string)

        # Get the key values of the entities (nm..... : 'Kevin Hart')
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


# Randomize Paths
def randomize_paths(paths):
    len_paths_list = len(paths)
    unsorted_paths_list = []

    for i in range(len_paths_list):
        # Randomly choose an element from list
        element = choice(paths)
        unsorted_paths_list.append(element)
        # Pop the chosen element so it cannot be chosen again
        paths.pop(paths.index(element))

    return unsorted_paths_list


# Count, calculate percentages and write to file
def count_cal_write(answers, top, file):
    count = 0
    placement = 0
    placement_list = []

    for answer in answers:
        if answer in top:
            placement += top.index(answer) + 1
            placement_list.append(top.index(answer) + 1)
            count += 1

    if count != 0:
        percentage = count / len(answers)
        placement = placement / count
    else:
        percentage = 0.0

    print("Percentage: ", percentage, " Question: ", question)
    print("Their answers: ", answers)
    print("Our answers: ", top)
    print("Placements: ", placement_list, " Average placement: ", placement)

    file.write(
        question + "\t" + str(len(answers)) + "\t" + str(len(top)) + "\t"
        + str(percentage) + "\t" + str(placement_list) + "\t" + str(placement) + "\n")


# Test knowledge graph
def test_kg(answers, paths, file):

    # List of top 10
    top_kg = []

    # If we have ten or more paths only show the ten paths
    if len(paths) >= 10:
        for i in range(10):
            top_kg.append(paths[i][len(paths[i]) - 1])
    # Else show the paths we found
    else:
        for path in paths:
            top_kg.append(path[len(path) - 1])

    count_cal_write(answers, top_kg, file)


# Test relevance
def test_relevance(answers, paths, file, model, query):
    best_results = Relevance.most_relevant_path(paths, query, model)

    top_results = []

    for element in best_results:
        top_results.append(element[len(element) - 1])

    count_cal_write(answers, top_results, file)


# Load test data
test_dataset = load_files()

# Files load
#test_results_kg = open("test.csv", "w+")
test_results = open("test.csv", "w+")

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


answer_idx = 0
for question in test_dataset[0]:
    try:
        # Answers to the question from dataset
        answers = test_dataset[1][answer_idx].split(", ")
        answer_idx += 1

        entity_predicate_list = QueryAnalysis.query_processing(question)

        # Finds paths
        paths_list = run_main(entity_predicate_list)

        # Comment this in if we want to randomize paths
        # paths_list = randomize_paths(paths_list)

        # Comment this in if we want to reverse paths
        # paths_list.reverse()

        # Comment this in to test the kg
        # print("Knowledge graph")
        # test_kg(answers, paths_list, test_results_kg)

        # Find the best matching result
        # print("Relevance calculated")
        test_relevance(answers, paths_list, test_results, model, question)


    except:
        traceback.print_exc()
        continue

#test_results_kg.close()
test_results.close()



