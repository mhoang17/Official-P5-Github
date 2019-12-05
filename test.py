from KnowledgeGraph import PathProcessing


def seperate_all_paths(predicates, sec_all_paths, names):
    paths_list = []
    predicate = predicates[0]
    idx = 1

    # TODO: make it so that it will only do this if the entry is like mentioned before
    for elements in sec_all_paths:

        # This is only important if there are more entities and we therefore need to switch between predicate lists
        if len(predicates) > 1:
            # This is a fail safe measure so we don't get a out of bounds exception
            if idx < len(predicates) and idx < len(names):
                # If the next element is the name of the next entity, we need to switch to the predicate list
                # that belongs to that specific entity
                if names[idx] in elements[len(elements) - 1]:
                    predicate = predicates[idx]
                    idx += 1

        if len(elements) > 3:
            # We reverse the list because it is easier to go backwards, because the end node will only occur once.
            elements.reverse()

            # Here we store the path
            path = []

            # This will be important if we have found a part of the part and need the next predicate to know which
            # path we now need to take
            k = len(predicate) - 1

            # We have two for loops that kinda goes through the same. The outer goes through the whole list
            # While the other loop only loops from where the outer loop has reached to the end.
            # This is to find the remaining path which will always lie from l to len(elements)
            for l in range(len(elements)):
                # If we have found the correct predicate, then we know we have found the end of a path.
                if elements[l] == predicate[k]:
                    for j in range(l, len(elements)):
                        if elements[j] == predicate[k]:
                            # The entity which the edge goes into will always lie in the index before the index
                            # where the predicate lies
                            path.append(elements[j - 1])
                            path.append(elements[j])

                            # We will now move on to the next predicate
                            k -= 1

                        # If we have reached the end, then we know the path is done
                        elif j == len(elements) - 1:
                            path.append(elements[j])

                            # Reset k to the length of the current predicate list
                            k = len(predicate) - 1

                # If we found a path then we will add it
                if path:
                    # Reverse it so it will be in the correct order
                    path.reverse()
                    paths_list.append(path)

                    # Reset path
                    path = []
        else:
            paths_list.append(elements)
    return paths_list


