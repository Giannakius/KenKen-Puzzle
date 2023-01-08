from csp import *

class CAGE :
    def __init__(self, variables, op, result):
        self.variables = variables
        self.op = op
        self.result = result
        
    def getOpstring(self):
        return self.string_op

    def getOp(self):
        return self.op
    
    def getVars(self):
        return self.variables
    
    def get_neighbours_by_cage(self,var):
        return_vars = list(self.variables)
        return_vars.remove(var)
        return return_vars
    
    def have_solution_eq(self,value):
            if value == self.result :
                return True
            return False
        
    def has_solution_add_mul_eq(self, remain_var, curr_val, currdomains):
        if len(remain_var) == 0:
            return curr_val == self.result

        for value in currdomains[remain_var[0]]:
            if self.getOp() == '+':
                new_value = value + curr_val
                boolvar = self.has_solution_add_mul_eq(remain_var[1:], new_value, currdomains)
                if boolvar == True:  
                    return True
            if self.getOp() == "*":
                new_value = value * curr_val
                boolvar = self.has_solution_add_mul_eq(remain_var[1:], new_value, currdomains)
                if boolvar == True:  
                    return True
        return False
            
    def has_solution_div_sub(self, var, curr_val, currdoms):
        if len(var) == 0:
            if self.getOp() == '-':
                return curr_val == self.result
            if self.getOp() == '/':
                return curr_val == float(self.result)
        else:
            for value in currdoms[var[0]]:
                if self.getOp() == '-':
                    return value - curr_val == self.result or curr_val - value == self.result
                if self.getOp() == '/':
                    if value == 0:
                        return value == self.result
                    elif curr_val == 0:
                        return curr_val == self.result
                    else:
                        return value / curr_val == self.result or curr_val / value == self.result
    
class KenKen (CSP) :

    def __init__(self,string):
        [n,first_num,operators,cages] = self.split(string)
        self.n = n
        num_of_cages = len(cages)
        num_of_variables = n*n;
        self.variables = [i for i in range(num_of_variables)]
        self.domains = {var: [i+1 for i in range(n)] for var in self.variables}
        self.Cages = []
        for i in range(num_of_cages):
            self.Cages.append(CAGE(cages[i],operators[i],first_num[i]))
        self.neighbors = {var: self.same_cols_vars(var) + self.same_rows_vars(var) for var in self.variables}
        for var in self.variables:
            for cage in self.Cages:
                if var in cage.getVars():
                    self.neighbors[var] = self.neighbors[var] + cage.get_neighbours_by_cage(var)
        CSP.__init__(self,self.variables,self.domains,self.neighbors,self.f)
        self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
        for var in self.variables:
            self.neighbors[var] = list(dict.fromkeys(self.neighbors[var]))
        
    def split(self,string):
        lines = []
        with open(string,"r") as f:
            lines = [line.rstrip() for line in f]
        n = int(lines[0])
        lines.pop(0)
        first_num = []
        operators = []
        cages = []
        for str in lines:
            t = str.split('#', 1)[0]
            first_num.append(int(t))
            str =  str[len(t):]
            operators.append(str[len(str)-1])
            str = str[1:len(str)-2]
            full_number = ''
            tuple = ()
            for char in str:
                if char != '-':
                    full_number = full_number + char
                else:
                    tuple = tuple + (int(full_number),)
                    full_number = ''
            tuple = tuple + (int(full_number),)
            cages.append(tuple)
        return [n,first_num,operators,cages]
    
    def same_rows_vars(self,variable):
        rows = []
        for i in range(self.n):
            rows = self.variables[i*self.n:(i+1)*self.n]
            if (variable in rows):
                rows.remove(variable)
                return rows
                    
    def same_cols_vars(self,variable):
        for i in range(self.n):
            cols = []
            for j in range(0,self.n*self.n,self.n):
                cols.append(i+j)
            if (variable in cols):
                cols.remove(variable)
                return cols       
            
    def findCage(self, var):
        for cage in self.Cages:
            if var in cage.getVars():
                return cage
        
    def f(self,A, a, B, b):

        if (B in self.same_cols_vars(A) or B in self.same_rows_vars(A)) and a == b:
            return False

        Acage = self.findCage(A)
        Bcage = self.findCage(B)
        Aflag = True
        Bflag = True
        Acagevars = list(Acage.getVars())
        Bcagevars = list(Bcage.getVars())

        if len(Acagevars) == 1:
            Aflag = Acage.have_solution_eq(a)
        if len(Bcagevars) == 1:
            Bflag = Bcage.have_solution_eq(b)
        if len(Acagevars) == 1 or len(Bcagevars) == 1:
            return Aflag and Bflag

        if Acage == Bcage:
            Acagevars.remove(A)
            Acagevars.remove(B)
            if Acage.getOp() == '+':
                return Acage.has_solution_add_mul_eq(Acagevars, a + b, self.curr_domains)
            if Acage.getOp() == '*':
                return Acage.has_solution_add_mul_eq(Acagevars, a * b, self.curr_domains)
            if Acage.getOp() == '-':
                return Acage.has_solution_div_sub(Acagevars, a - b, self.curr_domains) or Acage.has_solution_div_sub(Acagevars, b - a, self.curr_domains)
            if Acage.getOp() == '/':
                return Acage.has_solution_div_sub(Acagevars, a/b, self.curr_domains) or Acage.has_solution_div_sub(Acagevars, b/a, self.curr_domains)
        return True

    def print_puzzle(self, puzzle):
        if puzzle == None:
            print("No solution found with this settings")
            return 0
        else:
            for i in range(self.n * self.n):
                if (i % (self.n) == 0):
                    print("")
                # print(puzzle)
                if i in puzzle:
                    print(str(puzzle[i]) + " ", end='')
                else:
                    print("x ", end='')
            print("\n")
            return 1
