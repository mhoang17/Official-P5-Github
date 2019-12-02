import numpy as np
from PredicatesEnum import PredicatesEnum as PreEnum


def most_relevant_path(paths, question):
    # Array of the values of relevance will be stored here
    relatedness = []

    # For each path we have to measure their relevance and put it in the array of relevance values
    for path in paths:
        relatedness.append(relevance(path, question))

    # Find the highest relevance value and find the index of it
    max_element = max(relatedness)
    max_elem_id = relatedness.index(max_element)

    # Return the path with the highest relevance
    return paths[max_elem_id]


def relevance(path, question):
    sum_results = 0

    token_list = question.split(" ")

    # For each label in the path, sum their relevance to all words in the question.
    for label in path:
        if label not in PreEnum.value2member_map_:
            sum_results += relevance_part(label, token_list)

    # Return the mean value of the relevance
    return (1 / len(path)) * sum_results


def relevance_part(label, question):
    similarities = [0]
    i = 1
    for token in question:
        similarities.append(i)
        i += 1
        # Word2Vec function here
        # Add value to similarities array

    # Return the highest value of the similarities (eg. Jumanji will be very similar in a search with Dwayne Johnson,
    # but maybe not as high for another actor but will still have a similarity value)
    return max(similarities)


question1 = "actor who worked with Kevin Hart"
paths1 = [['kevin hart', 'starred_in', 'paper soldiers', 'has_actor', 'beanie sigel'], ['kevin hart', 'starred_in', 'soul plane', 'has_actor', 'tom arnold'], ['kevin hart', 'starred_in', 'soul plane', 'has_actor', 'snoop dogg'], ['kevin hart', 'starred_in', 'soul plane', 'has_actor', 'dwayne adway'], ['kevin hart', 'starred_in', 'not easily broken', 'has_actor', 'maeve quinlan'], ['kevin hart', 'starred_in', 'not easily broken', 'has_actor', 'taraji p. henson'], ['kevin hart', 'starred_in', 'not easily broken', 'has_actor', 'morris chestnut'], ['kevin hart', 'starred_in', 'the wedding ringer', 'has_actor', 'affion crockett'], ['kevin hart', 'starred_in', 'the wedding ringer', 'has_actor', 'kaley cuoco'], ['kevin hart', 'starred_in', 'the wedding ringer', 'has_actor', 'josh gad'], ['kevin hart', 'starred_in', 'something like a business', 'has_actor', 'donnell rawlings'], ['kevin hart', 'starred_in', 'something like a business', 'has_actor', 'jennifer titus'], ['kevin hart', 'starred_in', 'something like a business', 'has_actor', 'clifton powell'], ['kevin hart', 'starred_in', 'ride along', 'has_actor', 'john leguizamo'], ['kevin hart', 'starred_in', 'ride along', 'has_actor', 'tika sumpter'], ['kevin hart', 'starred_in', 'ride along', 'has_actor', 'ice cube'], ['kevin hart', 'starred_in', 'central intelligence', 'has_actor', 'amy ryan'], ['kevin hart', 'starred_in', 'central intelligence', 'has_actor', 'danielle nicolet'], ['kevin hart', 'starred_in', 'central intelligence', 'has_actor', 'dwayne johnson'], ['kevin hart', 'starred_in', 'think like a man', 'has_actor', 'michael ealy'], ['kevin hart', 'starred_in', 'think like a man', 'has_actor', 'gabrielle union'], ['kevin hart', 'starred_in', 'think like a man', 'has_actor', 'chris brown'], ['kevin hart', 'starred_in', '35 and ticking', 'has_actor', 'keith robinson'], ['kevin hart', 'starred_in', '35 and ticking', 'has_actor', 'nicole ari parker'], ['kevin hart', 'starred_in', '35 and ticking', 'has_actor', 'tamala jones'], ['kevin hart', 'starred_in', 'let go', 'has_actor', 'edward asner'], ['kevin hart', 'starred_in', 'let go', 'has_actor', 'gillian jacobs'], ['kevin hart', 'starred_in', 'let go', 'has_actor', 'david denman'], ['kevin hart', 'starred_in', 'about last night', 'has_actor', 'joy bryant'], ['kevin hart', 'starred_in', 'about last night', 'has_actor', 'regina hall'], ['kevin hart', 'starred_in', 'the upside', 'has_actor', 'aja naomi king'], ['kevin hart', 'starred_in', 'the upside', 'has_actor', 'nicole kidman'], ['kevin hart', 'starred_in', 'the upside', 'has_actor', 'bryan cranston'], ['kevin hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'nick kroll'], ['kevin hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'ed helms'], ['kevin hart', 'starred_in', 'captain underpants: the first epic movie', 'has_actor', 'thomas middleditch'], ['kevin hart', 'starred_in', '9mm', 'has_actor', 'queen latifah'], ['kevin hart', 'starred_in', 'think like a man too', 'has_actor', 'la la anthony'], ['kevin hart', 'starred_in', 'think like a man too', 'has_actor', 'wendi mclendon-covey'], ['kevin hart', 'starred_in', 'jumanji: welcome to the jungle', 'has_actor', 'jack black'], ['kevin hart', 'starred_in', 'jumanji: welcome to the jungle', 'has_actor', 'karen gillan'], ['kevin hart', 'starred_in', 'get hard', 'has_actor', 't.i.'], ['kevin hart', 'starred_in', 'get hard', 'has_actor', 'alison brie'], ['kevin hart', 'starred_in', 'get hard', 'has_actor', 'will ferrell'], ['kevin hart', 'starred_in', 'the secret life of pets', 'has_actor', 'lake bell'], ['kevin hart', 'starred_in', 'the secret life of pets', 'has_actor', 'eric stonestreet'], ['kevin hart', 'starred_in', 'the secret life of pets', 'has_actor', 'louis c.k.'], ['kevin hart', 'starred_in', 'top five', 'has_actor', 'rosario dawson'], ['kevin hart', 'starred_in', 'top five', 'has_actor', 'chris rock'], ['kevin hart', 'starred_in', 'ride along 2', 'has_actor', 'benjamin bratt'], ['kevin hart', 'starred_in', 'fatherhood', 'has_actor', 'paul reiser'], ['kevin hart', 'starred_in', 'fatherhood', 'has_actor', 'alfre woodard'], ['kevin hart', 'starred_in', 'fatherhood', 'has_actor', 'anthony carrigan'], ['kevin hart', 'starred_in', 'the secret life of pets 2', 'has_actor', 'harrison ford'], ['kevin hart', 'starred_in', 'the secret life of pets 2', 'has_actor', 'patton oswalt'], ['kevin hart', 'starred_in', 'night school', 'has_actor', 'romany malco'], ['kevin hart', 'starred_in', 'night school', 'has_actor', 'rob riggle'], ['kevin hart', 'starred_in', 'night school', 'has_actor', 'tiffany haddish'], ['kevin hart', 'starred_in', 'the great outdoors', 'has_actor', 'tristan cantave'], ['kevin hart', 'starred_in', 'the great outdoors', 'has_actor', 'teena lewis'], ['kevin hart', 'starred_in', 'jumanji: the next level', 'has_actor', 'awkwafina'], ['kevin hart', 'starred_in', 'lone wolf', 'has_actor', 'ann douglas'], ['kevin hart', 'starred_in', 'lone wolf', 'has_actor', 'jamie newcomb'], ['kevin hart', 'starred_in', 'lone wolf', 'has_actor', 'dyann brown'], ['kevin hart', 'starred_in', 'mindkiller', 'has_actor', 'shirley ross'], ['kevin hart', 'starred_in', 'mindkiller', 'has_actor', 'wade kelley'], ['kevin hart', 'starred_in', 'mindkiller', 'has_actor', 'joe mcdonald'], ['kevin hart', 'starred_in', 'conviction', 'has_actor', 'catharine e. jones'], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', 'denise emilia sandulescu'], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', 'joe elliott'], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', 'jerry hayes'], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', 'george avgoustis'], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', "ashley-rene' everest"], ['kevin hartzman', 'starred_in', 'getting out', 'has_actor', 'michael j. renda'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'justin serino'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'mo el-zaatari'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'donna barbera'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'carter burch'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'keyna reynolds'], ['kevin hartzman', 'starred_in', 'desperate cowboys', 'has_actor', 'michael j. mowery'], ['kevin hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'kali rima mcgurk'], ['kevin hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'scott tuke'], ['kevin hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'peggy ann lloyd'], ['kevin hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'juniper purinton'], ['kevin hart', 'starred_in', 'the man who spoke to himself', 'has_actor', 'jeff nicholson']]
a = most_relevant_path(paths1, question1)
print(a[len(a)-1])
