from collections import defaultdict
import pandas as pd

# Read the files with actor names, movie titles and principal (relations between actors and movies)
names = pd.read_csv("names.csv", sep='\t', low_memory=False)
titles = pd.read_csv("titles.csv", sep='\t', low_memory=False, encoding="ISO-8859-1")
principal = pd.read_csv("principal.csv", sep='\t', low_memory=False)

# Dictionaries
names_dict = {}
titles_dict = {}
principal_dict = defaultdict(list)

# Load all names into the names dictionary
for i in range(len(names)-1):
    names_dict[names['nconst'].values[i]] = names['primaryName'].values[i]

# Load all titles into the titles dictionary
for i in range(len(titles)-1):
    titles_dict[titles['tconst'].values[i]] = titles['primaryTitle'].values[i]

# Load all relations into the principal dictionary
for i in range(len(principal)-1):

    # Some ID's from the principal file doesn't exist in titles file/dictionary and therefore we need to catch the
    # KeyError exception and ignore the missing id
    try:
        # Find the names and titles as well find the category of which the actor had in the movie
        movie_title = titles_dict[principal['tconst'].values[i]]
        actor_name = names_dict[principal['nconst'].values[i]]
        category = principal['category'].values[i]

        principal_dict[movie_title].append(category)
        principal_dict[movie_title].append(actor_name)

    except KeyError:
        continue

# Create a file which is our knowledge graph and write the header
kg = open('knowledge_graph.csv', 'w')
kg.write('subject\tpredicate\tobject\n')


# The function which finds all the relations between a person and movies through the principal file
def write_knowledge_graph(movie_name):

    # Values of the title
    values = principal_dict[movie_name]

    for idx in range(len(values) - 1):

        line = line2 = ""
        # Actor or Actress
        if values[idx].lower() == 'actor' or values[idx].lower() == 'actress':
            line = values[idx + 1] + "\tstarred_in\t" + movie_name + "\n"
            line2 = movie_name + "\thas_actor\t" + values[idx + 1] + "\n"

        # Director
        elif values[idx].lower() == 'director':
            line = values[idx + 1] + "\tdirected\t" + movie_name + "\n"
            line2 = movie_name + "\tdirected_by\t" + values[idx + 1] + "\n"

        # Writer
        elif values[idx].lower() == 'writer':
            line = values[idx + 1] + "\thas_written\t" + movie_name + "\n"
            line2 = movie_name + "\twritten_by\t" + values[idx + 1] + "\n"

        # Write to file
        kg.write(line)
        kg.write(line2)


for name in titles_dict:
    write_knowledge_graph(titles_dict[name])

kg.close()