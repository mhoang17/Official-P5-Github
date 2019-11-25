import csv
from collections import defaultdict

per_subject = defaultdict(list)
with open('knowledge_graph.csv') as inputfile:
    reader = csv.reader(inputfile, delimiter="\t")
    next(reader, None)
    for row_num, row_list in enumerate(reader, start=1):
        subject, predicate, object = row_list
        per_subject[subject].append(predicate)
        per_subject[subject].append(object)


def find_all_paths(graph, start, edges, j):
    paths = []
    for i in range(len(graph[start]) - 1):
        if graph[start][i] == edges[j] and i != len(graph[start]):
            i += 1
            if graph[start][i] not in visited_nodes:
                paths.append(graph[start][i])
                visited_nodes.append(graph[start][i])
            if j != len(edges) - 1:
                new_path = find_all_paths(graph, graph[start][i], edges, j + 1)
                paths = paths + new_path
    return paths


visited_nodes = ['Hamlet']
predicate_list = ['has_actor', 'starred_in']
print(find_all_paths(per_subject, visited_nodes[0], predicate_list, 0))
