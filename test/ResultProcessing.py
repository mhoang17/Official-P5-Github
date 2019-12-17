from random import randrange

import pandas as pd
from collections import defaultdict

results = pd.read_csv("test_results_window_2_principal.csv", sep="\t", header=None)

# The different columns in the file
answer_num = results[1]
answer_percentage = results[3]
answer_placement_list = results[4]
answer_placement = results[5]

# Make a dictionary of all the percentages
result_dict = defaultdict(list)
i = 0

for number in answer_num:
    result_dict[number].append(answer_percentage[i])
    i += 1

# A list of the placements in the file
placement_list = []

for elem in answer_placement_list:
    elem_list = list(elem)
    placement_list += [s for s in elem_list if s.isdigit()]

# Counter which will be reset after each test
count = 0

# We check how many question contains at least on candidate answer
for percentage in answer_percentage:
    if float(percentage) != 0.0:
        count += 1

print("Answer contains at least one candidate answer:       ", round((count/len(answer_percentage))*100, 4), "%")

count = 0
idx = 0

# Check if we have the same amount of single paths in all files
for value in answer_num:
    if results[2][idx] == 1:
        count += 1
    idx += 1

print("Only one path in answer:                             ", count)

count = 0
idx = 0

for value in answer_num:
    if value == 1 and results[2][idx] == 1:
        count += 1
    idx += 1

print("Only one path in answer and candidate answer:        ", count)


count = 0
# Check if the answers contains at least two candidate answers
# if the we get more than 1 candidate answer
for entry in result_dict:
    if entry != 1:
        for percentage in result_dict[entry]:
            if percentage*entry >= 2:
                count += 1

print("Answer contains at least two candidate answers:      ", round((count/(len(results)-len(result_dict[1])))*100, 4), "%")


count = 0
num_entries = 0
# Count how many times we get a all candidate answers in a answer
# if we have 2 to 10 candidate answers
for entry in result_dict:
    if entry != 1 and entry <= 10:
        num_entries += len(result_dict[entry])
        for percentage in result_dict[entry]:
            if percentage*entry == entry:
                count += 1

print("Answer contains all candidate answers (more than 2): ", round((count/num_entries)*100, 4), "%")

avg_place = 0
count = 0
# Average placement (not used in the report, just a nice to have)
for value in answer_placement:
    if float(value) != 0:
        avg_place += float(value)
        count += 1

print("Placement of candidate answers in our answer:        ", round(avg_place/count, 2))

count = 0
# Check how many times a candidate answer lies at top
for value in placement_list:
    if int(value) == 1:
        count += 1

print("Candidate answer lies on nr. 1 spot:                 ", round((count/len(placement_list))*100, 4), "%")

# Check how many times a candidate answer lies in the top 3
count = 0

for value in placement_list:
    if int(value) <= 3:
        count += 1

print("Candidate answer lies in top 3:                      ", round((count/len(placement_list))*100, 4), "%")
