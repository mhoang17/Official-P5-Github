import glob, os, time
import pandas as pd

csvDict = {}

def readFiles(path):
    all_files = glob.glob(path)
    csvDataDict = {}
    countOf = 1

    print('[+] Runing files ')
    startFile = time.time()  
    
    for filename in all_files:
        print('    ..' + filename +' - '+ str(countOf) +' of '+ str(len(all_files)))
        GetOnlyFileName = os.path.basename(filename)
        OnlyFileName = GetOnlyFileName.replace('.csv','')
        df = pd.read_csv(filename, header=0, low_memory=False, encoding='ISO-8859-1' )
        csvDataDict[OnlyFileName] = df
        countOf += 1
    endFile = time.time()
    csvDict = csvDataDict
    print('    ... Total time reading files (s) = ' + str(endFile-startFile) + '\n')
    return csvDataDict

    