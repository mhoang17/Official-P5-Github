import glob, time, os
import pandas as pd
import gensim
import LoadFiles
import TrainModelWord2Vec
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize

def Word2VecModel(finalList, csvDataDict):
    print('\n[+] Preparing the data for model')
    # Create new dataframe with columns as features from new dataframe
    dataFrameFeatures = csvDataDict.get('names').loc[:,['primaryName','primaryProfession']] 
    
    # Adding the generated list as colunm to the dataframe
    dataFrameFeatures['knownForTitles'] = finalList

    # Timing data preparation  
    startPreData = time.time()

    # For each row, combine all the columns into  one column
    comboColunmList = dataFrameFeatures.apply(lambda x: ','.join(x.astype(str)), axis=1)

    # Store and clean in a pandas dataframe
    df_clean = pd.DataFrame({'clean': comboColunmList})

    # Create the list of list format of the custom corpus for gensim modeling
    sent = [row.split(',') for row in df_clean['clean']]
    print(sent[:10])
    endPredata = time.time()
    print('     ..Total time (s) for preparing data = ' + str(endPredata-startPreData) + '\n')
    
    return TrainModelWord2Vec.trainModel(sent)

def actorKnownForMovies(csvDataDict):
    # Get the data form dataset and make dict of actor and known in movies
    ActorsMovieIDs = csvDataDict.get('names')[['primaryName', 'knownForTitles']]
    ActorsMovieIDsList = list(zip(ActorsMovieIDs.primaryName, ActorsMovieIDs.knownForTitles))
    return ActorsMovieIDsList

def movieTitlesAndIDs(csvDataDict): 
    # Get the data form dataset and make tuples of movies and their dataset ID
    moviesTitleIDs = csvDataDict.get('titles')[['tconst','primaryTitle']]
    movieTitleIDsDict = dict(zip(moviesTitleIDs.tconst, moviesTitleIDs.primaryTitle)) # {movieName : ttID} 
    return movieTitleIDsDict


def dataManipulation(ActorsMovieIDsList, movieTitleIDsDict):
    listOfKnowTitles = []    
    finalList = []

    for actorName, ttIDs in ActorsMovieIDsList:
        listOfKnowTitles = []
        listOfKnowTitles.append(ttIDs.split(','))
        placeHolderString = ''
        countList = listOfKnowTitles[0]
        for tID in countList:
            if tID == '\\N':
                break
                
            try:
                placeHolderString += actorName + ','
                placeHolderString  += movieTitleIDsDict[tID]
                
            except KeyError:
                continue
                
            if tID != countList[len(countList)-1]:
                placeHolderString += ','

        finalList.append([placeHolderString])
    
    return finalList 


print('\n[+] Running... please wait \n')
path = 'csvFiles/*.csv' # use your path
dataset = LoadFiles.readFiles(path)
knownForTupleList = actorKnownForMovies(dataset)
movieTitlesInDict = movieTitlesAndIDs(dataset)
finalList = dataManipulation(knownForTupleList, movieTitlesInDict)
Word2VecModel(finalList, dataset)


