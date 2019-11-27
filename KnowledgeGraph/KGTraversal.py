import csv
from collections import defaultdict


# Function to create the dictionary. The dictionary per_subject is represented as a dictionary of lists
def create_kg_dict():
    per_subject = defaultdict(list)
    with open('KnowledgeGraph/knowledge_graph.csv') as input_file:
        reader = csv.reader(input_file, delimiter="\t")
        next(reader, None)  # Ensures that we skip the header in the knowledge_graph.csv
        for row_num, row_list in enumerate(reader, start=1):
            subject, predicate, object = row_list  # A list of a subject, predicate, object
            # The next two lines append for each subject in per_subject dictionary a predicate and an object
            per_subject[subject].append(predicate)
            per_subject[subject].append(object)
    return per_subject


# Function to find all the paths from a starting node
def find_all_paths(graph, start, edges, visited_nodes, j):
    paths = []
    for i in range(len(
            graph[start]) - 1):  # Iterates through the span of the length of the values of the entry of the dictionary
        if graph[start][i] == edges[j] and i != len(graph[start]):
            i += 1
            #  If the current node has not been visited before, it will be added to the path
            #  and to the list of the visited nodes
            if graph[start][i] not in visited_nodes:
                paths.append(graph[start][i])
                visited_nodes.append(graph[start][i])
                #  As long as we have not reached the end of the list of edges
                if j != len(edges) - 1:
                    new_path = find_all_paths(graph, graph[start][i], edges, visited_nodes, j + 1)
                    paths = paths + new_path
    return paths
