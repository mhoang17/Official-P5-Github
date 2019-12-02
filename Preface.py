import sys
sys.path.insert(0, '/home/plebsbench/Documents/P5_Project/P5GitHub/Official-P5-Github')
from KnowledgeGraph import KnowledgeGraphLoader
from utils import MovieList
from vectorFiles import PrepareData
import LoadFiles


def runPreface():

    csv_Data_Dict = LoadFiles.read_Files('csvFiles/*.csv')

    print('[+] Running knowlegde graph')
    KnowledgeGraphLoader.runKGL(csv_Data_Dict)
    print('     ..Done with knowlegde graph')
    
    print('\n[+] Running Movie list')
    MovieList.run_Movie_List(csv_Data_Dict)
    print('     ..Done with Movie list')
    
    print('[+] Running model')
    PrepareData.run_Model(csv_Data_Dict)
    print('     ..Done with model')

runPreface()