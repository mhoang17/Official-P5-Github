from gensim.models import Word2Vec
import time


def train_model(sent):
    print('[+] Training the model')
    start_training = time.time()

    model = Word2Vec(sent, min_count=1, size=100, workers=4, window=7, sg=1)

    end_training = time.time()
    print('     ..Total time (s) for preparing data = ' + str(end_training - start_training))

    # similarities = model.wv.most_similar('Fred Astaire')

    saved_model = model.save("PrefaceOutput/word2vec.model")

    # print(model11.wv.most_similar(["actor", "Fred Astaire"], topn=11, indexer=None))
    return saved_model