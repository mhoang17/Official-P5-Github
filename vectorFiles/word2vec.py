from gensim.models import Word2Vec, KeyedVectors
import pandas as pd
from nltk.tokenize import word_tokenize

df = pd.read_csv('csvFiles\wiki_movie_plots_deduped.csv')

movies = df['Plot'].values

moviesVec = [word_tokenize(synopsis) for synopsis in movies[:3000]]

model = Word2Vec(moviesVec, min_count=1, size=100)

while True:
    sentence = input("Enter your search...\n")
    print(model.wv.most_similar(sentence))
