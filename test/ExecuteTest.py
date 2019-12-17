import time
import pandas as pd
import traceback
from random import choice
from KnowledgeGraph import KGTraversal, Relevance
from QueryProcesing import QueryAnalysis
from utils import Dictionaries
from gensim.models import Word2Vec
from Main import UserSearch


# Load training data
def load_files():
    file = pd.read_csv('wiki-entities_qa_actor_to_movie_dev.csv', header=None, sep="\t")
    return file


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
def count_cal_write(cand_answer, top, file):
    count = 0
    placement = 0
    placement_list = []

    for answer in cand_answer:
        if answer in top:
            placement += top.index(answer) + 1
            placement_list.append(top.index(answer) + 1)
            count += 1

    if count != 0:
        percentage = count / len(cand_answer)
        placement = placement / count
    else:
        percentage = 0.0

    print("Percentage: ", percentage, " Question: ", question)
    print("Their answers: ", cand_answer)
    print("Our answers: ", top)
    print("Placements: ", placement_list, " Average placement: ", placement)

    file.write(
        question + "\t" + str(len(cand_answer)) + "\t" + str(len(top)) + "\t"
        + str(percentage) + "\t" + str(placement_list) + "\t" + str(placement) + "\n")


# Test knowledge graph
def test_kg(cand_answer, paths, file):

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

    count_cal_write(cand_answer, top_kg, file)


# Test relevance
def test_relevance(cand_answer, paths, file, w2v_model, query):
    best_results = Relevance.most_relevant_path(paths, query, w2v_model)

    top_results = []

    for element in best_results:
        top_results.append(element[len(element) - 1])

    count_cal_write(cand_answer, top_results, file)


# Load test data
test_dataset = load_files()

# test_results_kg = open("test.csv", "w+")
test_results = open("test.csv", "w+")
time_results = open("test_time.csv", "w+")

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

        start_time = time.time()

        entity_predicate_list = QueryAnalysis.query_processing(question)

        # Finds paths
        paths_list = UserSearch.find_all_paths(entity_predicate_list, dictionary, kg_graph)

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

        end_time = time.time()
        time_spent = end_time - start_time
        print("Time spent in seconds: ", time_spent)
        time_results.write(str(time_spent))

    except:
        traceback.print_exc()
        continue

# test_results_kg.close()
test_results.close()
time_results.close()


