import glob
import pandas as pd
import time

#Load csv file from path and return a list
def loadFiles():
    startPreData = time.time()
    csvDataDict = []

    pd.set_option('display.max_rows', 50)

    path = r'C:\Users\janta\Desktop\AAU\Datalogi 5. semester\Projekt\csvFiles'  # use your path
    all_files = glob.glob(path + "/*.csv")

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, low_memory=False, encoding='ISO-8859-1')
        print(filename)
        csvDataDict.append(df)

    endPredata = time.time()
    print('     ..Total time (s) for preparing data = ' + str(endPredata - startPreData) + '\n')
    return csvDataDict


#csvDataDict = Preface.csv_Data_Dict

#Takes 3 columns and return a list with only movies.
def createMovielist(csvDataDict):
    titleTypeList = []
    for item in csvDataDict.get('titles')['titleType'].iteritems():
        titleTypeList.append(item[1])
    tConstList = []
    for item in csvDataDict.get('titles')['tconst'].iteritems():
        tConstList.append(item[1])
    titleList = []
    for item in csvDataDict.get('titles')['primaryTitle'].iteritems():
        titleList.append(item[1])
    movieList = []
    #All the list are equal in length, and the elements fits together from the original list
    #so taking the same index in each list, and create an new list, then we are checking if
    #tilteType is movie, if true then we will append it to the movie list.
    for i in range(len(tConstList)):
        phList1 = [tConstList[i], titleTypeList[i], titleList[i]]
        if phList1[1] == "movie":
            movieList.append(phList1)
    return movieList


#movieList = createMovielist(csvDataDict)

#Writes to a file by giving the function the name for the file and the data
def write_To_File(name, data):
    with open(name, 'w') as f:
        for item in data:
            f.write('%s\n' % item)

def run_Movie_List(dataset):
    #csvDataDict = Preface.csv_Data_Dict
    movieList = createMovielist(dataset)
    #Calling the function and giving it the name.
    write_To_File('PrefaceOutput/movieList.txt', movieList)