list1 = [['steven spielberg', 'directed', 'firelight'], ['steven spielberg', 'directed', 'the sugarland express'], ['steven spielberg', 'directed', 'jaws'], ['steven spielberg', 'directed', 'close encounters of the third kind'], ['steven spielberg', 'directed', '1941'], ['steven spielberg', 'directed', 'raiders of the lost ark'], ['steven spielberg', 'directed', 'e.t. the extra-terrestrial'], ['steven spielberg', 'directed', 'twilight zone: the movie'], ['steven spielberg', 'directed', 'indiana jones and the temple of doom'], ['steven spielberg', 'directed', 'the color purple'], ['steven spielberg', 'directed', 'empire of the sun'], ['steven spielberg', 'directed', 'always'], ['steven spielberg', 'directed', 'indiana jones and the last crusade'], ['steven spielberg', 'directed', 'hook'], ['steven spielberg', 'directed', 'jurassic park'], ['steven spielberg', 'directed', "schindler's list"], ['steven spielberg', 'directed', 'amistad'], ['steven spielberg', 'directed', 'the lost world: jurassic park'], ['steven spielberg', 'directed', 'saving private ryan'], ['steven spielberg', 'directed', 'minority report'], ['steven spielberg', 'directed', 'a.i. artificial intelligence'], ['steven spielberg', 'directed', 'catch me if you can'], ['steven spielberg', 'directed', 'the terminal'], ['steven spielberg', 'directed', 'indiana jones and the kingdom of the crystal skull'], ['steven spielberg', 'directed', 'war of the worlds'], ['steven spielberg', 'directed', 'munich'], ['steven spielberg', 'directed', 'lincoln'], ['steven spielberg', 'directed', 'the adventures of tintin'], ['steven spielberg', 'directed', 'untitled indiana jones project'], ['steven spielberg', 'directed', 'war horse'], ['steven spielberg', 'directed', 'untitled george gershwin project'], ['steven spielberg', 'directed', 'ready player one'], ['steven spielberg', 'directed', 'west side story'], ['steven spielberg', 'directed', 'the kidnapping of edgardo mortara'], ['steven spielberg', 'directed', 'bridge of spies'], ['steven spielberg', 'directed', 'the bfg'], ['steven spielberg', 'directed', 'the post'], ['steven spielberg', 'directed', 'blackhawk'], ['steven spielberg', 'directed', 'untitled ulysses s. grant project'], ['tom hanks', 'starred_in', 'bachelor party'], ['tom hanks', 'starred_in', 'splash'], ['tom hanks', 'starred_in', 'the man with one red shoe'], ['tom hanks', 'starred_in', 'volunteers'], ['tom hanks', 'starred_in', 'every time we say goodbye'], ['tom hanks', 'starred_in', 'the money pit'], ['tom hanks', 'starred_in', 'nothing in common'], ['tom hanks', 'starred_in', 'dragnet'], ['tom hanks', 'starred_in', 'big'], ['tom hanks', 'starred_in', 'punchline'], ['tom hanks', 'starred_in', "the 'burbs"], ['tom hanks', 'starred_in', 'turner & hooch'], ['tom hanks', 'starred_in', 'the bonfire of the vanities'], ['tom hanks', 'starred_in', 'joe versus the volcano'], ['tom hanks', 'starred_in', 'a league of their own'], ['tom hanks', 'starred_in', 'philadelphia'], ['tom hanks', 'starred_in', 'sleepless in seattle'], ['tom hanks', 'starred_in', 'forrest gump'], ['tom hanks', 'starred_in', 'apollo 13'], ['tom hanks', 'starred_in', 'toy story'], ['tom hanks', 'starred_in', 'that thing you do!'], ['tom hanks', 'starred_in', 'toy story 2'], ['tom hanks', 'starred_in', 'the green mile'], ['tom hanks', 'starred_in', 'saving private ryan'], ['tom hanks', 'starred_in', "you've got mail"], ['tom hanks', 'starred_in', 'cast away'], ['tom hanks', 'starred_in', 'road to perdition'], ['tom hanks', 'starred_in', 'catch me if you can'], ['tom hanks', 'starred_in', 'the ladykillers'], ['tom hanks', 'starred_in', 'the polar express'], ['tom hanks', 'starred_in', 'the terminal'], ['tom hanks', 'starred_in', 'the da vinci code'], ['tom hanks', 'starred_in', 'toy story 3'], ['tom hanks', 'starred_in', 'the great buck howard'], ['tom hanks', 'starred_in', "charlie wilson's war"], ['tom hanks', 'starred_in', 'extremely loud & incredibly close'], ['tom hanks', 'starred_in', 'angels & demons'], ['tom hanks', 'starred_in', 'untitled elvis presley project'], ['tom hanks', 'starred_in', "defying the nazis: the sharps' war"], ['tom hanks', 'starred_in', 'cloud atlas'], ['tom hanks', 'starred_in', 'captain phillips'], ['tom hanks', 'starred_in', 'larry crowne'], ['tom hanks', 'starred_in', 'toy story 4'], ['tom hanks', 'starred_in', 'in the garden of beasts'], ['tom hanks', 'starred_in', 'saving mr. banks'], ['tom hanks', 'starred_in', 'a hologram for the king'], ['tom hanks', 'starred_in', 'inferno'], ['tom hanks', 'starred_in', 'a beautiful day in the neighborhood'], ['tom hanks', 'starred_in', 'sully'], ['tom hanks', 'starred_in', 'bios'], ['tom hanks', 'starred_in', 'bridge of spies'], ['tom hanks', 'starred_in', 'the circle'], ['tom hanks', 'starred_in', 'greyhound'], ['tom hanks', 'starred_in', 'the post'], ['tom hanks', 'starred_in', 'news of the world'], ['tom hanks', 'starred_in', 'a man called ove']]
list2 = [['Kevin Hart', 'starred_in', 'paper soldiers', 'paper soldiers', 'has_actor', 'beanie sigel'], ['Kevin Hart', 'starred_in', 'soul plane', 'soul plane', 'has_actor', 'dwayne adway', 'soul plane', 'has_actor', 'snoop dogg', 'soul plane', 'has_actor', 'tom arnold'], ['Kevin Hart', 'starred_in', 'not easily broken', 'not easily broken', 'has_actor', 'morris chestnut', 'not easily broken', 'has_actor', 'taraji p. henson', 'not easily broken', 'has_actor', 'maeve quinlan'], ['Kevin Hart', 'starred_in', 'the wedding ringer', 'the wedding ringer', 'has_actor', 'josh gad', 'the wedding ringer', 'has_actor', 'kaley cuoco', 'the wedding ringer', 'has_actor', 'affion crockett'], ['Kevin Hart', 'starred_in', 'extreme job'], ['Kevin Hart', 'starred_in', 'scrooged'], ['Kevin Hart', 'starred_in', 'night wolf'], ['Kevin Hart', 'starred_in', 'something like a business', 'something like a business', 'has_actor', 'clifton powell', 'something like a business', 'has_actor', 'jennifer titus', 'something like a business', 'has_actor', 'donnell rawlings'], ['Kevin Hart', 'starred_in', 'monopoly'], ['Kevin Hart', 'starred_in', 'ride along', 'ride along', 'has_actor', 'ice cube', 'ride along', 'has_actor', 'tika sumpter', 'ride along', 'has_actor', 'john leguizamo'], ['Kevin Hart', 'starred_in', 'central intelligence', 'central intelligence', 'has_actor', 'dwayne johnson', 'central intelligence', 'has_actor', 'danielle nicolet', 'central intelligence', 'has_actor', 'amy ryan'], ['Kevin Hart', 'starred_in', 'uptown saturday night'], ['Kevin Hart', 'starred_in', 'think like a man', 'think like a man', 'has_actor', 'chris brown', 'think like a man', 'has_actor', 'gabrielle union', 'think like a man', 'has_actor', 'michael ealy'], ['Kevin Hart', 'starred_in', '35 and ticking', '35 and ticking', 'has_actor', 'tamala jones', '35 and ticking', 'has_actor', 'nicole ari parker', '35 and ticking', 'has_actor', 'keith robinson'], ['Kevin Hart', 'starred_in', 'let go', 'let go', 'has_actor', 'david denman', 'let go', 'has_actor', 'gillian jacobs', 'let go', 'has_actor', 'edward asner'], ['Kevin Hart', 'starred_in', 'about last night', 'about last night', 'has_actor', 'regina hall', 'about last night', 'has_actor', 'joy bryant'], ['Kevin Hart', 'starred_in', 'the upside', 'the upside', 'has_actor', 'bryan cranston', 'the upside', 'has_actor', 'nicole kidman', 'the upside', 'has_actor', 'aja naomi king'], ['Kevin Hart', 'starred_in', 'captain underpants: the first epic movie', 'captain underpants: the first epic movie', 'has_actor', 'thomas middleditch', 'captain underpants: the first epic movie', 'has_actor', 'ed helms', 'captain underpants: the first epic movie', 'has_actor', 'nick kroll'], ['Kevin Hart', 'starred_in', '9mm', '9mm', 'has_actor', 'queen latifah'], ['Kevin Hart', 'starred_in', 'think like a man too', 'think like a man too', 'has_actor', 'wendi mclendon-covey', 'think like a man too', 'has_actor', 'la la anthony'], ['Kevin Hart', 'starred_in', 'jumanji: welcome to the jungle', 'jumanji: welcome to the jungle', 'has_actor', 'karen gillan', 'jumanji: welcome to the jungle', 'has_actor', 'jack black'], ['Kevin Hart', 'starred_in', 'get hard', 'get hard', 'has_actor', 'will ferrell', 'get hard', 'has_actor', 'alison brie', 'get hard', 'has_actor', 't.i.'], ['Kevin Hart', 'starred_in', 'the secret life of pets', 'the secret life of pets', 'has_actor', 'louis c.k.', 'the secret life of pets', 'has_actor', 'eric stonestreet', 'the secret life of pets', 'has_actor', 'lake bell'], ['Kevin Hart', 'starred_in', 'top five', 'top five', 'has_actor', 'chris rock', 'top five', 'has_actor', 'rosario dawson'], ['Kevin Hart', 'starred_in', 'ride along 2', 'ride along 2', 'has_actor', 'benjamin bratt'], ['Kevin Hart', 'starred_in', 'fatherhood', 'fatherhood', 'has_actor', 'anthony carrigan', 'fatherhood', 'has_actor', 'alfre woodard', 'fatherhood', 'has_actor', 'paul reiser'], ['Kevin Hart', 'starred_in', 'the secret life of pets 2', 'the secret life of pets 2', 'has_actor', 'patton oswalt', 'the secret life of pets 2', 'has_actor', 'harrison ford'], ['Kevin Hart', 'starred_in', 'dashing through the snow'], ['Kevin Hart', 'starred_in', 'ride along 3'], ['Kevin Hart', 'starred_in', 'night school', 'night school', 'has_actor', 'tiffany haddish', 'night school', 'has_actor', 'rob riggle', 'night school', 'has_actor', 'romany malco'], ['Kevin Hart', 'starred_in', 'the great outdoors', 'the great outdoors', 'has_actor', 'teena lewis', 'the great outdoors', 'has_actor', 'tristan cantave'], ['Kevin Hart', 'starred_in', 'on the run'], ['Kevin Hart', 'starred_in', 'jumanji: the next level', 'jumanji: the next level', 'has_actor', 'awkwafina'], ['Kevin Hart', 'starred_in', 'my own worst enemy'], ['Kevin Hart', 'starred_in', 'co-parenting'], ['Kevin Hart', 'starred_in', 'black friday'], ['Kevin Hart', 'starred_in', 'untitled Kevin Hart/romantic comedy project'], ['Kevin Hart', 'starred_in', 'lone wolf', 'lone wolf', 'has_actor', 'dyann brown', 'lone wolf', 'has_actor', 'jamie newcomb', 'lone wolf', 'has_actor', 'ann douglas'], ['Kevin Hart', 'starred_in', 'mindkiller', 'mindkiller', 'has_actor', 'joe mcdonald', 'mindkiller', 'has_actor', 'wade kelley', 'mindkiller', 'has_actor', 'shirley ross'], ['Kevin Hart', 'starred_in', 'conviction', 'conviction', 'has_actor', 'catharine e. jones'], ['Kevin Hartzman', 'starred_in', 'getting out', 'getting out', 'has_actor', 'michael j. renda', 'getting out', 'has_actor', "ashley-rene' everest", 'getting out', 'has_actor', 'george avgoustis', 'getting out', 'has_actor', 'jerry hayes', 'getting out', 'has_actor', 'joe elliott', 'getting out', 'has_actor', 'denise emilia sandulescu'], ['Kevin Hartzman', 'starred_in', 'desperate cowboys', 'desperate cowboys', 'has_actor', 'michael j. mowery', 'desperate cowboys', 'has_actor', 'keyna reynolds', 'desperate cowboys', 'has_actor', 'carter burch', 'desperate cowboys', 'has_actor', 'donna barbera', 'desperate cowboys', 'has_actor', 'mo el-zaatari', 'desperate cowboys', 'has_actor', 'justin serino'], ['Kevin Hart', 'starred_in', 'the man who spoke to himself', 'the man who spoke to himself', 'has_actor', 'jeff nicholson', 'the man who spoke to himself', 'has_actor', 'juniper purinton', 'the man who spoke to himself', 'has_actor', 'peggy ann lloyd', 'the man who spoke to himself', 'has_actor', 'scott tuke', 'the man who spoke to himself', 'has_actor', 'kali rima mcgurk']]

predicates1 = [['directed'], ['starred in']]
predicates2 = [['starred_in', 'has_actor']]

names1 = ['Kevin Hart']
names2 = ['steven spielberg', 'tom hanks']

a = seperate_all_paths(predicates2, list2, names2)

print(a)