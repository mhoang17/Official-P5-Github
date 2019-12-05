import glob, time, os
import pandas as pd
import gensim
from vectorFiles import TrainModelWord2Vec
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize


def prepare_data(final_list, csv_data_dict):
    # print('\n[+] Preparing the data for model')
    # Create new dataframe with columns as features from new dataframe
    dataframe_features = csv_data_dict.get('names').loc[:, ['primaryName', 'primaryProfession']]

    # Adding the generated list as colunm to the dataframe
    dataframe_features['knownForTitles'] = final_list

    # Timing data preparation  
    start_pre_data = time.time()

    # For each row, combine all the columns into  one column
    combo_list = dataframe_features.apply(lambda x: ','.join(x.astype(str)), axis=1)

    # Store and clean in a pandas dataframe
    df_clean = pd.DataFrame({'clean': combo_list})

    # Create the list of list format of the custom corpus for gensim modeling
    sent = [row.split(',') for row in df_clean['clean']]
    # print(sent[:10])
    end_pre_data = time.time()
    print('     ..Total time (s) for preparing data = ' + str(end_pre_data - start_pre_data) + '\n')

    return TrainModelWord2Vec.train_model(sent)


def actor_known_for_movies(csv_data_dict):
    # Get the data form dataset and make dict of actor and known in movies
    actors_movie_ids = csv_data_dict.get('names')[['primaryName', 'knownForTitles']]
    actors_movie_ids_list = list(zip(actors_movie_ids.primaryName, actors_movie_ids.knownForTitles))
    return actors_movie_ids_list


def movie_titles_and_ids(csv_data_dict):
    # Get the data form dataset and make tuples of movies and their dataset ID
    movies_title_ids = csv_data_dict.get('titles')[['tconst', 'primaryTitle']]
    movie_title_ids_dict = dict(zip(movies_title_ids.tconst, movies_title_ids.primaryTitle))  # {movieName : ttID}
    return movie_title_ids_dict


def data_manipulation(actors_movie_ids_list, movie_title_ids_dict):
    list_of_know_titles = []
    final_list = []

    for actor_Name, ttIDs in actors_movie_ids_list:
        list_of_know_titles = []
        list_of_know_titles.append(ttIDs.split(','))
        place_holder_string = ''
        count_list = list_of_know_titles[0]
        for tID in count_list:
            if tID == '\\N':
                break

            try:
                place_holder_string += actor_Name + ','
                place_holder_string += movie_title_ids_dict[tID]

            except KeyError:
                continue

            if tID != count_list[len(count_list) - 1]:
                place_holder_string += ','

        final_list.append(place_holder_string)

    return final_list


def run_model(data_set):
    # print('\n[+] Running... please wait \n')
    # path = 'csvFiles/*.csv' # use your path
    # dataset = Preface.csv_Data_Dict
    known_for_tuple_list = actor_known_for_movies(data_set)
    movie_titles_in_dict = movie_titles_and_ids(data_set)
    final_list = data_manipulation(known_for_tuple_list, movie_titles_in_dict)
    prepare_data(final_list, data_set)
