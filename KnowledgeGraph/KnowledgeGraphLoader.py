import pandas as pd
import time
from PredicatesEnum import PredicatesEnum as pe


def fetch_movie_list():
    with open('PrefaceOutput/movie_list.txt', 'r') as f:
        main_list = [[line.replace('[', '').replace('\n', '').replace(']', '').replace('\'', '')] for line in f]

    tmp_frame = pd.DataFrame(main_list, columns=['All'])
    movie_frame = pd.DataFrame(tmp_frame.All.str.split(', ', 2).tolist(), columns=['tconst', 'kind', 'primaryTitle'])
    title_dict = dict(zip(movie_frame.tconst, movie_frame.primaryTitle))
    return title_dict


def write_kg(file, data_set):
    principal = data_set.get('principals')
    titles_dict = fetch_movie_list()

    # For each entry in principal, save it to the KG file with the proper relations
    for i in range(len(principal) - 1):

        # Some ID's from the principal file doesn't exist in titles file/dictionary
        #  and therefore we need to catch the KeyError exception and ignore the missing id
        if principal['tconst'].values[i] in titles_dict:
            # Find the names and titles as well find the category of which the actor had in the movie
            movie_id = principal['tconst'].values[i]
            person_id = principal['nconst'].values[i]
            category = principal['category'].values[i].lower()
            line = line2 = ""

            # If actor or actress
            if category == "actor" or category == "actress":
                line = person_id + "\t" + pe.STARRED_IN + "\t" + movie_id + "\n"
                line2 = movie_id + "\t" + pe.HAS_ACTOR + "\t" + person_id + "\n"

            # If director
            elif category == "director":
                line = person_id + "\t" + pe.DIRECTED + "\t" + movie_id + "\n"
                line2 = movie_id + "\t" + pe.HAS_DIRECTOR + "\t" + person_id + "\n"

            # If writer
            elif category == "writer":
                line = person_id + "\t" + pe.WROTE + "\t" + movie_id + "\n"
                line2 = movie_id + "\t" + pe.HAS_WRITER + "\t" + person_id + "\n"

            # Write to file
            file.write(line)
            file.write(line2)


def run_kgl(data_set):
    start_time = time.time()
    # Create a file which is our knowledge graph and write the header
    kg = open('PrefaceOutput/knowledge_graph.csv', 'w')
    kg.write('subject\tpredicate\tobject\n')

    # Write to the KG file
    write_kg(kg, data_set)

    kg.close()

    end_time = time.time()
    print('     ..Total time (s) for knowledge graph = ' + str(end_time - start_time))
