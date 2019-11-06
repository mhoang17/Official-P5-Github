import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords
import shlex

# Stop words
stop_words = {"ourselves", "hers", "between", "yourself", "again", "there", "about", "once",
              "during", "out", "very", "having", "they", "own", "an", "be", "some", "for",
              "its", "yours", "such", "into", "most", "itself", "other", "off", "is", "s",
              "am", "who", "him", "each", "the", "until", "are", "we", "these", "your", "his",
              "through", "don", "me", "were", "her", "more", "this", "down", "should", "our",
              "their", "while", "up", "to", "ours", "had", "she", "no", "when", "at", "any",
              "them", "same", "been", "have", "will", "on", "does", "yourselves", "then", "that",
              "because", "what", "why", "so", "can", "did", "not", "now", "he", "you", "has",
              "just", "where", "too", "only", "myself", "which", "those", "i", "few", "whom",
              "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how",
              "further", "was", "here", "than"}


#adj1 = {word for word, pos in brown.tagged_words() if pos.startswith('JJ')}
#adj2 = {word for word, pos in brown.tagged_words() if pos.startswith('JJR')}
#adj3 = {word for word, pos in brown.tagged_words() if pos.startswith('JJS')}
#stop_words.update(adj1)
#stop_words.update(adj2)
#stop_words.update(adj3)


# '' notation for non-separable words
sentence = input("Enter your search...\n")
sentence_arr = shlex.split(sentence, posix=False)
tag_arr = []

# Tokenize the words
for i in range(len(sentence_arr)):
    # If the element has a ' in it, it means that it should automatically be seen as a keyword
    if "'" in sentence_arr[i] or "\"" in sentence_arr[i]:
        tag_arr.append(sentence_arr[i])

    #
    else:
        tag = nltk.word_tokenize(sentence_arr[i])
        filtered_text = [w for w in tag if not w in stop_words]

        if filtered_text:
            tag_arr.append(nltk.pos_tag(filtered_text))

print("Tagged sentence: ", tag_arr)
