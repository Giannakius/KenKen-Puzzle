from csp import *

class KenKen(CSP):
    def __init__(self, file):
        with open('easy.txt') as f: puzzle = f.readlines()
        splited = puzzle.split('#')
        n = int(splited[0])
        splited = splited[1:]
        self.cages = self.parsePuzzle(splited)
        self.RN = list(range(n))
        self.Cell = itertools.count().__next__
        self.bgrid = [[self.Cell() for x in self.RN] for y in self.RN]
        self.rows = self.bgrid  # rows are same as bgrid
        self.cols = list(zip(*self.bgrid))
        self.neighbors = {v: set() for v in sum(self.rows, [])}
        self.cages_vars = [cage.getVars() for cage in self.cages]
        for unit in map(set, self.rows + self.cols + self.cages_vars):
            for v in unit:
                self.neighbors[v].update(unit - {v})

        # Create a string = '1,2..N' where n*n is the size of the grid.
        possible_val = ''.join(str(v) for v in range(1, n + 1))
        # domains are initially all posible values i.e '1,2..N'
        self.domains = {var: possible_val for var in sum(self.rows, [])}
        CSP.__init__(self, None, self.domains, self.neighbors, self.KenKen_constraints)
        # Override CSP attribute curr_domains. Here, we definitely want to use it.
        self.curr_domains = {v: list(self.domains[v]) for v in sum(self.rows, [])}
