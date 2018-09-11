# Swiss Voting in 2018


## 1. Swiss voting codes

The canton of Valais will be revising its Constitution and a Constitutional Assembly has to be elected in November, 2018. The electoral committee thinks that it is important that *all* members of the civil society are represented in the writing of a Constitution -- so they need a way to select a balance committee across important attributes: gender, age and locality. 

### 1.1. Running a single experiment using the default settings

To run the code, you might need to install a package CPLEX (https://www.ibm.com/products/ilog-cplex-optimization-studio). 
The main program is balance_election.py, which takes an election as input, formulates voting as an integer linear program, and computes optimal balanced committees. To test whether the code works, try:

  python balance_election.py Entremont Entremont_candidates Entremont_attribute Entremont_votes

where "Entremont" is a district name, "Entremont_candidates" is a file containing the information of candidates, "Entremont_attribute" is a file containing the information of balance constraints, and "Entremont_votes" is a file containing the information of votes.
After running "balance_election.py", the code will generate an resulting file "result/Entremont_result.txt" that contains the information of all winning committees. The code will also generate an additional file that contains the formulation of the corresponding integer linear program (optimization.lp).


### 1.2. Generating all optimal balance committees

Program "balance_election.py" can compute all optimal balance committee that achieves the most votes by running:

  python balance_election.py district candidate_file attribute_file votes_file alg_num

The key "district" represents the name of the district for election.

The key "candidate_file" represents the file containing the information of candidates.

The key "attribute_file" represents the file containing the information of balance constraints.

The key "votes_file" represents the file containing the information of votes.

The number "alg_num" represents the applied algorithm: alg_num=0 represents using CPLEX and alg_num=1 represents using an enumerating algorithm.

The "candidate_file" file has the following format:
  1. A single line with a number m (the number of candidates).
  2. m lines with descriptions of the candidates. Each line contains four items: candidate_name, gender, age and region. Here "gender" takes 2 valued 0/1 which corresponds to male/female correspondingly, "age" takes 3 valued 0/1/2 which corresponds to age range 18-30/30-65/65+ correspondingly, and "region" takes at most 6 valued 0/1/2/3/4/5 which corresponds to different partitions with respect to the district.

For example, the following file defines seven candidates:
  7
  Valentina Darbellay,1,1,1
  Marie-Luce Duroux Barman,1,1,0
  Baptiste Fellay,0,0,1
  Jasmine Lovey,1,0,1
  Jean-François Lovey,0,1,1
  Daniel Moulin,0,2,0
  Léna Vaudan,1,0,0

The "attribute_file" file has the following format:
  1. A single line with two numbers a1 and a2, which represents that the selected committee should contain exactly a1 males and a2 females.
  2. A single line with three numbers b1, b2 and b3, which represents that the selected committee should contain at least b1 candidates among age range 18-30, b2 candidates among age range 30-65, and b3 candidates among age range 65+.
  3. A single line with at most six numbers c1,c2,..., which represents that the selected committee should contain at least ci candidates from Region i of the corresponding district.

For example, the following file defines all balance constraints. Observe that there are two regions in this example.
  3,3
  1,2,1
  3,2

The "votes_file" file has the following format:
  1. m lines with two terms: candidate_name, votes. Here, "votes" is the number of votes obtained by the candidate. Note that the order of candidates should be the same as in "candidate_file".

For example, the following file defines seven candidates:
  Valentina Darbellay,100
  Marie-Luce Duroux Barman,100
  Baptiste Fellay,100
  Jasmine Lovey,100
  Jean-François Lovey,100
  Daniel Moulin,100
  Léna Vaudan,100

The generated "result/district_result" file has the following format:
  1. Five lines that summarizes the results: total votes of the optimal unconstrained committee V1, total votes of an optimal balance committee V2, the number T of optimal balance committees, balance constraints and votes of candidates.
  2. T optimal balanced committees, each with the same form as described in Section 1.3.
    1) A single line with a number that represents it is the i-th optimal committee.
    2) k lines with descriptions of the selected candidates. Each line is of form: candidate_name: gender, age, locality, #votes.
    3) A summarization of attributes for this optimal committee:
      I. Two lines represent the number of selected males and females respectively.
      II. Three lines represent the number of selected candidates among age range 18-30, 30-65, and 65+ respectively.
      III. l lines (l is the number of regions for the district) represent the number of selected candidates from each region.


For example, if input files are the prior examples containing seven candidates, running "python balance_election.py Entremont Entremont_candidates Entremont_attribute Entremont_votes 0" or "python balance_election.py Entremont Entremont_candidates Entremont_attribute Entremont_votes 1" produces the following contents:
  Total votes of the optimal unconstrained committee: 600
  Total votes of an optimal balance committee: 600
  Total number of optimal balance committees: 2
  Balance constraints: [[3, 3], [1, 2, 1], [3, 2]]
  Votes: [100 100 100 100 100 100 100]

  Optimal committee: 1
  Marie-Luce Duroux Barman: Female, 30-num_region5, Region 1, votes=100
  Baptiste Fellay: Male, 18-30, Region 2, votes=100
  Jasmine Lovey: Female, 18-30, Region 2, votes=100
  Jean-François Lovey: Male, 30-num_region5, Region 2, votes=100
  Daniel Moulin: Male, num_region5+, Region 1, votes=100
  Léna Vaudan: Female, 18-30, Region 1, votes=100
  Male: 3
  Female: 3
  18-30: 3
  30-65: 2
  65+: 1
  Region 1: 3
  Region 2: 3

  Optimal committee: 2
  Valentina Darbellay: Female, 30-num_region5, Region 2, votes=100
  Marie-Luce Duroux Barman: Female, 30-num_region5, Region 1, votes=100
  Baptiste Fellay: Male, 18-30, Region 2, votes=100
  Jean-François Lovey: Male, 30-num_region5, Region 2, votes=100
  Daniel Moulin: Male, num_region5+, Region 1, votes=100
  Léna Vaudan: Female, 18-30, Region 1, votes=100
  Male: 3
  Female: 3
  18-30: 2
  30-65: 3
  65+: 1
  Region 1: 3
  Region 2: 3










 