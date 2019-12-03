import sys
sys.path.insert(0, '/home/plebsbench/Documents/P5_Project/P5GitHub/Official-P5-Github')
import numpy as np
from gensim.models import Word2Vec
from PredicatesEnum import PredicatesEnum as PreEnum

def most_relevant_path(paths, question, model):
    # Array of the values of relevance will be stored here
    relatedness = []

    # For each path we have to measure their relevance and put it in the array of relevance values
    for path in paths:
        relatedness.append(relevance(path, question,model))

    # Find the highest relevance value and find the index of it
    max_element = max(relatedness)
    max_elem_id = relatedness.index(max_element)

    # Return the path with the highest relevance
    return paths[max_elem_id]


def relevance(path, question,model):
    sum_results = 0

    token_list = question.split(" ")

    # For each label in the path, sum their relevance to all words in the question.
    for label in path:
        if label not in PreEnum._value2member_map_:
            sum_results += relevance_part(label, token_list, model)

    # Return the mean value of the relevance
    return (1 / len(path)) * sum_results


def relevance_part(label, question, model):
    
    similarities = [0]
    
    for token in question:
        try:
            #testMe = model.wv.similarity(label, token)
            similarities.append(model.wv.similarity(label, token))

            #print('Token: '+ token + ' Label: '+ label)
            #print('\n')
        except KeyError:
            continue
        # for similarityValue in testMe.values():
        print(similarities)
        # Word2Vec function here
        # Add value to similarities array

    # Return the highest value of the similarities (eg. Jumanji will be very similar in a search with Dwayne Johnson,
    # but maybe not as high for another actor but will still have a similarity value)
    return max(similarities)

