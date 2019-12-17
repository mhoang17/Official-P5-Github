from KnowledgeGraph import RunSearch
from utils import Dictionaries
from KnowledgeGraph import KGTraversal, Relevance
import traceback
from QueryProcesing import QueryAnalysis
from gensim.models import Word2Vec


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

# We have a while loop that runs forever, so we don't need to reload the dictionary every time we search
while True:
    try:
        # User input
        user_input = input("Enter your search: ")

        # Query analysis - output is a list of all entities and which predicates that should be in the path
        # (Eg. [['Tom Hanks', [starred_in]], ['Steven Spielberg',[directed]]])
        entity_predicate_list = QueryAnalysis.query_processing(user_input)

        # Call the first-class object find_all_paths
        paths_list = RunSearch.find_all_paths(entity_predicate_list, dictionary, kg_graph)

        # Find the best matching result
        best_results = Relevance.most_relevant_path(paths_list, user_input, model)

        # Loop through the best_results and print each element
        for element in best_results:
            print(element[len(element) - 1])

    except:
        traceback.print_exc()
        print("A problem occurred while your search ran. Please try again.")
        continue
