#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def addToDict(x):
    return list(dict.fromkeys(x))

def loadFiles():
    csvDataList = []

    pd.set_option('display.max_rows', 50)

    path = r'/home/somepleb/Documents/P5_Project/imdb_dataset' # use your path
    all_files = glob.glob(path + "/*.csv")

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, low_memory=False )
        print(filename)
        csvDataList.append(df)
    
    return csvDataList

csvDataList = loadFiles()

def columnToList(data, clNr, clName):
    phList = []
    if(clName == 'primaryName' or clName == 'primaryTitle'):
        for x in data[clNr][[clName]].iteritems():
            for y in x[1]:
                for z in str(y).split(' '):
                    phList.append(z)
    elif(clName == 'titleType'):
         for i in data[clNr][[clName]].iteritems():
             for j in i[1]:
                 phList.append(j)
    elif(clName == 'genres'):
        for i in data[clNr][[clName]].iteritems():
             for j in i[1]:
                 for k in str(j).split(','):
                     phList.append(k)
    return phList

def completeWords():
    completeList = []

    completeList = columnToList(csvDataList, 1, 'primaryName' ) + columnToList(csvDataList, 2, 'primaryTitle' ) + columnToList(csvDataList, 2, 'titleType' ) + columnToList(csvDataList, 2, 'genres' )
    
    completeList = addToDict(completeList)

    return completeList

def writeToFile():
    with open('WordList.txt', 'w') as f:
        for item in completeWords():
            f.write('%s\n' % item)

writeToFile()