
# Takes 3 columns and return a list with only movies.
def create_movie_list(csv_data_dict):
    title_type_list = []
    for item in csv_data_dict.get('titles')['titleType'].iteritems():
        title_type_list.append(item[1])
    t_const_list = []
    for item in csv_data_dict.get('titles')['tconst'].iteritems():
        t_const_list.append(item[1])
    title_list = []
    for item in csv_data_dict.get('titles')['primaryTitle'].iteritems():
        title_list.append(item[1])
    movie_list = []
    # All the list are equal in length, and the elements fits together from the original list
    # so taking the same index in each list, and create an new list, then we are checking if
    # tilteType is movie, if true then we will append it to the movie list.
    for i in range(len(t_const_list)):
        ph_list1 = [t_const_list[i], title_type_list[i], title_list[i]]
        if ph_list1[1] == "movie":
            movie_list.append(ph_list1)
    return movie_list


# movieList = createMovielist(csvDataDict)

# Writes to a file by giving the function the name for the file and the data
def write_to_file(name, data):
    with open(name, 'w') as f:
        for item in data:
            f.write('%s\n' % item)


def run_movie_list(dataset):
    # csvDataDict = Preface.csv_Data_Dict
    movie_list = create_movie_list(dataset)
    # Calling the function and giving it the name.
    write_to_file('../PrefaceOutput/movie_list.txt', movie_list)
