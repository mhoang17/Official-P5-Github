import nltk
from nltk.corpus import stopwords
import shlex

# Stop words from the English dictionary
stop_words = set(stopwords.words('english'))

# '' notation for non-separable words
sentence = input("Enter your search...\n")
sentence_arr = shlex.split(sentence, posix=False)
tag_arr = []

# If the element has a ' in it, it means that it should automatically be seen as a keyword
for i in range(len(sentence_arr)):
    if "'" not in sentence_arr[i]:
        tag = nltk.word_tokenize(sentence_arr[i])
        tag_arr.append(nltk.pos_tag(tag))
    else:
        tag_arr.append(sentence_arr[i])

print("Tagged sentence: ", tag_arr)
