# Official-P5-Github
GUIDE TO SETTING UP THE SEARCH ENGINE

	1.	Create a directory called csvFiles
	2.	Download the IMDb subdatasets from https://datasets.imdbws.com:
    ⁃	title.principals.tsv.gz (rename to principals.csv when unzipped)
    ⁃	title.basics.tsv.gz (rename to titles.csv when unzipped)
    ⁃	name.basics.tsv.gz (rename to names.csv when unzipped)
	3.	Put the downloaded files into the csvFiles directory
	4.	Run Preface.py from the Main directory.
	5.	After this is done, you should be able to run the UserSearch.py file in order to write a search query
    ⁃	In file QueryAnalysis.py you should comment in line 48 in order to write the queries:
    ⁃	movie with [name]
    ⁃	movie directed by [name]
    ⁃	movie written by [name]
    ⁃	actor who worked with [name]
    ⁃	If line 48 is not commented in, you can write:
    ⁃	what movie did [name] star in?
