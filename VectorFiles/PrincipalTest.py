from utils import Dictionaries
from KnowledgeGraph import KGTraversal
from PredicatesEnum import PredicatesEnum as PreEnum


# Open file
file = open("VectorFiles/principal_restructured.txt", "w")

# Create knowledge graph
knowledge_graph = KGTraversal.create_kg_dict()

# Create dictionary
dictionary = Dictionaries.make_dict()

# For each item in our knowledge graph
for entry in knowledge_graph:

    connections = []
    person_id = ""
    string = ""

    try:
        # If we find a name ID
        if "nm" in entry:
            person_id = entry

            # We don't want to save the predicates, only the movie IDs
            for value in knowledge_graph[entry]:
                if value not in PreEnum._value2member_map_:
                    connections.append(value)

            # For all the movies we have found we want to save it in the format,
            # where the actor is always between its movies
            for i in range(len(connections)):

                if i == len(connections) - 1:
                    string += dictionary[person_id] + "," + dictionary[connections[i]] + "\n"
                else:
                    string += dictionary[person_id] + "," + dictionary[connections[i]] + ","

            # Write to file
            file.write(string)

    except KeyError:
        continue

# Close file
file.close()
