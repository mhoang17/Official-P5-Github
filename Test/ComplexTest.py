from gensim.models import Word2Vec
from KnowledgeGraph import Relevance, KGTraversal
from PredicatesEnum import PredicatesEnum as PreEnum
from utils import Dictionaries
from KnowledgeGraph import RunSearch


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
paths = RunSearch.find_all_paths(entity_predicates, dictionary, kg_graph)

# Find the best results
best_results = Relevance.most_relevant_path(paths, question, model)

# Only the last element answers the search query
top_results = []

for element in best_results:
    top_results.append(element[len(element) - 1])

print(top_results)
