import spacy
from spacy.matcher.matcher import Matcher
from PredicatesEnum import PredicatesEnum as pe
import shlex

nlp = spacy.load("en_core_web_sm")


def query_processing(query):
    # Split the string in quotation from the rest of the string
    str_split = shlex.split(query, posix=True)

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

    # We analyse the query
    doc = nlp(new_string)

    # The pattern matcher
    matcher = Matcher(nlp.vocab)

    # We find the part of speech tags of the different words
    pos = extract_pos(matcher, doc)

    # Find words that should be seen together
    search_words = verb_adp(pos)

    # We re-merge the elements which are in quotation with the words we have found the tags of
    new_search_words = re_merge(position, search_words)

    # We find the proper predicates for a query
    predicates(new_search_words)

    # Comment this in to reverse the list so we can correctly bind things
    # new_search_words.reverse()

    query = result(new_search_words)

    return query


def extract_pos(matcher, nlp_doc):
    pos = []
    matcher.add('NOUN', None, [{'POS': 'NOUN'}])
    matcher.add('NAME', None, [{'POS': 'PROPN'}, {'POS': 'PROPN'}])
    matcher.add('VERB', None, [{'POS': 'VERB'}])
    matcher.add('ADP', None, [{'POS': 'ADP'}])
    matcher.add('CCONJ', None, [{'POS': 'CCONJ'}])
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        pos.append(span.text)
    return pos


def verb_adp(triples):
    # We need a copy of the triples list, in order to pop words from the list while looping over it
    search_words = list(triples)

    for i in range(len(triples) - 1):

        # Tokenizes element i in triples
        word1 = nlp(triples[i])
        word2 = nlp(triples[i + 1])

        # Find the part of speech of the element
        tag1 = [token.pos_ for token in word1]
        tag2 = [token.pos_ for token in word2]

        # If the current element is a verb and the following verb is a adp (eg. in or with) then we merge them into one
        if tag1[0] == 'VERB' and tag2[0] == 'ADP':
            con = triples[i] + " " + triples[i + 1]
            search_words[i] = con
            search_words.pop(i + 1)

    return search_words


def re_merge(position, searchWords):
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

    return new_search_words


def predicates(new_search_words):
    # Translate words into predicates
    for i in range(len(new_search_words)):
        element = new_search_words[i]
        if "with" in element:
            if "worked" in element:
                new_search_words[i] = [pe.STARRED_IN.value, pe.HAS_ACTOR.value]
            else:
                new_search_words[i] = [pe.STARRED_IN.value]
        elif "star" in element or "appear" in element or "act" in element :
            new_search_words[i] = [pe.STARRED_IN.value]
        elif "made" in element or "directed" in element:
            new_search_words[i] = [pe.DIRECTED.value]
        elif "written" in element:
            new_search_words[i] = [pe.WROTE.value]


def result(new_search_words):
    # Subject, predicate, object list
    spo = []

    for i in range(len(new_search_words)):
        element_list = new_search_words[i]
        # We will only append things that have pairs. So if we find a predicate, then it will not be looked at because
        # a valid entry has to start with a word (eg. Spielberg)
        if type(element_list) is not list and element_list != 'and' and "movie" not in element_list and "film" not in element_list:
            # Now we want to find the predicates
            for j in range(i, len(new_search_words)):
                # If the type of the element is list then it means it is a collection of predicates
                if type(new_search_words[j]) is list:
                    element = [element_list, new_search_words[j]]
                    spo.append(element)
                    break

    return spo
