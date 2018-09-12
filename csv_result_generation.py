################################
# winner.py -- Winner Computation
#
# -*- coding: utf-8 -*-
import scipy.misc
import copy
import itertools
from random import *
from sys import *
import csv
import codecs

# import rule package
from bloc_rule import *

reload(sys)
sys.setdefaultencoding('utf-8')




# divide an integer n into the sum of d integers
def partition(n, d, Upper, depth=0):
    if d == depth:
        return [[]]
    return [
        [i] + item
        for i in range(min(n, Upper[0]) + 1)
        for item in partition(n - i, d, Upper[1:], depth=depth + 1)
    ]

#############################################################
# read in the information of candidates in the following format
# m (number of candidates)
# Name1,gender_1,age_1,locality_1 (sensitive attributes of m candidates: gender: male/female, age: junior/middle-aged/senior, locality: city/countryside)
# ...

# return (C,name)

def readData_candidate(f):

    C = [] # attribute information of candidates
    name = [] # name information of candidates
    lines = f.readlines()
    m = lines[0].split('\n')

    for l in lines[1:int(m[0]) + 1]:
        l.strip('\n')
        name += l.split(",")[0:1]
        s = l.split(",")[1:4]
        s = [int(x) for x in s]
        C += [s]

    return (C, name)

############################################################
# read in the information of balance constraints for all attributes
# #Male,#Female
# #18-30,#30-65,#65+
# #Region 1,#Region 2, ...

# return (lowpar)

def readData_attr(f):

    lowpar = [] # balance (lower) constraints for gender, age and region
    lines = f.readlines()

    for l in lines[0:3]:
        l.strip('\n')
        s = l.split(",")[0:]
        s = [int(x) for x in s]
        lowpar += [s]

    return (lowpar)

#############################################################
# read in the information of votes in the following format
# Name 1,votes 1
# Name 2,votes 2
# ...
# Name m,votes m

# return (votes)

def readData_votes(f,m):

    votes = []
    lines = f.readlines()

    for l in lines[0:]:
        l.strip('\n')
        s = l.split(",")[1:2]
        votes += s
    votes = np.array(votes)
    votes = map(int,votes)
    return votes

#################################################################
# read in the information of commune in our format
# Name1,commune1
# ...

# return commune

def readData_commune(f):
    commune = []
    lines = f.readlines()

    for l in lines[0:]:
        l = l.strip('\n')
        s = l.split(",")[1:]
        commune += s
    return commune


#################################################################

#
# print winners
#

# print all optimal balance committees

def printWinners(W, C, votes, district, name, commune):
    num = len(W)  # the number of optimal feasible committees
    m = len(name)
    output_name = district + "_result" + ".csv"
    output_file = codecs.open("Dist_"+district+"/"+output_name, "w")
    output_file.write("District;Full name of candidate;F;H;18-30;31-65;65+;Commune;#votes;")
    for j in range(num-1):
        string = "Committee " + str(j+1) + ";"
        output_file.write(string)
    output_file.write("Committee " + str(num) + "\n")

    for i in range(m):
        if C[i][0] == 1:
            gender = "1;"
        elif C[i][0] == 0:
            gender = ";1"
        if C[i][1] == 0:
            age = "1;;"
        elif C[i][1] == 1:
            age = ";1;"
        elif C[i][1] == 2:
            age = ";;1"
        row = district + ";" + name[i] + ";" + gender + ";" + age + ";" + commune[i] + ";" + str(votes[i]) + ";"
        output_file.write(row.encode('latin-1'))
        for j in range(num-1):
            sol = list(W[j])
            if i in sol:
                type = "1"
            else:
                type = ""
            output_file.write(type+";")
        sol = list(W[num-1])
        if i in sol:
            type = "1"
        else:
            type = ""
        output_file.write(type + "\n")

    output_file.close()



