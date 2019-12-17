from KnowledgeGraph import KnowledgeGraphLoader
from utils import MovieList
from VectorFiles import PrepareData
import LoadFiles

# Sets up all the needed
def run_preface():
    # Load the files into RAM
    csv_data_dict = LoadFiles.read_files('csvFiles/*.csv')

    # Run the creation of Movie List with the IMDb dataset
    print('[+] Running Movie list')
    MovieList.run_movie_list(csv_data_dict)
    print('     ..Done with Movie list\n')

    # Run the creation of Knowledge graph with the IMDb dataset
    print('[+] Running knowledge graph')
    KnowledgeGraphLoader.run_kgl(csv_data_dict)
    print('     ..Done with knowledge graph\n')

    # Run the creation of Word2Vec model with the IMDb dataset
    print('\n[+] Running model')
    PrepareData.run_model(csv_data_dict)
    print('     ..Done with model')

# Run the run_preface function
run_preface()
