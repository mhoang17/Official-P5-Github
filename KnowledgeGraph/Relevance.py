import numpy as np
from gensim.models import Word2Vec
from PredicatesEnum import PredicatesEnum as PreEnum


def best_results(relatedness, paths, output):

    # Find the most related item
    max_element = max(relatedness)
    max_elem_id = relatedness.index(max_element)

    # Append to output list
    output.append(paths[max_elem_id])

    # Pop elements out, so we don't pick them again
    relatedness.pop(max_elem_id)
    paths.pop(max_elem_id)


def most_relevant_path(paths, question, model):
    # Array of the values of relevance will be stored here
    relatedness = []
    new_list = []

    # For each path we have to measure their relevance and put it in the array of relevance values
    for path in paths:
        relatedness.append(relevance(path, question, model))

    # Find the highest relevance value and find the index of it
    if len(paths) >= 10:
        for x in range(10):
            best_results(relatedness, paths, new_list)

    else:
        for x in range(len(paths)):
            best_results(relatedness, paths, new_list)

    # Return the path with the highest relevance
    return new_list


def relevance(path, question, model):
    sum_results = 0

    question = question.split(" ")

    # For each label in the path, sum their relevance to all words in the question.
    for label in path:
        if label not in PreEnum._value2member_map_:
            sum_results += relevance_part(label, question, model)

    # Return the mean value of the relevance
    return (1 / len(path)) * sum_results


def relevance_part(label, question, model):
    similarities = []

    for token in question:
        try:
            similarities.append(model.wv.similarity(label, token))
        except KeyError:
            continue

    # If our list is empty, just append 0 to the list
    if not similarities:
        similarities.append(0)

    # Return the highest value of the similarities (eg. Jumanji will be very similar in a search with Dwayne Johnson,
    # but maybe not as high for another actor but will still have a similarity value)
    return max(similarities)

