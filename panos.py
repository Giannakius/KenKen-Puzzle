import operator
from csp import *
import time

oper_dict = { '+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '=': None }

class CAGE :
    def __init__(self, Temp_variables, Temp_Oper, Temp_Result):
        self.variables = Temp_variables
        self.op = Temp_Oper
        self.result = Temp_Result

    def has_solution_add_mul_eq(self, remain_var, curr_val, currdomains):
        if len(remain_var) == 0:
            return curr_val == self.result
        for value in currdomains[remain_var[0]]:
            oper = oper_dict[self.op]
            if oper == '+' or oper == "*":
                boolvar = self.has_solution_add_mul_eq(remain_var[1:], oper(value, curr_val), currdomains)
                if boolvar == True:
                    return True
        return False

    def has_solution_div_sub(self, var, curr_val, currdoms):
        oper = oper_dict[self.op]
        if len(var) == 0:
            if oper == '-':
                return curr_val == self.result
            if oper == '/':
                return curr_val == float(self.result)
        else:
            for value in currdoms[var[0]]:
                if oper == '-':
                    return value - curr_val == self.result or curr_val - value == self.result
                if oper == '/':
                    if value == 0:
                        return value == self.result
                    elif curr_val == 0:
                        return curr_val == self.result
                    else:
                        return value / curr_val == self.result or curr_val / value == self.result

class kenken (CSP) :
    def __init__(self,string):
        [n,first_num,operators,cages] = self.split(string)
        self.n = n
        self.variables = [i for i in range(n*n)]
        self.domains = {var: [i+1 for i in range(n)] for var in self.variables}
        self.Cages = [CAGE(cages[i],operators[i],first_num[i]) for i in range(len(cages))]
        self.neighbors = {var: self.same_cols_vars(var) + self.same_rows_vars(var) for var in self.variables}
        CSP.__init__(self,self.variables,self.domains,self.neighbors,self.f)
        self.curr_domains = {v: list(self.domains[v]) for v in range(n*n)}
        self.neighbors = [list(dict.fromkeys(self.neighbors[var])) for var in self.variables]


    def split(self,string):
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
        for i in range(self.n):
            rows = self.variables[i*self.n:(i+1)*self.n]
            if (variable in rows):
                rows.remove(variable)
                return rows

    def same_rows_vars(self, variable):
        rows = []
        for i in range(self.n):
            rows = self.variables[i * self.n:(i + 1) * self.n]
            if (variable in rows):
                rows.remove(variable)
                return rows

    def same_cols_vars(self, variable):
        for i in range(self.n):
            cols = []
            for j in range(0, self.n * self.n, self.n):
                cols.append(i + j)
            if (variable in cols):
                cols.remove(variable)
                return cols

    def findCage(self, var):
        for cage in self.Cages:
            if var in cage.variables:
                return cage
    def f(self,A, a, B, b):
        if (B in self.same_cols_vars(A) or B in self.same_rows_vars(A)) and a == b: return False
        Acage = self.findCage(A); Acagevars = list(Acage.variables); Aflag = True
        Bcage = self.findCage(B); Bcagevars = list(Bcage.variables); Bflag = True
        if len(Acagevars) == 1:
            Aflag = a == Acage.result
        if len(Bcagevars) == 1:
            Bflag = b == Bcage.result
        if len(Acagevars) == 1 or len(Bcagevars) == 1:
            return Aflag and Bflag
        if Acage == Bcage:
            Acagevars.remove(A)
            Acagevars.remove(B)
            oper = oper_dict[Acage.op]
            if oper == '+' or oper == '*':
                return Acage.has_solution_add_mul_eq(Acagevars, oper(a,b), self.curr_domains)
            elif oper == '-' or oper == '/':
                return Acage.has_solution_div_sub(Acagevars, oper(a,b), self.curr_domains) or Acage.has_solution_div_sub(Acagevars, oper(a,b), self.curr_domains)
        return True

    def print_puzzle(self, puzzle):
        if puzzle == None:
            print("No solution found with this settings")
            return 0
        else :
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

def solver(problems, algorithmn, select_unassigned_variable, inf=no_inference):
    solved = 0
    promlem_times = []
    print("Settings : \n" + "select_unassigned_variable = " + str(select_unassigned_variable) + "\ninference = " + str(inf))
    for i in range(len(problems)):
        start_problem = time.time()
        AC3(problems[i])
        print("Solving Problem " +str(i) + " size " + str(problems[i].n) + "*" +str(problems[i].n))
        solved+=problems[i].print_puzzle(algorithmn(problems[i],select_unassigned_variable, inference=inf))
        print("Asssigns = " + str(problems[i].nassigns))
        end_problem = time.time()
        promlem_times.append(end_problem - start_problem)
        print(end_problem - start_problem)
    print("Solved "+str(solved)+"/"+str(len(problems)))
    print("Cpu Time = " + str(sum(promlem_times)) + " s")
    return promlem_times

def solver_min_conflicts(problems):
    solved = 0
    promlem_times = []
    print("Settings : min_conflicts \n")
    for i in range(len(problems)):
        start_problem = time.time()
        AC3(problems[i])
        print("Solving Problem " +str(i) + " size " + str(problems[i].n) + "*" +str(problems[i].n))
        solved += problems[i].print_puzzle(min_conflicts(problems[i]))
        print("Asssigns = " + str(problems[i].nassigns))
        end_problem = time.time()
        promlem_times.append(end_problem - start_problem)
    print("Solved "+str(solved)+"/"+str(len(problems)))
    print("Cpu Time = " + str(sum(promlem_times)) + " s")
    return promlem_times

e1 = kenken("rqeyqs_folder/Kenkel-3-easy");
e2 = kenken("rqeyqs_folder/Kenken-4-Hard.txt")
e3 = kenken("rqeyqs_folder/Kenken-5-Hard.txt")
e4 = kenken("rqeyqs_folder/Kenken-6-Hard.txt")
e5 = kenken("rqeyqs_folder/Kenken-7-Hard-1.txt")
e6 = kenken("rqeyqs_folder/Kenken-7-Hard-2.txt")
e7 = kenken("rqeyqs_folder/Kenken-8-Hard-1.txt")
e8 = kenken("rqeyqs_folder/Kenken-8-Hard-2.txt")
e9 = kenken("rqeyqs_folder/Kenken-9-Hard-1.txt")
e10 = kenken("rqeyqs_folder/Kenken-9-Hard-2.txt")
problems = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]



#trash
#solver(problems, backtracking_search, mac)
# print(backtracking_search(e))
e2.print_puzzle(backtracking_search(e2,select_unassigned_variable=mrv))

#print(backtracking_search(e1,select_unassigned_variable=mrv,inference=forward_checking))
# print(backtracking_search(e,select_unassigned_variable=mrv))