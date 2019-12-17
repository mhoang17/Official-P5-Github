from gensim.models import Word2Vec
import time


def train_model(sent):
    print('[+] Training the model')
    start_training = time.time()

    # Train the model with the given(sent) text corpus
    model = Word2Vec(sent, min_count=1, size=100, workers=4, window=7, sg=1)

    end_training = time.time()
    print('     ..Total time (s) for preparing data = ' + str(end_training - start_training))

    # Save the model after training
    saved_model = model.save("PrefaceOutput/word2vec.model")

    return saved_model
