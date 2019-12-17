import time
import pandas as pd
from VectorFiles import TrainModelWord2Vec


def prepare_data(final_list, csv_data_dict):
    # print('\n[+] Preparing the data for model')
    # Create new dataframe with columns as features from new dataframe
    dataframe_features = csv_data_dict.get('names').loc[:, ['primaryName', 'primaryProfession']]

    # Adding the generated list as colunm to the dataframe
    dataframe_features['knownForTitles'] = final_list

    # Timing data preparation  
    start_pre_data = time.time()

    # For each row, combine all the columns into one column
    combo_list = dataframe_features.apply(lambda x: ','.join(x.astype(str)), axis=1)

    # Store and clean in a pandas dataframe, such that Word2Vec will accept the corpus
    df_clean = pd.DataFrame({'clean': combo_list})

    # Create the list of list format of the custom corpus for Gensim modeling
    sent = [row.split(',') for row in df_clean['clean']]

    end_pre_data = time.time()
    print('     ..Total time (s) for preparing data = ' + str(end_pre_data - start_pre_data) + '\n')

    return TrainModelWord2Vec.train_model(sent)


def actor_known_for_movies(csv_data_dict):
    # Get the data form dataset and make list of tuples actor and known in movies
    actors_movie_ids = csv_data_dict.get('names')[['primaryName', 'knownForTitles']]

    # E.g of how actors_movie_ids_list looks like [('primaryName', 't0043044, tt0072308, tt0053137, tt0043044')]
    actors_movie_ids_list = list(zip(actors_movie_ids.primaryName, actors_movie_ids.knownForTitles))
    return actors_movie_ids_list


def movie_titles_and_ids(csv_data_dict):
    # Get the data form dataset and make tuples of movies and their dataset ID
    movies_title_ids = csv_data_dict.get('titles')[['tconst', 'primaryTitle']]

    # E.g of how movie_title_ids_dict looks like {movieName : ttID}
    movie_title_ids_dict = dict(zip(movies_title_ids.tconst, movies_title_ids.primaryTitle))
    return movie_title_ids_dict


def data_manipulation(actors_movie_ids_list, movie_title_ids_dict):
    # Initialize empty list 
    list_of_know_titles = []
    final_list = []

    # Loop through the list of tuples actors_movie_ids_list
    # where each element looks like [('primaryName', 't0043044, tt0072308, tt0053137, tt0043044')]
    # E.g of each element in actors_movie_ids_list [(’Fred Astaire’, ’tt0043044,tt0072308,tt0053137,tt0043044’), ... ]
    for actor_Name, ttIDs in actors_movie_ids_list:
        
        # Initialize empty list every time we loop through an element, such that we have a clean list for every actor
        list_of_know_titles = []

        # Split every tID ('t0043044','tt0072308','tt0053137','tt0043044') into each tID separately
        # E.g 't0043044' is a an element in list_of_know_titles
        list_of_know_titles.append(ttIDs.split(','))

        # Initialize empty string for concatenation of actor name and movie title
        place_holder_string = ''

        # Set the count_list to the list of tID
        # E.g ('t0043044','tt0072308','tt0053137','tt0043044')
        count_list = list_of_know_titles[0]

        # Loop through every element in count_list
        # which is ('t0043044','tt0072308','tt0053137','tt0043044')
        # where each tID  = 't0043044'
        for tID in count_list:

            # if '\\N' is encountered in the list, break out of loop and take next element
            if tID == '\\N':
                break

            try:
                # Concatenate the actor name with a comma
                # E.g 'Fred Astaire,'
                place_holder_string += actor_Name + ','

                # Further concatenate the actor name with movie title.
                # The movie title is found by look up in the dictionary using the tID
                # E.g 'Fred Astaire, Funny Face'
                place_holder_string += movie_title_ids_dict[tID]

            except KeyError:
                continue

            # If not the last element in the count_list is reached add a comma,
            # for separation of actor name and movie title
            # E.g 'Fred Astaire, Funny Face, Fred Astaire, The Towering Inferno, .. , .. '
            if tID != count_list[len(count_list) - 1]:
                place_holder_string += ','

        # Add the results(place_holder_string) to the a final list for every element in actors_movie_ids_list
        final_list.append(place_holder_string)

    return final_list


def run_model(data_set):
    # Call actor_known_for_movies with IMDb dataset
    known_for_tuple_list = actor_known_for_movies(data_set)

    # Call movie_titles_in_dict with IMDb dataset
    movie_titles_in_dict = movie_titles_and_ids(data_set)

    # Call data_manipulation with the two functions known_for_tuple_list and movie_titles_in_dict
    final_list = data_manipulation(known_for_tuple_list, movie_titles_in_dict)

    # Call prepare_data with the function final_list and the IMDb dataset
    prepare_data(final_list, data_set)
