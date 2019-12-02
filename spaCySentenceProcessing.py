import spacy
from spacy.matcher.matcher import Matcher
import PredicatesEnum as pe
import shlex

keywords = []

nlp = spacy.load("en_core_web_sm")

# Raw input string
str = "movie directed by Steven Spielberg and with Tom Hanks"

# Split the string in quotation from the rest of the string
str_split = shlex.split(str, posix=True)

# Create string which we analyse the word classes and which word should be converted into one
# ('worked' 'with' becomes 'worked with')
new_string = ""

# Dictionary over all positions of words in raw strings
position = {}

# If the element contains a quotation mark then it should not be a part of the new string
for element in str_split:
    if "'" not in element:
        new_string += element + " "

    # Add to dictionary
    position[str_split.index(element)] = element

doc = nlp(new_string)
matcher = Matcher(nlp.vocab)

triples = []

def extract_triple(nlp_doc):
    pattern = [{'POS': 'NOUN'}]
    pattern4 = [{'POS': 'ADP'}]
    pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    pattern3 = [{'POS': 'VERB'}]
    pattern5 = [{'POS': 'CCONJ'}]
    matcher.add('TRIPLE', None, pattern)
    matcher.add('TRIPLE', None, pattern2)
    matcher.add('TRIPLE', None, pattern3)
    matcher.add('TRIPLE', None, pattern4)
    matcher.add('TRIPLE', None, pattern5)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        triples.append(span.text)
    return triples

extract_triple(doc)

# We need a copy of the triples list, in order to pop words from the list while looping over it
searchWords = list(triples)

for i in range(len(triples) - 1):

    # Tokenizes element i in triples
    word1 = nlp(triples[i])
    word2 = nlp(triples[i + 1])

    # Find the part of speech of the element
    tag1 = [token.pos_ for token in word1]
    tag2 = [token.pos_ for token in word2]

    # If the current element is a verb and the following verb is a adp (eg. in or with) then we merge them into one
    if tag1[0] == 'VERB' and tag2[0] == 'ADP':
        con = triples[i] + " " + triples[i+1]
        searchWords[i] = con
        searchWords.pop(i + 1)

# We want to merge the words in quotation with the newly found words
new_search_words = []
i = 0
for element in position:
    # If the element contains quotation marks then add it to the new list
    if "'" in position[element]:
        new_search_words.append(position[element])

    elif i != len(searchWords):
        # if the element has is contained in the previously found, then add it to the new list
        if position[element] in searchWords[i]:
            new_search_words.append(searchWords[i])
            i += 1

# Translate words into predicates
for i in range(len(new_search_words)):
    element = new_search_words[i]
    if "with" in element:
        if "worked" in element:
            new_search_words[i] = ["starred_in", "has_actor"]
        else:
            new_search_words[i] = ["starred_in"]
    elif "starred" in element or "played" in element:
        new_search_words[i] = ["starred_in"]
    elif "made" in element or "directed" in element:
        new_search_words[i] = ["directed"]
    elif "written" in element:
        new_search_words[i] = ["has_written"]


# Reverse the list so we can correctly bind words
new_search_words.reverse()

# Subject, predicate, object list
spo = []


for i in range(len(new_search_words)):
    element_list = new_search_words[i]
    # We will only append things that have pairs. So if we find a predicate, then it will not be looked at because
    # a valid entry has to start with a word (eg. Spielberg)
    if type(element_list) is not list and element_list != 'and':
        # Now we want to find the predicates
        for j in range(i, len(new_search_words)):
            # If the type of the element is list then it means it is a collection of predicates
            if type(new_search_words[j]) is list:
                element = [element_list, new_search_words[j]]
                spo.append(element)
                break

print(spo)
