import pandas as pd
import Dictionaries


def write_kg(file):
    principal = pd.read_csv("../csvFiles/principals.csv", sep=',', nrows=3000000, low_memory=False)
    titles_dict = Dictionaries.make_titles_dict()

    # For each entry in principal, save it to the KG file with the proper relations
    for i in range(len(principal) - 1):

        # Some ID's from the principal file doesn't exist in titles file/dictionary
        #  and therefore we need to catch the KeyError exception and ignore the missing id
        try:
            # Find the names and titles as well find the category of which the actor had in the movie
            titles_dict[principal['tconst']]

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

        except KeyError:
            continue


# Create a file which is our knowledge graph and write the header
kg = open('knowledge_graph.csv', 'w')
kg.write('subject\tpredicate\tobject\n')

# Write to the KG file
write_kg(kg)

kg.close()
