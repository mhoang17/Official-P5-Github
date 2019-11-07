import tmdbsimple as tmdb

tmdb.API_KEY = 'a32e5d0ae63fd4f2dd3977596c27b6d7'

f = open('csvFiles\movieSynopsis.csv', 'w')
f.write('synopsis\n')

for i in range(1000):
    try:
        movie = tmdb.Movies(i)
        response = movie.info()
        f.write(response['overview'] + '\n')
    except:
        continue

f.close()
