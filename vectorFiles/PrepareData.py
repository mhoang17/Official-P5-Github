import glob, time, os
import pandas as pd
import gensim
import LoadFiles
import TrainModelWord2Vec
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

def Word_2_Vec_Model(final_List, csv_Data_Dict):
    print('\n[+] Preparing the data for model')
    # Create new dataframe with columns as features from new dataframe
    dataFrame_Features = csv_Data_Dict.get('names').loc[:,['primaryName','primaryProfession']][:10]
    
    # Adding the generated list as colunm to the dataframe
    dataFrame_Features['knownForTitles'] = final_List

    # Timing data preparation  
    start_Pre_Data = time.time()

    # For each row, combine all the columns into  one column
    combo_Colunm_List = dataFrame_Features.apply(lambda x: ','.join(x.astype(str)), axis=1)

    # Store and clean in a pandas dataframe
    df_clean = pd.DataFrame({'clean': combo_Colunm_List})

    # Create the list of list format of the custom corpus for gensim modeling
    sent = [row.split(',') for row in df_clean['clean']]
    print(sent[:10])
    end_Pre_data = time.time()
    print('     ..Total time (s) for preparing data = ' + str(end_Pre_data-start_Pre_Data) + '\n')
    
    return TrainModelWord2Vec.train_model(sent)

def actor_Known_For_Movies(csv_Data_Dict):
    # Get the data form dataset and make dict of actor and known in movies
    Actors_Movie_IDs = csv_Data_Dict.get('names')[['primaryName', 'knownForTitles']][:10]
    Actors_Movie_IDs_List = list(zip(Actors_Movie_IDs.primaryName, Actors_Movie_IDs.knownForTitles))
    return Actors_Movie_IDs_List

def movie_Titles_And_IDs(csv_Data_Dict): 
    # Get the data form dataset and make tuples of movies and their dataset ID
    movies_Title_IDs = csv_Data_Dict.get('titles')[['tconst','primaryTitle']]
    movie_Title_IDs_Dict = dict(zip(movies_Title_IDs.tconst, movies_Title_IDs.primaryTitle)) # {movieName : ttID} 
    return movie_Title_IDs_Dict


def data_Manipulation(Actors_Movie_IDs_List, movie_Title_IDs_Dict):
    list_Of_Know_Titles = []    
    final_List = []

    for actor_Name, ttIDs in Actors_Movie_IDs_List:
        list_Of_Know_Titles = []
        list_Of_Know_Titles.append(ttIDs.split(','))
        place_Holder_String = ''
        count_List = list_Of_Know_Titles[0]
        for tID in count_List:
            if tID == '\\N':
                break
                
            try:
                place_Holder_String += actor_Name + ','
                place_Holder_String  += movie_Title_IDs_Dict[tID]
                
            except KeyError:
                continue
                
            if tID != count_List[len(count_List)-1]:
                place_Holder_String += ','

        final_List.append(place_Holder_String)
    
    return final_List 


print('\n[+] Running... please wait \n')
path = 'csvFiles/*.csv' # use your path
dataset = LoadFiles.read_Files(path)
known_For_Tuple_List = actor_Known_For_Movies(dataset)
movie_Titles_In_Dict = movie_Titles_And_IDs(dataset)
final_List = data_Manipulation(known_For_Tuple_List, movie_Titles_In_Dict)
Word_2_Vec_Model(final_List, dataset)


