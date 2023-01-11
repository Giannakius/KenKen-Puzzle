import time
from csp import *

class Cage :

    # Intialize Cage
    def __init__(self, variables, op, result):
        self.variables = variables
        self.operator = op
        self.result = result
    
    # If Cage has Solution the value "value"
    def Have_Solution(self,value):
        if value == self.result :
            return True
        else:
            return False

    # Get the neighbours of the Cage
    def Get_Neighbours(self,var):
        temp_var = list(self.variables)
        temp_var.remove(var)
        return temp_var


    # If the Multiply or the Add proposal Has Solution return True
    def Add_Multiply_Has_Solution(self, remain_var, curr_val, currdomains):
        if len(remain_var) == 0:
            return curr_val == self.result

        for value in currdomains[remain_var[0]]:
            if self.operator == '+':
                new_value = value + curr_val
            elif self.operator == '*':
                new_value = value * curr_val
            
            if self.Add_Multiply_Has_Solution(remain_var[1:], new_value, currdomains) == True:  
                return True
        return False
    
    # If the Subtraction or the division proposal Has Solution return True
    def Div_Sub_Has_Solution(self, var, curr_val, currdoms):
        if len(var) == 0:
            if self.operator == '-':
                return curr_val == self.result
            if self.operator == '/':
                return curr_val == float(self.result)
        else:
            for value in currdoms[var[0]]:
                if self.operator == '-':
                    return value - curr_val == self.result or curr_val - value == self.result
                if self.operator == '/':
                    
                    a1 = value == self.result
                    a2 = curr_val == self.result
                    
                    if value == 0:
                        return a1
                    elif curr_val == 0:
                        return a2
                    else:
                        return value / curr_val == self.result or curr_val / value == self.result



class KenKen (CSP) :

    # Intialize KenKen Problem
    def __init__(self,string):
        [n,first_num,operators,cages] = self.split(string)
        self.n = n

        self.variables = [x for x in range(n*n)]
        self.domains = {var: [x+1 for x in range(n)] for var in self.variables}
        self.Cages = []
        
        for x in range(len(cages)):
            self.Cages.append(Cage(cages[x],operators[x],first_num[x]))
        
        self.neighbors = {var: self.same_cols_vars(var) + self.same_rows_vars(var) for var in self.variables}
        
        for var in self.variables:
            for cage in self.Cages:
                if var in cage.variables:
                    self.neighbors[var] = self.neighbors[var] + cage.Get_Neighbours(var)
        
        CSP.__init__(self,self.variables,self.domains,self.neighbors,self.Constraits)
        
        self.curr_domains = {v: list(self.domains[v]) for v in self.variables}
        
        for var in self.variables:
            self.neighbors[var] = list(dict.fromkeys(self.neighbors[var]))
    
    
    # returns the n and 3 tuples
    def split(self,string):
        lines = []
        first_num = []
        operators = []
        cages = []
        
        with open(string,"r") as Constraits:
            lines = [line.rstrip() for line in Constraits]

        n = int(lines[0])
        lines.pop(0)
        
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

        # n = μεγεθος προβληματος
        # first_num ειναι λιστα με τα αποτελεσματα των πραξεων ενος cage
        # operators ειναι μια λιστα με τα operators (δεξια δεξια)
        # cages ειναι μια λιστα με ολες τις ενδιαμεσες τιμες

        return [n,first_num,operators,cages]
    
    # παιρνει ως ορισμα μια μεταβλητη και επιστρεφει μια λιστα με τις μεταβλητες που βρισκονται στην ιδια ΓΡΑΜΜΗ με αυτη
    def same_rows_vars(self,variable):
        rows = []
        for x in range(self.n):
            rows = self.variables[x*self.n:(x+1)*self.n]
            if (variable in rows):
                rows.remove(variable)
                return rows

    # παιρνει ως ορισμα μια μεταβλητη και επιστρεφει μια λιστα με τις μεταβλητες που βρισκονται στην ιδια ΣΤΗΛΗ με αυτη             
    def same_cols_vars(self,variable):
        for x in range(self.n):
            cols = []
            for k in range(0,self.n*self.n,self.n):
                cols.append(x+k)
            if (variable in cols):
                cols.remove(variable)
                return cols       
            
    def Find_Cage(self, var):
        for cage in self.Cages:
            if var in cage.variables:
                return cage
    


    # Επιστρεφει False αν μετα την αναθεση τιμων a στο Α και b στο Β δεν ικανοποιειται τουλαχιστον ενας περιορισμος

    def Constraits(self,A, a, B, b):

        if (B in self.same_cols_vars(A) or B in self.same_rows_vars(A)) and a == b:
            return False
        
        Aflag = True
        Bflag = True
        Acage = self.Find_Cage(A)
        Bcage = self.Find_Cage(B)
        
        Acagevars = list(Acage.variables)
        Bcagevars = list(Bcage.variables)


        if len(Acagevars) == 1:
            Aflag = Acage.Have_Solution(a)
        if len(Bcagevars) == 1:
            Bflag = Bcage.Have_Solution(b)
        if len(Acagevars) == 1 or len(Bcagevars) == 1:
            return (Aflag and Bflag)

        if Acage == Bcage:
            Acagevars.remove(A)
            Acagevars.remove(B)

            if Acage.operator == '+':
                return Acage.Add_Multiply_Has_Solution(Acagevars, a + b, self.curr_domains)
            if Acage.operator == '*':
                return Acage.Add_Multiply_Has_Solution(Acagevars, a * b, self.curr_domains)
            if Acage.operator == '-':
                return Acage.Div_Sub_Has_Solution(Acagevars, a - b, self.curr_domains) or Acage.Div_Sub_Has_Solution(Acagevars, b - a, self.curr_domains)
            if Acage.operator == '/':
                return Acage.Div_Sub_Has_Solution(Acagevars, a/b, self.curr_domains) or Acage.Div_Sub_Has_Solution(Acagevars, b/a, self.curr_domains)
        
        return True

    def Print_Puzzle(self, puzzle):
        if puzzle == None:
            print("No solution found with this settings")
            return 0
        else:
            return 1



