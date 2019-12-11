import pandas as pd
from collections import defaultdict

results = pd.read_csv("test_results.csv", sep="\t", header=None)
results_kg = pd.read_csv("test_results_kg.csv", sep="\t", header=None)

answer_num = results[1]
answer_percentage = results[3]
answer_placement_list = results[4]
answer_placement = results[5]

answer_percentage_kg = results_kg[3]

count = 0

for percentage in answer_percentage:
    if float(percentage) != 0.0:
        count += 1

print("Answer contains at least one candidate answer:       ", round((count/len(answer_percentage))*100, 4), "%")


result_dict = defaultdict(list)

i = 0

for number in answer_num:
    result_dict[number].append(answer_percentage[i])
    i += 1

count = 0

for entry in result_dict:
    if entry != 1:
        for percentage in result_dict[entry]:
            if percentage*entry >= 2:
                count += 1

print("Answer contains at least two candidate answers:      ", round((count/(len(results)-len(result_dict[1])))*100, 4), "%")

count = 0

for entry in result_dict:
    if entry != 1:
        for percentage in result_dict[entry]:
            if percentage*entry == entry:
                count += 1

print("Answer contains all candidate answers (more than 2): ", round((count/(len(results)-len(result_dict[1])))*100, 4), "%")

avg_place = 0
count = 0

for value in answer_placement:
    if float(value) != 0:
        avg_place += float(value)
        count += 1

print("Placement of candidate answers in our answer:        ", round(avg_place/count, 2))

placement_list = []

for elem in answer_placement_list:
    elem_list = list(elem)
    placement_list += [s for s in elem_list if s.isdigit()]

count = 0

for value in placement_list:
    if int(value) == 1:
        count += 1

print("Candidate answer lies on nr. 1 spot:                 ", round((count/len(placement_list))*100, 4), "%")


count = 0
i = 0
for percentage in answer_percentage:
    if percentage > answer_percentage_kg[i]:
        count += 1
    i += 1

print("Contains more candidate result than no relevance:    ", count)
