import time as tm
import random as rn
from Functions import *
import math as mt

# Generate perants
def AIS_MALBP(problem, ct, alpha, popsize, Descendants, cloned, mutation_rate, mutation_func, varsize = 4):
    # ct = int(problem)
    print(problem, ct)	
    prob = prob_data(problem)
    lb = mt.ceil(sum([prob[0][x]['Processing time'] for x in prob[0]])/ct)
    problem_data = prob[0]
    tasks = [x for x in problem_data]
    ts_len = len(tasks)
    total_area = prob[1]
    mutation_function = mutate_fn(mutation_func)
    best_solution_eval = float('inf')
    for i in prob[0]:
        prob[0][i]['Variance'] = rn.random() * ((prob[0][i]['Processing time']/varsize) ** 2)
        ct_test = prob[0][i]['Processing time'] + 1.96 * np.sqrt(prob[0][i]['Variance'])
        if ct_test > ct:
            prob[0][i]['Variance'] = ((ct - prob[0][i]['Processing time']) / 1.96) ** 2
    population= {}  
      
    start = tm.time()
    for j in range(popsize):
        sol_structure = rn.sample(tasks,ts_len)									
        population[j] = SolutionClass(ct, total_area, alpha, problem_data, sol_structure,2)        
        if population[j].solution[1] < best_solution_eval:
            bestsol = population[j].solution[0]                
            best_solution_eval = population[j].solution[1]
            best_struct = population[j].sol_structure
            num_stations, num_operators = population[j].solution[2][1], population[j].solution[3][1]
    # Generate Descendants
    for j in range(popsize):
        mutation_function(population[j], mutation_rate, Descendants)
        for k in population[j].mutated_solutions:
            if k[1] < best_solution_eval:
                best_solution_eval = k[1]
                bestsol = k[0]
                best_struct = list(k[0].keys())
                num_stations, num_operators = k[2][1], k[3][1]
    # Clonal selection
    sol = SolutionClass(ct, total_area, alpha, problem_data, best_struct,2)
    mutation_function(sol, mutation_rate, cloned)
    if sol.solution[1] < best_solution_eval:
        bestsol = sol.solution[0]                
        best_solution_eval = sol.solution[1]
        best_struct = sol.sol_structure
        num_stations, num_operators = sol.solution[2][1], sol.solution[3][1]        
    end = tm.time() - start
    return bestsol, best_solution_eval, num_stations, num_operators, end, lb