if __name__ == "__main__":

    ##################################
    # input

    # read the district name for election
    district = str(argv[1])

    # read the information of candidates
    candidate = district+"_candidates"
    candidate_file = open("Dist_"+district+"/"+candidate, "r")
    (C, name) = readData_candidate(candidate_file)
    C = np.array(C)
    m = len(C)

    # read the information of balance constraints
    attr = district+"_attribute"
    attr_file = open("Dist_"+district+"/"+attr, "r")
    lowpar = readData_attr(attr_file)
    num_region = len(lowpar[2])
    k = lowpar[0][0] + lowpar[0][1]
    uppar = [[m, m], [m, m, m], [m] * num_region]  # upper fairness parameters for different categories of all groups

    # read the information of votes
    votes = np.random.randint(500, size=m)
    voting = district+"_votes"
    voting_file = open("Dist_"+district+"/"+voting, "r")
    votes = readData_votes(voting_file, m)

    # read the information of commune
    commune_file = codecs.open("Dist_"+district+"/"+district+"_commune", "r")
    commune = readData_commune(commune_file)

    stru = [2, 3,num_region]  # the group structure of sensitive attributes. Each number represents the number of categories in different groups.
    cand = [["Male", "Female"], ["18-30", "30-65", "65+"],
            ["Region 1", "Region 2", "Region 3", "Region 4", "Region 5",
             "Region 6"]]  # cand is the corresponding category names of stru

    ###################################################
    # decide the applied algorithm
    alg = 0
    if len(argv) > 2:
        alg = int(argv[2])

    #####################################
    # using CPLEX to compute the optimal balance committees
    if alg == 1:
        W, S = bloc(C, votes, k, stru, lowpar, uppar)  # compute optimal committees with balance constraints

        sortvotes = sorted(map(int, votes), reverse=True)
        US = 0
        for i in range(k):
            US += sortvotes[i]  # compute the total votes of the unconstrained optimal committee

        printWinners(W, C, votes, district, name, commune) # output the results

    ###########################################################################################################
    # using an enumerating algorithm to compute the optimal balance committees
    ################################################################################
    # compute the number of candidates in each partition
    elif alg == 0:
        sortvotes = sorted(map(int, votes), reverse=True)
        US = 0
        for i in range(k):
            US += sortvotes[i]  # compute the total votes of the unconstrained optimal committee

        per_lowpar = copy.deepcopy(lowpar)
        for rr in range(num_region + 1, 7):
            per_lowpar[2] += [0]

        num_male = [[0 for col in range(3)] for row in range(num_region)]
        name_male = [[{} for col in range(3)] for row in range(num_region)]
        for i in range(m):
            if C[i][0] == 0:
                age = int(C[i][1])
                region = int(C[i][2])
                num_male[region][age] += 1
                name_male[region][age][i] = votes[i]
        male_att = np.nonzero(num_male)
        nonzero_male = len(male_att[0])
        upper_male = [0] * nonzero_male
        for i in range(nonzero_male):
            upper_male[i] = num_male[male_att[0][i]][male_att[1][i]]
        for i in range(num_region):
            for j in range(3):
                name_male[i][j] = sorted(name_male[i][j].items(), key=lambda x: x[1], reverse=True)

        num_female = [[0 for col in range(3)] for row in range(num_region)]
        name_female = [[{} for col in range(3)] for row in range(num_region)]
        for i in range(m):
            if C[i][0] == 1:
                age = int(C[i][1])
                region = int(C[i][2])
                num_female[region][age] += 1
                name_female[region][age][i] = votes[i]
        female_att = np.nonzero(num_female)
        nonzero_female = len(female_att[0])
        upper_female = [0] * nonzero_female
        for i in range(nonzero_female):
            upper_female[i] = num_female[female_att[0][i]][female_att[1][i]]
        for i in range(num_region):
            for j in range(3):
                name_female[i][j] = sorted(name_female[i][j].items(), key=lambda x: x[1], reverse=True)

        ############################################################################

        # enumerate all possible divisions of k with respect to non-zero partitions

        male_per = [[lowpar[0][0] - sum(p)] + p for p in partition(lowpar[0][0], nonzero_male - 1, upper_male[1:])]
        male_winner = []
        for i in range(len(male_per)):
            if male_per[i][0] <= upper_male[0]:
                male_winner += [male_per[i]]

        female_per = [[lowpar[0][1] - sum(p)] + p for p in
                      partition(lowpar[0][1], nonzero_female - 1, upper_female[1:])]
        female_winner = []
        for i in range(len(female_per)):
            if female_per[i][0] <= upper_female[0]:
                female_winner += [female_per[i]]

        ###########################################################################
        # compute all optimal solutions

        opt = 0  # the optimal total votes
        fea = 0  # number of feasible solutions
        opt_committee = []

        for mm in range(len(male_winner)):
            for ff in range(len(female_winner)):
                num_y = 0
                num_a = 0
                num_o = 0
                num_0 = 0
                num_1 = 0
                num_2 = 0
                num_3 = 0
                num_4 = 0
                num_5 = 0

                for i in range(nonzero_male):
                    # region
                    if male_att[0][i] == 0:
                        num_0 += male_winner[mm][i]
                    elif male_att[0][i] == 1:
                        num_1 += male_winner[mm][i]
                    elif male_att[0][i] == 2:
                        num_2 += male_winner[mm][i]
                    elif male_att[0][i] == 3:
                        num_3 += male_winner[mm][i]
                    elif male_att[0][i] == 4:
                        num_4 += male_winner[mm][i]
                    elif male_att[0][i] == 5:
                        num_5 += male_winner[mm][i]
                    # age
                    if male_att[1][i] == 0:
                        num_y += male_winner[mm][i]
                    elif male_att[1][i] == 1:
                        num_a += male_winner[mm][i]
                    elif male_att[1][i] == 2:
                        num_o += male_winner[mm][i]

                for i in range(nonzero_female):
                    # region
                    if female_att[0][i] == 0:
                        num_0 += female_winner[ff][i]
                    elif female_att[0][i] == 1:
                        num_1 += female_winner[ff][i]
                    elif female_att[0][i] == 2:
                        num_2 += female_winner[ff][i]
                    elif female_att[0][i] == 3:
                        num_3 += female_winner[ff][i]
                    elif female_att[0][i] == 4:
                        num_4 += female_winner[ff][i]
                    elif female_att[0][i] == 5:
                        num_5 += female_winner[ff][i]
                    # age
                    if female_att[1][i] == 0:
                        num_y += female_winner[ff][i]
                    elif female_att[1][i] == 1:
                        num_a += female_winner[ff][i]
                    elif female_att[1][i] == 2:
                        num_o += female_winner[ff][i]

                count = 1
                total_votes = 0

                if (num_y >= per_lowpar[1][0]) & (num_a >= per_lowpar[1][1]) & (num_o >= per_lowpar[1][2]):
                    if (num_0 >= per_lowpar[2][0]) & (num_1 >= per_lowpar[2][1]) & (num_2 >= per_lowpar[2][2]) & (
                            num_3 >= per_lowpar[2][3]) & (num_4 >= per_lowpar[2][4]) & (num_5 >= per_lowpar[2][5]):
                        committee_male = [[] for row in range(nonzero_male)]
                        all_male = [[]]
                        for i in range(nonzero_male):
                            if male_winner[mm][i] > 0:
                                count *= scipy.misc.comb(upper_male[i], male_winner[mm][i])
                                per_vote = 0
                                for vv in range(male_winner[mm][i]):
                                    per_vote += name_male[male_att[0][i]][male_att[1][i]][vv][1]
                                total_votes += per_vote
                                for item in itertools.combinations(range(upper_male[i]), male_winner[mm][i]):
                                    per_voteM = 0
                                    per_committee = []
                                    for c in item:
                                        per_voteM += name_male[male_att[0][i]][male_att[1][i]][c][1]
                                    if per_voteM == per_vote:
                                        for c in item:
                                            per_committee.append(name_male[male_att[0][i]][male_att[1][i]][c][0])
                                        committee_male[i] += [per_committee]
                                per_allmale = all_male
                                all_male = []
                                for com in per_allmale:
                                    for com1 in committee_male[i]:
                                        all_male += [com + com1]

                        committee_female = [[] for row in range(nonzero_female)]
                        all_female = [[]]
                        for i in range(nonzero_female):
                            if female_winner[ff][i] > 0:
                                count *= scipy.misc.comb(upper_female[i], female_winner[ff][i])
                                per_vote = 0
                                for vv in range(female_winner[ff][i]):
                                    per_vote += name_female[female_att[0][i]][female_att[1][i]][vv][1]
                                total_votes += per_vote
                                for item in itertools.combinations(range(upper_female[i]), female_winner[ff][i]):
                                    per_voteF = 0
                                    per_committee = []
                                    for c in item:
                                        per_voteF += name_female[female_att[0][i]][female_att[1][i]][c][1]
                                    if per_voteF == per_vote:
                                        for c in item:
                                            per_committee.append(name_female[female_att[0][i]][female_att[1][i]][c][0])
                                        committee_female[i] += [per_committee]
                                per_allfemale = all_female
                                all_female = []
                                for com in per_allfemale:
                                    for com1 in committee_female[i]:
                                        all_female += [com + com1]

                        fea += count
                        if total_votes >= opt:
                            if total_votes > opt:
                                opt = total_votes
                                opt_committee = []
                            for com in all_male:
                                for com1 in all_female:
                                    opt_committee += [sorted(com + com1)]

        printWinners(opt_committee, C, votes, district, name, commune) # output the results

