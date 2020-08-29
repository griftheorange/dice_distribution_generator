import numpy as np
import matplotlib.pyplot as plt
import re
import itertools
import math


def get_distribution(num, sides):
    arr = []
    results = {}
    for n in range(0, sides**num):
        print(n)
        sum_val = sum([((n // (sides**m)) % sides)+1 for m in range(0,num)])
        if sum_val in results.keys():
            results[sum_val] += 1
        else:
            results[sum_val] = 1
    
    total = sum(results.values())

    results = {k: float(v)/float(total)*100 for k,v in results.items()}
    binomial_results = binomialize(results)

    return [results, binomial_results, str(num)+"d"+str(sides)]

def combinations_tool(num, sides):
    results = {}
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
        
        # Using the number of the unique terms, we can increment the result hash at the key of their sum
        if sum_val in results.keys():
            results[sum_val] += num_unique_perms
        else:
            results[sum_val] = num_unique_perms
            
    # Map all the values to their respective proportion vs the total, make percentage 
    total = sum(results.values())
    print(results)
    results = {k: float(v)/float(total)*100 for k,v in results.items()}
    binomial_results = binomialize(results)
    return [results, binomial_results, str(num)+"d"+str(sides)]
        
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
    plt.show()
        
def experiment(num, sides):
    val = num
    counter = 1
    results = {}
    for i in range(0, sides**num):
        if counter > sides:
            counter = 1
            val -= (sides-1)
        
        if val in results.keys():
            results[val] += 1
        else:
            results[val] = 1
        counter += 1
        val += 1
    print(results)


pattern = re.compile("^\d+d\d+$")
while True:
    print("Please type your die:")
    value = input()
    if pattern.match(value):
        values = list(map(lambda x: int(x), value.split("d")))
        # data = get_distribution(values[0], values[1])
        data = combinations_tool(values[0], values[1])
        plot_graphs(data)
        # experiment(values[0], values[1])

