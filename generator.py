import numpy as np
import matplotlib.pyplot as plt
import re
import itertools
import math


def combinations_tool(num, sides):
    results = {}
    line_results = []
    # Generate all combinations from set of possible die rolls, allow repeats
    combinations = list(itertools.combinations_with_replacement([i for i in range(1, sides+1)], num))

    # Iterate through unique combinations
    for comb in combinations:
        sum_val = sum(comb)

        # For each combinaiton, count the number of occurrences for each number
        # This lets us track duplicates
        duplicate_tracker = {}
        for val in comb:
            if val in duplicate_tracker.keys():
                duplicate_tracker[val] += 1
            else:
                duplicate_tracker[val] = 1

        # Number of unique permutations of list with duplicates can be represented by permutating the list
        # {List Length}!
        # Then dividing out the duplicates permutations 
        # For example 'ABABCD' would have (6!)/(2!2!) unique permutations

        # Calculates duplicate permutations for denominator
        denominator = 1
        for val in duplicate_tracker.values():
            denominator *= math.factorial(val)

        # num_unique_perms now represents all possible die rolls that map to this combination
        # They will always sum to the same value naturally
        num_unique_perms = (math.factorial(len(comb))/denominator)
        print("Combination", comb, sum_val, num_unique_perms)

        for i in range(0,int(num_unique_perms)):
            line_results.append(sum_val)
        
        # Using the number of the unique terms, we can increment the result hash at the key of their sum
        if sum_val in results.keys():
            results[sum_val] += num_unique_perms
        else:
            results[sum_val] = num_unique_perms
            
    # Map all the values to their respective proportion vs the total, make percentage 
    total = sum(results.values())
    results = {k: float(v)/float(total)*100 for k,v in results.items()}
    binomial_results = binomialize(results)
    return [results, binomial_results, str(num)+"d"+str(sides), line_results]
        
def binomialize(results):
    binomial_results = {}
    last_key = None
    for key in results.keys():
        if last_key:
            binomial_results[key] = results[key] + binomial_results[last_key]
            last_key = key
        else:
            last_key = key
            binomial_results[key] = results[key]
    return binomial_results

def plot_graphs(data):
    fig, axs = plt.subplots(2)
    fig.suptitle("Distributions of "+ data[2])
    axs[1].axhline(y=50, linewidth=1, color='b')
    axs[0].bar(data[0].keys(), data[0].values(), 0.7, color='g')
    axs[1].bar(data[1].keys(), data[1].values(), 0.7, color='r')
    fig.show()

def plot_line_grid(data_arr):
    fig1, f1_axes = plt.subplots(nrows=len(data_arr), ncols=len(data_arr[0]))
    for x in range(0, len(data_arr)):
        for y in range(0, len(data_arr[x])):
            f1_axes[x][y].scatter(data_arr[x][y][0], list(range(1, len(data_arr[x][y][0])+1)), color='b', s=2)
            f1_axes[x][y].plot(data_arr[x][y][0], list(range(1, len(data_arr[x][y][0])+1)), color='b')
            f1_axes[x][y].title.set_text(data_arr[x][y][1])
    fig1.suptitle("Scatterplots of dice sum occurrences generated through combination method, lines connect in order of occurrence: " + str(len(data_arr))+'x'+str(len(data_arr[x])))
    fig1.show()


pattern = re.compile("^\d+d\d+$")
pattern_linegrid = re.compile("^\d+x\d+$")
while True:
    print("Please type your die:")
    value = input()
    if pattern.match(value):
        values = list(map(lambda x: int(x), value.split("d")))
        data = combinations_tool(values[0], values[1])
        plot_graphs(  data)
    elif pattern_linegrid.match(value):
        values = list(map(lambda x: int(x), value.split("x")))
        datasets = []
        for x in range(0, values[0]):
            datasets.append([])
            for y in range(0, values[1]):
                dataset = combinations_tool(x+1, y+1)
                datasets[x].append([dataset[3], dataset[2]])
        plot_line_grid(datasets)

