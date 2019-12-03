import csv
from collections import defaultdict


# Function to create the dictionary. The dictionary per_subject is represented as a dictionary of lists
def create_kg_dict():
    per_subject = defaultdict(list)
    with open('PrefaceOutput/knowledge_graph.csv') as input_file:
        reader = csv.reader(input_file, delimiter="\t")
        next(reader, None)  # Ensures that we skip the header in the knowledge_graph.csv
        for row_num, row_list in enumerate(reader, start=1):
            subject, predicate, object = row_list  # Row_list is a list of a subject, predicate, object
            # The next two lines append for each subject in per_subject dictionary a predicate and an object.
            # This means that idx 0,2,4... (even numbers) is the value of the predicate/edge
            # and uneven numbers are the object that are connected to the subject through the previous predicate
            per_subject[subject].append(predicate)
            per_subject[subject].append(object)
    return per_subject


# Function to find all the paths from a starting node
def find_all_paths(graph, start, edges, visited_nodes, j):
    paths = []
    subject_values = graph[start]
    # Iterates through the span of the length of the values of the entry of the dictionary (graph)
    for i in range(len(subject_values) - 1):
        #  If the edge that is outgoing from the subject is equal to the edge that is supposed to be "visited"
        #  then we should visit the object
        if subject_values[i] == edges[j] and i != len(subject_values):
            i += 1
            #  If the current node has not been visited before, it will be added to the path
            #  and to the list of the visited nodes
            if subject_values[i] not in visited_nodes:
                paths.append(start)
                paths.append(edges[j])
                paths.append(subject_values[i])
                visited_nodes.append(subject_values[i])
                #  As long as we have not reached the end of the list of edges
                if j != len(edges) - 1:
                    #  Store the traversal of graph into the variable new_path and then add new_path to
                    #  the already existing paths
                    new_path = find_all_paths(graph, subject_values[i], edges, visited_nodes, j + 1)
                    paths += new_path
    return paths
