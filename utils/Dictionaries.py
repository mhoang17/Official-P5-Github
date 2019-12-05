import pandas as pd


def fetch_movie_list():
    with open('PrefaceOutput/movieList.txt', 'r') as f:
        main_list = [[line.replace('[', '').replace('\n', '').replace(']', '').replace('\'', '')] for line in f]

    tmp_frame = pd.DataFrame(main_list, columns=['All'])
    movie_frame = pd.DataFrame(tmp_frame.All.str.split(', ', 2).tolist(), columns=['tconst', 'kind', 'primaryTitle'])
    return movie_frame


def make_dict():
    names = pd.read_csv('csvFiles/names.csv', header=0, low_memory=False, encoding='utf-8')
    titles = pd.read_csv('csvFiles/titles.csv', header=0, low_memory=False, encoding='utf-8')
    dictionary = {}

    for i in range(len(names) - 1):
        dictionary[names['nconst'].values[i]] = names['primaryName'].values[i]

    for i in range(len(titles) - 1):
        dictionary[titles['tconst'].values[i]] = str(titles['primaryTitle'].values[i])

    return dictionary


def make_persons_dict():
    names_dict = {}
    names = pd.read_csv('csvFiles/names.csv', header=0, low_memory=False, encoding='utf-8')

    # Load all names into the names dictionary
    for i in range(len(names) - 1):
        names_dict[names['nconst'].values[i]] = names['primaryName'].values[i]

    return names_dict


def make_titles_dict():
    titles_dict = {}
    titles = fetch_movie_list()

    # Load all titles into the titles dictionary
    for i in range(len(titles) - 1):
        titles_dict[titles['tconst'].values[i]] = str(titles['primaryTitle'].values[i])

    return titles_dict
