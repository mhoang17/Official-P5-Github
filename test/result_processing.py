import pandas as pd
from collections import defaultdict

results = pd.read_csv("test_results.csv", sep="\t", header=None)
results_kg = pd.read_csv("test_results_kg.csv", sep="\t", header=None)

answer_num = results[1]
answer_percentage = results[3]
answer_placement_list = results[4]
answer_placement = results[5]

count = 0

for percentage in answer_percentage:
    if float(percentage) != 0.0:
        count += 1

print((count/len(answer_percentage))*100)


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

print((count/(len(results)-len(result_dict[1])))*100)

count = 0

for entry in result_dict:
    if entry != 1:
        for percentage in result_dict[entry]:
            if percentage*entry == entry:
                count += 1

print((count/(len(results)-len(result_dict[1])))*100)

avg_place = 0
count = 0

for value in answer_placement:
    if float(value) != 0:
        avg_place += float(value)
        count += 1

print(avg_place/count)

placement_list = []

for elem in answer_placement_list:
    elem_list = list(elem)
    placement_list += [s for s in elem_list if s.isdigit()]

count = 0

for value in placement_list:
    if int(value) == 1:
        count += 1

print((count/len(placement_list))*100)