#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program reads in an input, triples it and then writes the result
to a file. 
"""
import decimal
import sys 
import os
import math
import random
import numpy
from matplotlib import pyplot


# comment afterwards
#seed = sys.argv[2]

#random.seed(int(seed))
#numpy.random.seed(int(seed))

# run the load algo 1 on trace and random modes
def Load_Balancing_Algo1(p, s, mode, f, d, service_lines, arrival_lines, time_end):
    if mode == "trace":
        #simulate until all jobs have departed 

        # for i in arrival lines 
        sum_arrival = []

        # get the arrival time
        for i in range(len(arrival_lines)):
            if i == 0:
                sum_arrival.append(arrival_lines[i])
            else:
                sum_arrival.append(format(float(arrival_lines[i]) + float(sum_arrival[i-1]),'.4f'))
        new_list = list(zip(sum_arrival, service_lines))

    # consider time_end for random    
    elif mode == "random":
        # run until time_end
        
        # service time generated by g(t)
        # g(t) = 0 for 0 <= t <= a
        alpha = float(service_lines[0])
        beta = float(service_lines[1])
        
        t = getArrivalTime(arrival_lines)

        random_arrival = []
        random_service = []
        while (t < float(time_end)):
            random_arrival.append(t)
            t = t + getArrivalTime(arrival_lines)

        for i in range(len(random_arrival)):
            random_service.append(getServiceTime(alpha, beta))

        new_list =  list(zip(random_arrival, random_service))
        
    s1_queue = []
    s2_queue = []
    s3_queue = []

    s1_departure = []
    s2_departure = []
    s3_departure = []

    s1_arrival = []
    s2_arrival = []
    s3_arrival = []
    
    for j,i in new_list: 
        
        while s3_queue:
            if s3_queue[0] <= float(j):
                s3_departure.append(s3_queue[0])
                s3_queue.pop(0)
            else:
                break
        
        while s2_queue:
            if s2_queue[0] <= float(j):
                s2_departure.append(s2_queue[0])
                s2_queue.pop(0)
            else:
                break
        
        while s1_queue:
            if s1_queue[0] <= float(j):
                s1_departure.append(s1_queue[0])
                s1_queue.pop(0)
            else:
                break
        
        
        ns = min(len(s2_queue), len(s1_queue))

        if p == '1':
            condition = ns <= float(len(s3_queue))-float(d)
        elif p == '2':
            condition = ns <= float(len(s3_queue))/float(f)-float(d)

        if not s3_queue:
            s3_queue.append(float(j) + float(i)/float(f))
            s3_arrival.append(float(j))
        elif ns == 0 or condition:
            
            if len(s1_queue) == ns:
                if not s1_queue:
                    s1_queue.append(float(j) + float(i))
                else:
                    s1_queue.append(s1_queue[-1] + float(i))
                s1_arrival.append(float(j))
            else:
                if not s2_queue:
                    s2_queue.append(float(j) + float(i))
                else:
                    s2_queue.append(s2_queue[-1] + float(i))
                s2_arrival.append(float(j))
        else:
            s3_queue.append(s3_queue[-1] + float(i)/float(f))
            s3_arrival.append(float(j))
        # time is time plus the interarrival time
    
    while True:
        if s3_queue:
            s3_departure.append(s3_queue[0])
            s3_queue.pop(0)
        if s1_queue:
            s1_departure.append(s1_queue[0])
            s1_queue.pop(0)
        if s2_queue:
            s2_departure.append(s2_queue[0])
            s2_queue.pop(0)
        if not s3_queue and not s2_queue and not s1_queue:
            break
    
    response_time = 0

    for i in range(len(s1_arrival)):
        response_time =  response_time + (float(s1_departure[i]) - float(s1_arrival[i]))
    for i in range(len(s2_arrival)):
        response_time =  response_time + (float(s2_departure[i]) - float(s2_arrival[i]))

    for i in range(len(s3_arrival)):
        response_time =  response_time + (float(s3_departure[i]) - float(s3_arrival[i]))
    
    
    sum_served = len(s1_arrival) + len(s2_arrival) + len(s3_arrival)
    Output_to_File(s, mode, response_time, sum_served, s1_arrival, s1_departure, s2_arrival, s2_departure, s3_arrival, s3_departure)

    return

def getArrivalTime(arrival_lines):
    lenda = float(arrival_lines[0])
    a1 = random.expovariate(lenda)
        
    # uniformly distributed in the interval [a2l, a2u]
    a2l = float(arrival_lines[1])
    a2u = float(arrival_lines[2])
    a2 = random.uniform(a2l, a2u)

    # ak
    ak = a2 * a1

    return ak

def getServiceTime(alpha, beta):
    gamma = (beta - 1)/(alpha**(1-beta))
    prob = numpy.random.uniform(0,1)
    while prob == 0.0:
        prob = numpy.random.uniform(0,1)
    #prob = round(prob, 6)
    service_time = (prob*(1-beta)/gamma + alpha**(1-beta)) ** (1/(1-beta))
    return service_time

# takes input and output it to the files
def Output_to_File(s, mode, response_time, num_served, s1_arrival, server1, s2_arrival, server2, s3_arrival, server3):
    #if mode == 'trace':
    # add the mean response time to the file
    out_folder = 'output'
    out_file = os.path.join(out_folder, 'mrt_' + s + '.txt')
    mrt = (response_time/num_served)
    #format_mrt = truncate(mrt, 4)
    #print(mrt)
    #print(format(format_mrt,'.4f'))
    # TODO: remember to change this back from testing
    with open(out_file, 'w') as file:
        file.writelines(format(mrt, '.4f') + '\n')
    file.close()

    # add s1 output 
    s1out_file = os.path.join(out_folder, 's1_dep_' + s + '.txt')

    with open(s1out_file, 'w') as file:
        for i in range(len(s1_arrival)):
            file.writelines(str(format(s1_arrival[i],'.4f')) + '\t' + str(format(server1[i], '.4f')) + '\n')
    
    # add s2 output
    s2out_file = os.path.join(out_folder, 's2_dep_' + s + '.txt')

    with open(s2out_file, 'w') as file:
        for i in range(len(s2_arrival)):
            file.writelines(str(format(s2_arrival[i], '.4f')) + '\t' + str(format(server2[i], '.4f')) + '\n')
    
    # add s3 output
    s3out_file = os.path.join(out_folder, 's3_dep_' + s + '.txt')

    with open(s3out_file, 'w') as file:
        for i in range(len(s3_arrival)):
            file.writelines(str(format(s3_arrival[i], '.4f')) + '\t' + str(format(server3[i], '.4f')) + '\n')

    return

def main(s):
       
    config_folder = 'config'

    # First read the number 
    
    # Find the mode_number file
    mode_file = os.path.join(config_folder, 'mode_' + s + '.txt')

    with open (mode_file) as f:
        mode = f.readlines()[0]

        # read the list of inter-arrival times 
        interarrival_file = os.path.join(config_folder, 'interarrival_' + s + '.txt')
        # add all the arrival time into an array
        f = open(interarrival_file, "r")
        arrival_lines = []
        for line in f:
            arrival_lines.append(format(float(line), '.4f'))
        #arrival_lines = f.read().splitlines()
        f.close()

        # read the list of service times in the slow server time unit 
        service_file = os.path.join(config_folder, 'service_' + s + '.txt')
        f = open(service_file, "r")
        service_lines = f.read().splitlines()
        f.close()
        #print(service_lines)

        # read the content of the para file
        para_file = os.path.join(config_folder, 'para_' + s + '.txt')
        f = open(para_file, "r")
        para_lines = f.read().splitlines()
        f.close()

        # get the value of d and f
        d = para_lines[2]
        f = para_lines[0]
        time_end = 0
        
        if mode == 'trace':
            Load_Balancing_Algo1(para_lines[1],s, mode, f, d, service_lines, arrival_lines, time_end)
        elif mode == 'random':
            time_end = para_lines[3]
            Load_Balancing_Algo1(para_lines[1], s, mode, f, d, service_lines, arrival_lines, time_end)
        

if __name__ == "__main__":
   main(sys.argv[1])