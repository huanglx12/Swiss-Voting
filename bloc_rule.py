import numpy as np
import sys

sys.path.append('/afs/akt.tu-berlin.de/service/cplex/cplex/python/x86-64_sles10_4.1') # the path of CPLEX package
import cplex
from cplex.exceptions import CplexError


# generate the optimization problem for fair voting:
# Each binary variable xi represents a candidate Ci. xi = 1 means that we select candidate Ci as a winner.
# xi should satisfy the cardinality constraint sum_i xi = k and all fairness constraints according to sensitive attributes.
def write_cplex_format_bloc(tmp, C, score, k, stru, lowpar, uppar):
    m = len(score)
    f = open(tmp, 'w')


    # generate the objective function: the total score of the selected committee
    s = "Maximize\nobj:"

    pos = 0
    first = True
    for i in range(m):
        if not first:
            s += " +"
        first = False
        s += " " + str(score[i]) + " x" + str(i)

        pos += 1

    f.write(s + "\n")
    f.write("Subject To\n")

    # generate the cardinality constraint: the number of selected winners is k.
    subj_k = "c1:"
    first = True
    for i in range(m):
        if not first:
            subj_k += " +"
        first = False
        subj_k += " " + "x" + str(i)

    f.write(subj_k + ' = ' + str(k) + '\n')

    # generate the fairness constraint for different categories of all groups.

    num = 1
    for j in range(len(stru)):
        for l in range(stru[j]):
            num += 1
            subj_l = "c" + str(num) + ":" # the lower bound constraint for category stru[j][l]
            num += 1
            subj_u = "c" + str(num) + ":" # the upper bound constraint for category stru[j][l]
            first = True
            for i in range(m):
                if int(C[i][j]) == l: # the j-th sensitive attribute of candidate i is of value l
                    if not first:
                        subj_l += " +"
                        subj_u += " +"
                    first = False
                    subj_l += " " + "x" + str(i)
                    subj_u += " " + "x" + str(i)

            f.write(subj_l + ' >= ' + str(lowpar[j][l]) + '\n')
            f.write(subj_u + ' <= ' + str(uppar[j][l]) + '\n')



    # list all binary variables
    f.write("Binary\n")
    for i in range(m):
        f.write("x" + str(i) + "\n")

    f.write("End\n")
    f.close()


# apply CPLEX to compute all optimal committees with fairness constraints and the optimal score
def run_ilp_bloc(C, score, k, stru, lowpar, uppar):
    m = len(score)

    tmp = "optimization" + ".lp"

    # generate the optimization problem for fair voting
    write_cplex_format_bloc(tmp, C, score, k, stru, lowpar, uppar)
    cpx = cplex.Cplex(tmp)

    cpx.set_log_stream(None)
    cpx.set_error_stream(None)
    cpx.set_results_stream(None)

    # apply CPLEX to solve the optimization problem
    try:
        cpx.parameters.randomseed.set(1)
        cpx.solve()
    except CplexError, exc:
        print >> sys.stderr, "There is no feasible solution."
        return

    opt = int(cpx.solution.get_objective_value()) # compute the score of the optimal committee with fairness constraints

    cpx.parameters.mip.pool.absgap.set(0) # ensure to compute optimal committees
    cpx.parameters.mip.limits.populate.set(3000000) # output at most 10000 optimal committees. The number 100 can be modified accordingly.
    cpx.parameters.mip.pool.intensity.set(4)
    cpx.populate_solution_pool()
    # print>>sys.stderr, opt, cpx.solution.pool.get_num()

    x = {} # solutions computed by CPLEX
    candidates = {}
    c = {} # record all optimal committees
    for i in range(cpx.solution.pool.get_num()):
        x[i] = np.array(cpx.solution.pool.get_values(i,)[-m:])
        candidates[i] = np.arange(0, m, 1)
        c[i] = candidates[i][np.logical_and(x[i] > 0.9, x[i] < 1.1)]

    # print >>sys.stderr, "There are %d optimal committees" % (len(c))

    return c, opt


# compute all optimal committees with fairness constraints
def bloc( C, score, k, stru, lowpar, uppar ):

  (winning_committee, total_satisfaction) = run_ilp_bloc(C, score, k, stru, lowpar, uppar)
  return winning_committee, total_satisfaction