# Solve problem
def Problem_Solver(problems, algorithmn, select_unassigned_variable, inf=no_inference):

    Solved_Problems_counter = 0 
    return_list = []    #Tuple with times and assigns

    for k in range(len(problems)):

        start_problem = time.time() # Start Timer
        AC3(problems[k])
        Solved_Problems_counter+=problems[k].Print_Puzzle(algorithmn(problems[k],select_unassigned_variable, inference=inf))
        end_problem = time.time()   # End Timer
        return_list.append((end_problem - start_problem,problems[k].nassigns))

    return return_list


def Solve_Problem_Min_Conflicts(problems):
    
    Solved_Problems_counter = 0 # Solved Problems Counter
    return_list = [] # tuple with Times and Assigns

    for k in range(len(problems)):

        start_problem = time.time() # Start Timer
        AC3(problems[k])
        Solved_Problems_counter += problems[k].Print_Puzzle(min_conflicts(problems[k],100))

        end_problem = time.time() # End Timer
        return_list.append((end_problem - start_problem,problems[k].nassigns))

    return return_list



#Main Programm

#Initialize problems

problems = []
for x in range(9): problems.append(KenKen("Problems/Kenken-"+str(x+1)+".txt"))

#list contains a tuple with tie time and assigns of every problem
return_list = []

#Run with Forward_Checking
return_list.append(Problem_Solver(problems, backtracking_search, mrv, forward_checking))

#Run without Forward_Checking
#return_list.append(Problem_Solver(problems, backtracking_search, mrv))

#Run with Mac Algorithm
return_list.append(Problem_Solver(problems, backtracking_search, mrv, mac))

#Run with Min_Conflict
#return_list.append(Solve_Problem_Min_Conflicts(problems))


print("               MRV/FC           MRV/MAC        Min_Conficts")

Total_times = 0
Total_assigns = 0
for x in range(len(problems)):
    print("Problem :" + str(x + 1) + " ", end='')
    if x < len(problems) - 1: print(" ", end='')
    for k in range(len(return_list)):
        print(str('%.8f' % return_list[k][x][0]) + " sec | ", end='')
        Total_times += return_list[k][x][0]
    print("")
print("")
for x in range(len(problems)):
    print("Problem :" + str(x + 1) + " ", end='')
    if x < len(problems) - 1: print(" ", end='')
    for k in range(len(return_list)):
        print(str(return_list[k][x][1]) + " assigns ", end='')
        Total_assigns += return_list[k][x][1]
    print("")


