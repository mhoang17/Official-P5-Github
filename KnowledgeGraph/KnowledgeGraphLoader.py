import pandas as pd

# Read the files with actor names, movie titles and principal (relations between actors and movies)
names = pd.read_csv("names.csv", sep=',', nrows=200000, low_memory=False)
titles = pd.read_csv("titles.csv", sep='\t', low_memory=False, encoding="ISO-8859-1")
principal = pd.read_csv("principal.csv", sep=',', nrows=900000, low_memory=False)

# We only need specific information, so we store them here
names = names[['nconst', 'primaryName']]
titles = titles[['tconst', 'primaryTitle']]
principal = principal[['tconst', 'nconst', 'category']]

# Create a file which is our knowledge graph and write the header
f = open('knowledge_graph.csv', 'w')
f.write('subject\tpredicate\tobject\n')


# The function which finds all the relations between a person and movies through the principal file
def write_knowledge_graph(movie_id):
    # First we find the nconst of the person
    tconst = titles['tconst'].values[movie_id]

    # Find all entries of nconst in the principal sub-dataset
    relations = principal.loc[principal['tconst'] == tconst]

    # For all the entries split tconst and categories from each other to make writing easier
    nconst = relations['nconst'].values
    category = relations['category'].values

    # Here we find the predicate: if actor/actress: starred_in, director: directed_by, writer: written_by
    for i in range(len(nconst)):
        if category[i].lower() == "actor" or category[i].lower() == "actress":
            line = nconst[i] + "\tstarred_in\t" + tconst + "\n"
            line_2 = tconst + "\thas_actor\t" + nconst[i] + "\n"
            f.write(line)
            f.write(line_2)
        elif category[i].lower() == "director":
            line = nconst[i] + "\tdirected\t" + tconst + "\n"
            line_2 = tconst + "\tdirected_by\t" + nconst[i] + "\n"
            f.write(line)
            f.write(line_2)
        elif category[i].lower() == "writer":
            line = nconst[i] + "\thas_written\t" + tconst + "\n"
            line_2 = tconst + "\twritten_by\t" + nconst[i] + "\n"
            f.write(line)
            f.write(line_2)


# For n people, run function and write relations to file
NUMBER_OF_MOVIES = 500
for i in range(NUMBER_OF_MOVIES):
    write_knowledge_graph(i)

# Closing the knowledge graph file
f.close()
