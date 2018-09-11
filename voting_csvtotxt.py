################################
# winner.py -- Winner Computation
#
# -*- coding: utf-8 -*-
import scipy.misc
import pandas as pd
import itertools
import codecs
from bloc_rule import *
from random import *
from sys import *

reload(sys)
sys.setdefaultencoding('utf-8')

#############################################################
# read in the information of candidates in our format
# m (number of candidates)
# Name1,gender_1,age_1,locality_1 (sensitive attributes of m candidates: gender: male/female, age: junior/middle-aged/senior, locality: city/countryside)
# ...

# return name

def readData_name(f):
    name = []
    lines = f.readlines()
    m = lines[0].split('\n')

    for l in lines[1:int(m[0]) + 1]:
        l.strip('\n')
        name += l.split(",")[0:1]

    return name


##############################################################
# compute the votes of each candidate
def readData_votes(f,name):

    m = len(name)
    votes = [0]*m
    lines = f.readlines()

    for l in lines[1:]:
        l.strip('\n')
        string = l.split(";")[1:3]
        male = string[0].split(",")
        for c in male:
            for i in range(m):
                if name[i] in c:
                    votes[i] += 1

        female = string[1].split(",")
        for c in female:
            for i in range(m):
                if name[i] in c:
                    votes[i] += 1

    return votes


###############################################################
# main program

if __name__ == "__main__":

    seed()

    # singleopt_cplex = 0
    # singleopt_ouralg = 0

    ##################################
    # input
    district = str(argv[1])

    # read the information of candidates
    candidate = district + "_candidates"
    candidate_file = open("Dist_"+district+"/"+candidate, "r")
    name = readData_name(candidate_file)
    m = len(name)

    ballot = str(argv[2])
    #ballot_file = pd.read_csv(ballot, delimiter=';', decimal=',', encoding='latin-1')
    ballot_file = codecs.open("Dist_"+district+"/"+ballot, "r", "latin-1")
    votes = readData_votes(ballot_file,name)

###################################################
    # output the votes file

    file_name = district + "_votes"
    district_votes = open("Dist_"+district+"/"+file_name, "w")
    for ii in range(m):
        row = name[ii] + "," + str(votes[ii]) + "\n"
        district_votes.write(row.encode())
