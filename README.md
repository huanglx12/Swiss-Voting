# Swiss Voting in 2018


## 1. Swiss voting codes

The canton of Valais will be revising its Constitution and a Constitutional Assembly has to be elected in November, 2018. The electoral committee thinks that it is important that *all* members of the civil society are represented in the writing of a Constitution -- so they need a way to select a balance committee across important attributes: gender, age and locality. 

### 1.1. Running a single experiment using the default settings

To run the code, you need to install Python 2.7. The main program is balance_election.py, which takes an election as input, and computes optimal balanced committees. To test whether the code works, try:

  python balance_election.py Entremont

where "Entremont" is a district name. After running "balance_election.py", the code will generate an resulting file "Dist_Entremont/Entremont_result.txt" that contains the information of all winning committees.

### 1.2. Information of candidates and balance criteria

The basic information of Swiss voting can be found in the folder "Files_AppelCitoyen".
The file "Candidats-primaire-AC-final-pour-EPFL+Votebox.xlsx" contains the information of all candidates in different districts, including name (Nom and Prenom), gender (F/H), age (18-30/30-65/65+) and commune.
The file "Region.pdf" indicates how to divide different districts into at most 6 regions.
The file "Criteria.pdf" contains the balance constraints for gender, age and region in different districts. Note that the "flotant" column represents the number of selected candidates that can be allocated in any manner.

### 1.3. Generating all optimal balance committees into a .txt file

Program "balance_election.py" can compute all optimal balance committee that achieves the most votes by running and records them in a .txt file:

  python balance_election.py district alg_num

The key "district" represents the name of the district for election.

The program will read the following three files from the folder "Dist_district":
  "district_candidates" -- the file containing properties of candidates: gender, age and region;
  "district_attribute" -- the file containing the information of balance constraints;
  "district_votes" -- the file containing the information of votes.

The number "alg_num" represents the applied algorithm: alg_num=0 represents using the default enumerating algorithm and alg_num=1 represents using a CPLEX solver.
Hint: Using alg_num=1 requires to install a CPLEX solver (https://www.ibm.com/products/ilog-cplex-optimization-studio). After installing the provided IBM CPLEX solver, one should update line 4 in bloc_rule.py with the path of the cplex solver. E.g., the default path on MacOS seems to be /Applications/CPLEX_Studio_Community128/cplex/python/2.7/x86-64_osx. The code will also generate an additional file that contains the formulation of the corresponding integer linear program (optimization.lp).

The "district_candidates" file has the following format:
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

The "district_attribute" file has the following format:
  1. A single line with two numbers a1 and a2, which represents that the selected committee should contain exactly a1 males and a2 females.
  2. A single line with three numbers b1, b2 and b3, which represents that the selected committee should contain at least b1 candidates among age range 18-30, b2 candidates among age range 30-65, and b3 candidates among age range 65+.
  3. A single line with at most six numbers c1,c2,..., which represents that the selected committee should contain at least ci candidates from Region i of the corresponding district.
Hint: interested readers can modify the balance constraints in this file and check the consequences of changing criteria.

For example, the following file defines all balance constraints. Observe that there are two regions in this example.
  3,3
  1,2,1
  3,2


The "district_votes" file has the following format:
  1. m lines with two terms: candidate_name, votes. Here, "votes" is the number of votes obtained by the candidate. Note that the order of candidates should be the same as in "district_candidates".
Hint: interested readers can modify the number of votes in this file and check the consequences.

For example, the following file defines seven candidates:
  Valentina Darbellay,18
  Marie-Luce Duroux Barman,19
  Baptiste Fellay,22
  Jasmine Lovey,21
  Jean-François Lovey,29
  Daniel Moulin,25
  Léna Vaudan,22

If alg_num=0, the program will generate a file "Dist_district/district_result.txt". If alg_num=1, the program will generate a file "Dist_district/district_result_1.txt". One can verify that the two resulting files are exactly the same with the following format:
  1. Five lines that summarizes the results: total votes of the optimal unconstrained committee V1, total votes of an optimal balance committee V2, the number T of optimal balance committees, balance constraints and votes of candidates.
  2. T optimal balanced committees, each with the following format:
    1) A single line with a number that represents it is the i-th optimal committee.
    2) k lines with descriptions of the selected candidates. Each line is of form: candidate_name: gender, age, locality, #votes.
    3) A summarization of attributes for this optimal committee:
      I. Two lines represent the number of selected males and females respectively.
      II. Three lines represent the number of selected candidates among age range 18-30, 30-65, and 65+ respectively.
      III. l lines (l is the number of regions for the district) represent the number of selected candidates from each region.


For example, if input files are the prior examples containing seven candidates, running "python balance_election.py Entremont 0" or "python balance_election.py Entremont 1" produces the following contents:
  Total votes of the optimal unconstrained committee: 138
  Total votes of an optimal balance committee: 138
  Total number of optimal balance committees: 1
  Balance constraints: [[3, 3], [1, 2, 1], [3, 2]]
  Votes: [18 19 22 21 29 25 22]

  Optimal committee: 1
  Marie-Luce Duroux Barman: Female, 30-num_region5, Region 1, votes=19
  Baptiste Fellay: Male, 18-30, Region 2, votes=22
  Jasmine Lovey: Female, 18-30, Region 2, votes=21
  Jean-François Lovey: Male, 30-num_region5, Region 2, votes=29
  Daniel Moulin: Male, num_region5+, Region 1, votes=25
  Léna Vaudan: Female, 18-30, Region 1, votes=22
  Male: 3
  Female: 3
  18-30: 3
  30-65: 2
  65+: 1
  Region 1: 3
  Region 2: 3

### 1.4. Generating all optimal balance committees into a .csv file

Program "csv_result_generation.py" can compute all optimal balance committee that achieves the most votes by running and records them in a .csv file:

  python csv_result_generation.py district alg_num

The key "district" represents the name of the district for election.

The program will read the following four files from the folder "Dist_district":
  "district_candidates" -- the file containing properties of candidates: gender, age and region;
  "district_attribute" -- the file containing the information of balance constraints;
  "district_votes" -- the file containing the information of votes;
  "district_commune" -- the file containing the commune of candidates.

The number "alg_num" represents the applied algorithm: alg_num=0 represents using CPLEX and alg_num=1 represents using an enumerating algorithm.

We only need to introduce the format of the "district_commune" file:
  1. m lines with two terms: candidate_name, commune. Here, "commune" is the corresponding commune of the candidate. Note that the order of candidates should be the same as in "district_candidates".

For example, the following file defines seven candidates:
  Valentina Darbellay,Liddes
  Marie-Luce Duroux Barman,Vollèges
  Baptiste Fellay,Orsières
  Jasmine Lovey,Orsières
  Jean-François Lovey,Orsières
  Daniel Moulin,Vollèges
  Léna Vaudan,Bagnes

The program will generate a file "Dist_district/district_result.csv" with the following format:
  1. The first nine columns contain the information of candidates, including district, full name, gender, age, commune and the number of votes.
  2. T columns (assume there are T optimal balance committees), each with the following format:
    1) For the i-th optimal balance committee, the column name is "Committee i".
    2) If a candidate is selected by the i-th committee, then mark 1 in the corresponding grid. Otherwise, leave the grid blank.








 