model = Word2Vec.load('PrefaceOutput/word2vec.model')
question1 = "actor who worked with Kevin Hart"
paths1 = [['Kevin Hart', 'starred_in', 'paper soldiers', 'has_actor', 'Beanie Sigel'], ['Kevin Hart', 'starred_in', 'soul plane', 'has_actor', 'Tom Arnold'], ['Kevin Hart', 'starred_in', 'soul plane', 'has_actor', 'Snoop Dogg'], ['Kevin Hart', 'starred_in', 'soul plane', 'has_actor', 'Dwayne Adway'], ['Kevin Hart', 'starred_in', 'not easily broken', 'has_actor', 'Maeve Quinlan'], ['Kevin Hart', 'starred_in', 'not easily broken', 'has_actor', 'Taraji P. Henson'], ['Kevin Hart', 'starred_in', 'not easily broken', 'has_actor', 'Morris Chestnut'], ['Kevin Hart', 'starred_in', 'the wedding ringer', 'has_actor', 'affion crockett'], ['Kevin Hart', 'starred_in', 'the wedding ringer', 'has_actor', 'kaley cuoco'], ['Kevin Hart', 'starred_in', 'the wedding ringer', 'has_actor', 'josh gad'], ['Kevin Hart', 'starred_in', 'something like a business', 'has_actor', 'donnell rawlings'], ['Kevin Hart', 'starred_in', 'something like a business', 'has_actor', 'jennifer titus'], ['Kevin Hart', 'starred_in', 'something like a business', 'has_actor', 'clifton powell'], ['Kevin Hart', 'starred_in', 'ride along', 'has_actor', 'john leguizamo'], ['Kevin Hart', 'starred_in', 'ride along', 'has_actor', 'tika sumpter'], ['Kevin Hart', 'starred_in', 'ride along', 'has_actor', 'ice cube'], ['Kevin Hart', 'starred_in', 'central intelligence', 'has_actor', 'amy ryan'], ['Kevin Hart', 'starred_in', 'central intelligence', 'has_actor', 'danielle nicolet'], ['Kevin Hart', 'starred_in', 'central intelligence', 'has_actor', 'dwayne johnson'], ['Kevin Hart', 'starred_in', 'think like a man', 'has_actor', 'michael ealy'], ['Kevin Hart', 'starred_in', 'think like a man', 'has_actor', 'gabrielle union'], ['Kevin Hart', 'starred_in', 'think like a man', 'has_actor', 'chris brown'], ['Kevin Hart', 'starred_in', '35 and ticking', 'has_actor', 'keith robinson'], ['Kevin Hart', 'starred_in', '35 and ticking', 'has_actor', 'nicole ari parker'], ['Kevin Hart', 'starred_in', '35 and ticking', 'has_actor', 'tamala jones'], ['Kevin Hart', 'starred_in', 'let go', 'has_actor', 'edward asner'], ['Kevin Hart', 'starred_in', 'let go', 'has_actor', 'gillian jacobs'], ['Kevin Hart', 'starred_in', 'let go', 'has_actor', 'david denman'], ['Kevin Hart', 'starred_in', 'about last night', 'has_actor', 'joy bryant'], ['Kevin Hart', 'starred_in', 'about last night', 'has_actor', 'regina hall'], ['Kevin Hart', 'starred_in', 'the upside', 'has_actor', 'aja naomi king'], ['Kevin Hart', 'starred_in', 'the upside', 'has_actor', 'nicole kidman'], ['Kevin Hart', 'starred_in', 'the upside', 'has_actor', 'bryan cranston'], ['Kevin Hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'nick kroll'], ['Kevin Hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'ed helms'], ['Kevin Hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'thomas middleditch'], ['Kevin Hart', 'starred_in', '9mm', 'has_actor', 'queen latifah'], ['Kevin Hart', 'starred_in', 'think like a man too', 'has_actor', 'la la anthony'], ['Kevin Hart', 'starred_in', 'think like a man too', 'has_actor', 'wendi mclendon-covey'], ['Kevin Hart', 'starred_in', 'jumanji: welcome to the jungle', 'has_actor', 'jack black'], ['Kevin Hart', 'starred_in', 'jumanji: welcome to the jungle', 'has_actor', 'karen gillan'], ['Kevin Hart', 'starred_in', 'get hard', 'has_actor', 't.i.'], ['Kevin Hart', 'starred_in', 'get hard', 'has_actor', 'alison brie'], ['Kevin Hart', 'starred_in', 'get hard', 'has_actor', 'will ferrell'], ['Kevin Hart', 'starred_in', 'the secret life of pets', 'has_actor', 'lake bell'], ['Kevin Hart', 'starred_in', 'the secret life of pets', 'has_actor', 'eric stonestreet'], ['Kevin Hart', 'starred_in', 'the secret life of pets', 'has_actor', 'louis c.k.'], ['Kevin Hart', 'starred_in', 'top five', 'has_actor', 'rosario dawson'], ['Kevin Hart', 'starred_in', 'top five', 'has_actor', 'chris rock'], ['Kevin Hart', 'starred_in', 'ride along 2', 'has_actor', 'benjamin bratt'], ['Kevin Hart', 'starred_in', 'fatherhood', 'has_actor', 'paul reiser'], ['Kevin Hart', 'starred_in', 'fatherhood', 'has_actor', 'alfre woodard'], ['Kevin Hart', 'starred_in', 'fatherhood', 'has_actor', 'anthony carrigan'], ['Kevin Hart', 'starred_in', 'the secret life of pets 2', 'has_actor', 'harrison ford'], ['Kevin Hart', 'starred_in', 'the secret life of pets 2', 'has_actor', 'patton oswalt'], ['Kevin Hart', 'starred_in', 'night school', 'has_actor', 'romany malco'], ['Kevin Hart', 'starred_in', 'night school', 'has_actor', 'rob riggle'], ['Kevin Hart', 'starred_in', 'night school', 'has_actor', 'tiffany haddish'], ['Kevin Hart', 'starred_in', 'the great outdoors', 'has_actor', 'tristan cantave'], ['Kevin Hart', 'starred_in', 'the great outdoors', 'has_actor', 'teena lewis'], ['Kevin Hart', 'starred_in', 'jumanji: the next level', 'has_actor', 'awkwafina'], ['Kevin Hart', 'starred_in', 'lone wolf', 'has_actor', 'ann douglas'], ['Kevin Hart', 'starred_in', 'lone wolf', 'has_actor', 'jamie newcomb'], ['Kevin Hart', 'starred_in', 'lone wolf', 'has_actor', 'dyann brown'], ['Kevin Hart', 'starred_in', 'mindkiller', 'has_actor', 'shirley ross'], ['Kevin Hart', 'starred_in', 'mindkiller', 'has_actor', 'wade kelley'], ['Kevin Hart', 'starred_in', 'mindkiller', 'has_actor', 'joe mcdonald'], ['Kevin Hart', 'starred_in', 'conviction', 'has_actor', 'catharine e. jones'], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', 'denise emilia sandulescu'], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', 'joe elliott'], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', 'jerry hayes'], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', 'george avgoustis'], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', "ashley-rene' everest"], ['Kevin Hartzman', 'starred_in', 'getting out', 'has_actor', 'michael j. renda'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'justin serino'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'mo el-zaatari'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'donna barbera'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'carter burch'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'keyna reynolds'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'michael j. mowery'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'kali rima mcgurk'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'Scott Tuke'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'Peggy Ann Lloyd'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'Juniper Purinton'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'Jeff Nicholson']]
a = most_relevant_path(paths1, question1, model)
print(a[len(a)-1])
