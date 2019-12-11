import pandas as pd
from collections import defaultdict

results = pd.read_csv("test_results.csv", sep="\t", header=None)

answer_num = results[1]
answer_percentage = results[3]

count = 0

for percentage in answer_percentage:
    if float(percentage) != 0.0:
        count += 1

print((count/len(results))*100)


result_dict = defaultdict(list)

i = 0

for number in answer_num:
    result_dict[number].append(answer_percentage[i])
    i += 1

count2 = 0

for entry in result_dict:
    if entry != 1:
        for percentage in result_dict[entry]:
            if percentage*entry >= 2:
                count2 += 1

print((count2/(len(results)-len(result_dict[1])))*100)

