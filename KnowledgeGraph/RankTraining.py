import numpy as np


def most_relevant_path(paths, question):
    # Array of the values of relevance will be stored here
    relatedness = []

    # For each path we have to measure their relevance and put it in the array of relevance values
    for path in paths:
        relatedness.append(relevance(path, question))

    # Find the highest relevance value and find the index of it
    max_element = max(relatedness)
    max_elem_id = np.where(relatedness == max_element)

    # Return the path with the highest relevance
    return paths[max_elem_id]


def relevance(path, question):
    sum_results = 0

    # For each label in the path, sum their relevance to all words in the question.
    for label in path:
        sum_results += relevance_part(label, question)

    # Return the mean value of the relevance
    return (1 / len(path)) * sum_results


def relevance_part(label, simple_question):
    similarities = []

    for token in simple_question:
        delete_this = 0
        # Word2Vec function here
        # Add value to similarities array

    # Return the highest value of the similarities (eg. Jumanji will be very similar in a search with Dwayne Johnson,
    # but maybe not as high for another actor but will still have a similarity value)
    return max(similarities)
