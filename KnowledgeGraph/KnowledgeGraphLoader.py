import pandas as pd
import time


def fetch_movie_list():
    with open('PrefaceOutput/movieList.txt', 'r') as f:
        mainlist = [[line.replace('[', '').replace('\n', '').replace(']', '').replace('\'', '')] for line in f]

    tmp_frame = pd.DataFrame(mainlist, columns=['All'])
    movie_frame = pd.DataFrame(tmp_frame.All.str.split(', ', 2).tolist(), columns=['tconst', 'kind', 'primaryTitle'])
    title_dict = dict(zip(movie_frame.tconst, movie_frame.primaryTitle))
    return title_dict


def write_kg(file, dataset):
    principal = dataset.get('principals')
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
                line = person_id + "\tstarred_in\t" + movie_id + "\n"
                line2 = movie_id + "\thas_actor\t" + person_id + "\n"

            # If director
            elif category == "director":
                line = person_id + "\tdirected\t" + movie_id + "\n"
                line2 = movie_id + "\tdirected_by\t" + person_id + "\n"

            # If writer
            elif category == "writer":
                line = person_id + "\thas_written\t" + movie_id + "\n"
                line2 = movie_id + "\twritten_by\t" + person_id + "\n"

            # Write to file
            file.write(line)
            file.write(line2)


def run_kgl(dataset):
    start_time = time.time()
    # Create a file which is our knowledge graph and write the header
    kg = open('PrefaceOutput/knowledge_graph.csv', 'w')
    kg.write('subject\tpredicate\tobject\n')

    # Write to the KG file
    write_kg(kg, dataset)

    kg.close()

    end_time = time.time()
    print('     ..Total time (s) for knowledge graph = ' + str(end_time - start_time))
