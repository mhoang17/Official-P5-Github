import spacy

keywords = []

nlp = spacy.load("en_core_web_sm")
doc = nlp("movie with Jim Carrey and directed by Bill Gates")

# TODO: Maybe we should revise these keywords sometime
stop_words = ["ourselves", "hers", "between", "yourself", "again", "there", "about", "once",
              "during", "out", "very", "having", "they", "own", "an", "be", "some", "for",
              "its", "yours", "such", "into", "most", "itself", "other", "off", "is", "s",
              "am", "who", "him", "each", "the", "until", "are", "we", "these", "your", "his",
              "through", "don", "me", "were", "her", "more", "this", "down", "should", "our",
              "their", "while", "up", "to", "ours", "had", "she", "no", "when", "at", "any",
              "them", "same", "been", "have", "will", "on", "does", "yourselves", "then", "that",
              "because", "what", "why", "so", "can", "did", "not", "now", "he", "you", "has",
              "just", "where", "too", "only", "myself", "which", "those", "i", "few", "whom",
              "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how",
              "further", "was", "here", "than"]

# extract all tokens from doc and put them in a list called keywords
for token in doc:
    keywords.append(token)

# if a string in stop_words appear in the keywords list, it'll be removed from keywords
for x in stop_words:
    for y in keywords:
        if x == str(y):
            keywords.remove(y)

# reversing the order of words in the keywords list
keywords.reverse()
print(keywords)


