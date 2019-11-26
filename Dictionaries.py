import pandas as pd


def make_dict():
    names = pd.read_csv("csvFiles/names.csv", sep=',', nrows=4000000, low_memory=False)
    titles = pd.read_csv("csvFiles/titles.csv", sep='\t', low_memory=False, encoding="ISO-8859-1")
    dictionary = {}

    for i in range(len(names) - 1):
        dictionary[names['nconst'].values[i]] = names['primaryName'].values[i].lower()

    for i in range(len(titles) - 1):
        dictionary[titles['tconst'].values[i]] = titles['primaryTitle'].values[i].lower()

    return dictionary


def make_persons_dict():
    names_dict = {}
    names = pd.read_csv("../csvFiles/names.csv", sep=',', nrows=1000000, low_memory=False)

    # Load all names into the names dictionary
    for i in range(len(names) - 1):
        names_dict[names['nconst'].values[i]] = names['primaryName'].values[i].lower()

    return names_dict


def make_titles_dict():
    titles_dict = {}
    titles = pd.read_csv("../csvFiles/titles.csv", sep='\t', low_memory=False, encoding="ISO-8859-1")

    # Load all titles into the titles dictionary
    for i in range(len(titles) - 1):
        titles_dict[titles['tconst'].values[i]] = titles['primaryTitle'].values[i].lower()

    return titles_dict