import time

#Solve problem
def solver(problems, algorithmn, select_unassigned_variable, inf=no_inference):
    #keep solved problems counter
    solved = 0
    #keep tuple with times and assigns
    return_list = []
    for i in range(len(problems)):
        #start time counter
        start_problem = time.time()
        AC3(problems[i])
        print("Solving Problem " +str(i) + " size " + str(problems[i].n) + "*" +str(problems[i].n))
        #solve and print puzzle
        solved+=problems[i].print_puzzle(algorithmn(problems[i],select_unassigned_variable, inference=inf))
        print("Asssigns = " + str(problems[i].nassigns))
        #end time counter
        end_problem = time.time()
        return_list.append((end_problem - start_problem,problems[i].nassigns))
        print(end_problem - start_problem)
    print("Solved "+str(solved)+"/"+str(len(problems)))
    print("Cpu Time = " + str(sum(return_list[0])) + " s")
    return return_list


def Solve_Problem_Min_Conflicts(problems):
    
    solved = 0 # Solved Problems Counter
    return_list = [] # tuple with Times and Assigns
    
    #print("Min_Conflicts Algorithm \n")

    for k in range(len(problems)):

        start_problem = time.time() # Start Timer
        AC3(problems[k])
        print("\n Solving Problem " +str(k) + " size " + str(problems[k].n) + "*" +str(problems[k].n))
        solved += problems[k].print_puzzle(min_conflicts(problems[k],100))
        print("Asssigns = " + str(problems[k].nassigns))
        end_problem = time.time() # End Timer
        return_list.append((end_problem - start_problem,problems[k].nassigns))
    print("Solved "+str(solved)+"/"+str(len(problems)))
    print("Cpu Time = " + str(sum(return_list[0])) + " s" + "\n")
    return return_list



#Main Programm

#Initialize problems
e1 = KenKen("Problems/Kenkel-3-easy");
# e2 = KenKen("Problems/Kenken-4-Hard.txt")
# e3 = KenKen("Problems/Kenken-5-Hard.txt")
# e4 = KenKen("Problems/Kenken-6-Hard.txt")
# e5 = KenKen("Problems/Kenken-7-Hard-1.txt")
# e6 = KenKen("Problems/Kenken-7-Hard-2.txt")
# e7 = KenKen("Problems/Kenken-8-Hard-1.txt")
# e8 = KenKen("Problems/Kenken-8-Hard-2.txt")
# e9 = KenKen("Problems/Kenken-9-Hard-1.txt")
# e10 = KenKen("Problems/Kenken-9-Hard-2.txt")
problems = [e1]#, e2, e3, e4, e5, e6, e7, e8, e9, e10]
#list contains a tuple with tie time and assigns of every problem
return_list = []
#run with forward_checking
return_list.append(solver(problems, backtracking_search, mrv, forward_checking))
#run without forward_checking
#return_list.append(solver(problems, backtracking_search, mrv))
#run with mac algorithm
return_list.append(solver(problems, backtracking_search, mrv, mac))
#minconficts
return_list.append(Solve_Problem_Min_Conflicts(problems))






#AYTA MPOREITE NA TA SVISETE KAI NA TA VALETE STO PDF THS THEORIAS TA APOTELESMATA



#print results
print("\nTime Table for all problems/algorithms")
print("    mrv/fc      mrv/mac     min_conflicts")

Total_times = 0
Total_assigns = 0
for i in range(len(problems)):
    print("e" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(return_list)):
        print(str('%.8f' % return_list[j][i][0]) + "s ", end='')
        Total_times += return_list[j][i][0]
    print("")
print("")
for i in range(len(problems)):
    print("e" + str(i + 1) + " ", end='')
    if i < len(problems) - 1: print(" ", end='')
    for j in range(len(return_list)):
        print(str(return_list[j][i][1]) + " assigns ", end='')
        Total_assigns += return_list[j][i][1]
    print("")
print("Total CPU Time : " +str(Total_times) + "s " )
print("Total assigns : " +str(Total_assigns) + " assigns " + "\n")


#trash
#solver(problems, backtracking_search, mac)
# print(backtracking_search(e))
# print(backtracking_search(e,select_unassigned_variable=mrv))
#print(backtracking_search(e1,select_unassigned_variable=mrv,inference=forward_checking))
# print(backtracking_search(e,select_unassigned_variable=mrv))
                
         
# e1 = KenKen("Problems/Kenkel-3-easy");
# e2 = KenKen("Problems/Kenken-4-Hard.txt")
# e3 = KenKen("Problems/Kenken-5-Hard.txt")
# e4 = KenKen("Problems/Kenken-6-Hard.txt")
# e5 = KenKen("Problems/Kenken-7-Hard-1.txt")
# e6 = KenKen("Problems/Kenken-7-Hard-2.txt")
# e7 = KenKen("Problems/Kenken-8-Hard-1.txt")
# e8 = KenKen("Problems/Kenken-8-Hard-2.txt")
# e9 = KenKen("Problems/Kenken-9-Hard-1.txt")
#e10 = KenKen("Problems/Kenken-9-Hard-2.txt")
# problems = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10]
# solver(problems,min_conflicts)
#AC3(e10)
#e10.print_puzzle(backtracking_search(e10,select_unassigned_variable=mrv,inference=forward_checking))
# print(backtracking_search(e,select_unassigned_variable=mrv))
# print(backtracking_search(e1,select_unassigned_variable=mrv,inference=forward_checking))
# print(backtracking_search(e,select_unassigned_variable=mrv))from csp import *
