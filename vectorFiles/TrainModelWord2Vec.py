from gensim.models import Word2Vec
import time

def trainModel(sent):

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