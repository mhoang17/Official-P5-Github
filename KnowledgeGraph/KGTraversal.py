import csv
from collections import defaultdict


def create_kg_dict():
    per_subject = defaultdict(list)
    with open('KnowledgeGraph/knowledge_graph.csv') as input_file:
        reader = csv.reader(input_file, delimiter="\t")
        next(reader, None)
        for row_num, row_list in enumerate(reader, start=1):
            subject, predicate, object = row_list
            per_subject[subject].append(predicate)
            per_subject[subject].append(object)

    return per_subject


def find_all_paths(graph, start, edges, visited_nodes, j):
    paths = []
    for i in range(len(graph[start]) - 1):
        if graph[start][i] == edges[j] and i != len(graph[start]):
            i += 1
            if graph[start][i] not in visited_nodes:
                paths.append(graph[start][i])
                visited_nodes.append(graph[start][i])
                if j != len(edges) - 1:
                    new_path = find_all_paths(graph, graph[start][i], edges, visited_nodes, j + 1)
                    paths = paths + new_path
    return paths
