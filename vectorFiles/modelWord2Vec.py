import glob, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import gensim
import nltk.data
from gensim.models import Word2Vec
from nltk.tokenize import sent_tokenize, word_tokenize
import multiprocessing

csvDataList = []

def readFiles(csvDataList):
    pd.set_option('display.max_rows', 50)
    path = r'C:\Users\SomeUser\Documents\P5_Project\imdb_dataset' # use your path
    all_files = glob.glob(path + "/*.csv")
    csvDataList = []
    countOf = 1
    print('[+] Runing files ')  
    for filename in all_files:
        print('    ..' + filename +' - '+ str(countOf) +' of '+ str(len(all_files)))
        df = pd.read_csv(filename, header=0, low_memory=False, encoding='utf-8' )
        csvDataList.append(df)
        countOf += 1

    return csvDataList

def printData(csvDataList):
    print(csvDataList[0].head())    
    print(csvDataList[1].head())    
    print(csvDataList[2].head())    
    print(csvDataList[3].head())    
    print(csvDataList[4].head())    
    print(csvDataList[5].head())    
    print(csvDataList[6].head())    
    
def hardWorkingSlave(slaveList):

    return 0
    
def runSlaveWhipper():
    # p = Pool(processes = len(names))
    # start = time.time()
    # async_result = p.map_async(hardWorkingSlave, names)
    # p.close()
    # p.join()
    # print("Complete")
    # end = time.time()
    # print('Total time (s)= ' + str(end-start))

    return 0

def Word2VecAndTrainModel(finalList, csvDataList):
    # Create new dataframe with wanted combined colunms
    #csvDataList[0]['ttID_Actor_birth'] = csvDataList[0]['nconst'] + ' ' + csvDataList[0]['primaryName']
    print('[-] Setting up the data for training of model')
    # Create new dataframe with columns as features from new dataframe
    #csvDataList[0]['knownForMovies'] = finalList
    dataFrameFeatures = csvDataList[0].loc[:,['primaryProfession','birthYear','primaryName' ]] 

    dataFrameFeatures['knownForTitles'] = finalList

    #print(dataFrameFeatures.head())

    #dataFrameFeatures  = dataFrameFeatures['knownForTitles'].apply(','.join)
    print('     ..Preparing data')
    startPreData = time.time()

    # For each row, combine all the columns into  one column
    comboColunmList = dataFrameFeatures.apply(lambda x: ','.join(x.astype(str)), axis=1)

    # Store and clean in a pandas dataframe
    df_clean = pd.DataFrame({'clean': comboColunmList})

    # Create the list of list format of the custom corpus for gensim modeling
    sent = [row.split(',') for row in df_clean['clean']]
    #print(sent[:])
    endPredata = time.time()
    print('     ..Total time (s) for preparing data = ' + str(endPredata-startPreData) + '\n')

    # train the model with dataset
    print('[+] Training the model')
    startTraining = time.time()


    model = Word2Vec(sent, min_count=1 ,size=100, workers=4, window = 7, sg = 1)
    
    endTraining = time.time()
    print('     ..Total time (s) for preparing data = ' + str(endTraining-startTraining) + '\n')
    #model.most_similar('Funny Face')
    similarities = model.wv.most_similar('Fred Astaire')
    print('\n-- Most similar score --\n')

    for word, score in similarities:
        print(word, score)
    
    return

def actorKnownForMovies(csvDataList):
    print('[--] Running actor list')
    # Get the data form dataset and make dict of actor and known in movies
    ActorsMovieIDs = csvDataList[0][['primaryName', 'knownForTitles']]
    ActorsMovieIDsList = list(zip(ActorsMovieIDs.primaryName, ActorsMovieIDs.knownForTitles))
    return ActorsMovieIDsList

def movieTitlesAndIDs(csvDataList): 
    print('[--] Running movie dict')   
    start = time.time()
    # Get the data form dataset and make tuples of movies and their dataset ID
    #movieNamesWithID = csvDataList[1][['tconst','primaryTitle']].apply(tuple, axis=1)
    moviesTitleIDs = csvDataList[1][['tconst','primaryTitle']]
    movieTitleIDsDict = dict(zip(moviesTitleIDs.tconst, moviesTitleIDs.primaryTitle)) # {movieName : ttID} 
    end = time.time()
    print('     ..Total time (s) for dict creation = ' + str(end-start) + '\n')
    return movieTitleIDsDict


def dataManipulation(ActorsMovieIDsList, movieTitleIDsDict):
    print('[-] Smashing numbers.. please hold...')
    start = time.time()
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
                placeHolderString += movieTitleIDsDict[tID]
            except KeyError:
                continue

            if tID != countList[len(countList)-1]:
                placeHolderString += ', '
        

        finalList.append(placeHolderString)
    
    #print(finalList)

    end = time.time()
    print('     ..Total time (s) for data manipulation= ' + str(end-start) + '\n')
    #print(ActorsMovieIDsList)
    #writeToFile('finalList.txt', finalList)
    return finalList

def writeToFile(name, data):
    print('[++] Backing up data manipulation to '+ name)
    with open(name, 'w') as f:
        for item in data:
            f.write("%s\n" % item)
    print('     ..Done backing up \n')

def main():
    print('[+] Running script... please hold your orgasm \n')
    dataset = readFiles(csvDataList)
    knownForTupleList = actorKnownForMovies(dataset)
    movieTitlesInDict = movieTitlesAndIDs(dataset)
    theList = dataManipulation(knownForTupleList, movieTitlesInDict)
    Word2VecAndTrainModel(theList, dataset)

    return 0

if __name__ == "__main__":
    main()