# written by Thu Tran and Sandhya Ratnam
from math import *
import random
import time

# global variable:
SPEED = 900.0 # km/h according to https://en.wikipedia.org/wiki/Cruise_(aeronautics)

# read_csv reads the country-captials.read_csv
# returns a dictionary with country name as key
# a tuple of (capital name, lat, long)
def read_csv(filename):
    countries = {}  # empty dictonary
    f = open(filename, 'r')
    f.readline() # skip first line
    for line in f:
        parsetext = line.split(',')
        countries[parsetext[0]] = (parsetext[1], float(parsetext[2]), float(parsetext[3]))
    return countries;

# function to calculate distance form lat Long
# source: https://www.geeksforgeeks.org/program-distance-two-points-earth/
def calculate_distance(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula to calculate distance from lat long
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return(c * r)

# construct_distance takes a dictionary returned from read_csv
# returns a nested dictionary to note the distance of 2 countries
# example: distances['city1']['city2']
def construct_distance(countries, selected_countries):
    distances = {}  #distance is an empty dictionary
    for country in selected_countries:
        distances[country] = {}

    for country in distances.keys():
        lat1 = countries[country][1]
        long1 = countries[country][2]
        for other in selected_countries:
            lat2 = countries[other][1]
            long2 = countries[other][2]
            distances[country][other] = calculate_distance(lat1, lat2, long1, long2) # calculate distance here

    return distances

# greedy_search takes in starting city, distances (nested dictionary), time time_limit
# returns a list of the city to visit in order
# heursitics is the closest city
def best_first_greedy_search(start, distances, time_limit = inf):
    result = []
    list_of_countries = {}; # a dictionary of countries, visited
    for countries in distances.keys():
        list_of_countries[countries] = False

    current_country = start
    next_country = start
    time = 0 # hours
    all_visited = False
    time_to_go_home = 0 # time to go home from next city
    time_to_next_country = 0 # time to go from current city to next city
    while (time + time_to_next_country + time_to_go_home < time_limit and (not all_visited)):
        current_country = next_country # set current country to next country
        list_of_countries[current_country] = True
        time += time_to_next_country # increment the time
        result.append(current_country) # add current country to result
        current_country_distances = distances[current_country] # a dictionary containing distances from current country to other countries
        sorted_d = sorted(current_country_distances.items(), key=lambda x: x[1]) # a list of tuples
        for each_neighbor in sorted_d:
            # plan our next country
            if (list_of_countries[each_neighbor[0]] == False):
                next_country = each_neighbor[0]
                time_to_go_home = distances[start][next_country] / SPEED
                time_to_next_country = distances[current_country][next_country] / SPEED
                break # so as to only add 1

        # update all_visited
        temp = True
        for each in list_of_countries.values():
            temp = temp and each
        all_visited = temp
    # end of while loop

    #go home
    result.append(start)
    time += distances[start][current_country] / SPEED

    return result, time

def breadth_first_search(start, distances, time_limit = inf):
    invert_speed = 1/SPEED
    min_result = []
    min_time = inf
    queue = []
    # each element entered into the q is a tuple of the solution and
    # the cost of the solution
    queue.append(([start], 0))
    arr = []
    all_countries = distances.keys()
    while queue:
        u = queue.pop(0)
        cur_solution = u[0]
        cur_cost = u[1]
        # print("current solution length is " + str(len(cur_solution)) + " current cost: " + str(cur_cost))
         # if all countries have been explored
        if len(cur_solution) == len(all_countries):
            # update the cost
            cur_cost += distances[start][cur_solution[-1]] *invert_speed
            # going home
            cur_solution.append(start)
            # if this is a better solution
            # better solution is when we are able to visit the most city
            # in the shorter amount of time
            # priority 1: more countries, priority 2: less time
            if ((len(cur_solution) > len(min_result)) or (len(cur_solution) == len(min_result) and cur_cost < min_time)):
                min_time = cur_cost
                min_result = cur_solution

        else:
            # if from where we are going home is still within the cost then going home is a solution
            if (cur_cost + distances[cur_solution[-1]][start] *invert_speed <= time_limit):
                    arr = cur_solution.copy()
                    arr.append(start)
                    temp_cost = cur_cost + distances[arr[-1]][arr[-2]] *invert_speed
                    if ((len(arr) > len(min_result)) or (len(arr) == len(min_result) and temp_cost < min_time)):
                        min_time = temp_cost
                        min_result = arr

            for each_neighbor in all_countries:
                if each_neighbor not in cur_solution:
                    arr = cur_solution.copy()
                    # make sure that going to next neighbor and then go home would
                    # still make it under time constraints
                    if (cur_cost + distances[each_neighbor][arr[-1]] *invert_speed + distances[each_neighbor][start] *invert_speed <= time_limit):
                        arr.append(each_neighbor)
                        queue.append((arr, cur_cost + distances[arr[-2]][arr[-1]] *invert_speed))

    return min_result, min_time

# printing stats to compare performance of
# bfs and greedy on various problem size
def performance_stat(dict, size):
    # number of problems per case
    number_prob = 10
    # number of total countries
    all_countries = list(dict.keys())
    #print(all_countries)
    total_countries = len(all_countries)
    #various size of problems
    stats_bfs = [0] * len(size)
    stats_greedy = [0] * len(size)

    for i in range(len(size)):
        country_num = size[i]
        for j in range(number_prob):
            # countries to be in problem
            chosen_countries = []
            for k in range(country_num):
                # randomly pick countries to be in the problem domain
                random_num = random.randint(0,total_countries-1)
                # add to chosen countries
                chosen_countries.append(all_countries[random_num])
            # construct distances database for each problem
            print(chosen_countries)
            distances_database = construct_distance(dict, chosen_countries)
            start = time.time()
            breadth_first_search(chosen_countries[0], distances_database)
            end = time.time()
            stats_bfs[i] += (end - start)
            start = time.time()
            best_first_greedy_search(chosen_countries[0], distances_database)
            end = time.time()
            stats_greedy[i] += (end - start)

    for i in range(len(size)):
        stats_bfs[i] = stats_bfs[i] / number_prob
        stats_greedy[i] = stats_greedy[i] / number_prob

    print(stats_bfs)
    print(stats_greedy)
    return

# printing stats to compare solution quality of
# bfs and greedy on various problem size
def solution_quality_stat(dict, size):
    # number of problems per case
    number_prob = 10
    # number of total countries
    all_countries = list(dict.keys())
    #print(all_countries)
    total_countries = len(all_countries)
    #various size of problems
    stats_bfs = [0] * len(size)
    stats_greedy = [0] * len(size)

    for i in range(len(size)):
        country_num = size[i]
        for j in range(number_prob):
            # countries to be in problem
            chosen_countries = []
            for k in range(country_num):
                # randomly pick countries to be in the problem domain
                random_num = random.randint(0,total_countries-1)
                # add to chosen countries
                chosen_countries.append(all_countries[random_num])
            # construct distances database for each problem
            # print(chosen_countries)
            distances_database = construct_distance(dict, chosen_countries)
            res, time = breadth_first_search(chosen_countries[0], distances_database)
            stats_bfs[i] += time
            res, time = best_first_greedy_search(chosen_countries[0], distances_database)
            stats_greedy[i] += time

    for i in range(len(size)):
        stats_bfs[i] = stats_bfs[i] / number_prob
        stats_greedy[i] = stats_greedy[i] / number_prob

    print(stats_bfs)
    print(stats_greedy)
    return

def analysis(dict):
    size = [3,5,8,10]
    performance_stat(dict, size)
    solution_quality_stat(dict, size)

def main():
    dict = read_csv("country-capitals.csv")
    mode = input("Enter 'a' for analysis mode, other keys for user mode: ")
    if mode == "a":
        analysis(dict)
    else:
        print("List of all countries: ")
        all_countries_str = ""
        count = 0
        for each in dict.keys():
            all_countries_str += each + "    "
            count += 1
            if count == 5:
                count = 0
                all_countries_str += "\n"
        print(all_countries_str)
        input_countries = input("Enter list of countries separated by comma: ")
        chosen_countries = input_countries.split(',')
        input_time_limit = input("Enter time limit, skip for no time limit: ")
        if input_time_limit == "":
            limit = inf
        else:
            limit = float(input_time_limit)
        distances_database = construct_distance(dict, chosen_countries)
        if len(chosen_countries) <= 10:
            print("Optimal solution: ")
            res, time = breadth_first_search(chosen_countries[0], distances_database, time_limit=limit)
            print(res)
            print("total time: ", time)
            print("Greedy solution: ")
            res, time = best_first_greedy_search(chosen_countries[0], distances_database, time_limit=limit)
            print(res)
            print("total time: ", time)
        else:
            print("Optimal solution not possible")
            print("Greedy solution: ")
            res, time = best_first_greedy_search(chosen_countries[0], distances_database, time_limit=limit)
            print(res)
            print("total time: ", time)

if __name__ == "__main__":
    main()
