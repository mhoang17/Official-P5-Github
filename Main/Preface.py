from KnowledgeGraph import KnowledgeGraphLoader
from utils import MovieList
from vectorFiles import PrepareData
import LoadFiles


def run_preface():
    csv_data_dict = LoadFiles.read_files('csvFiles/*.csv')

    print('[+] Running Movie list')
    MovieList.run_movie_list(csv_data_dict)
    print('     ..Done with Movie list\n')

    print('[+] Running knowledge graph')
    KnowledgeGraphLoader.run_kgl(csv_data_dict)
    print('     ..Done with knowledge graph\n')

    print('\n[+] Running model')
    PrepareData.run_model(csv_data_dict)
    print('     ..Done with model')


run_preface()
