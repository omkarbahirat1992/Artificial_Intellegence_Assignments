'''
========================================================
KB in the from of object tree is created.
std_var() is implemnted
========================================================
'''


import sys, re, itertools
from my_utils import *


def reset_ouput_file():
    fp = open("ouput.txt", "w")
    fp.close()

class FOL_KB:
    def __init__(self, query, clause_list = []):
        self.query = query 
        self.clauses = []
        for clause in clause_list:
            self.tell(clause)

    def tell(self, sentence):
        self.clauses.append(sentence)

    #TODO: try to make it goal specific
    def fetch_rules_for_goal(self):
        return self.clauses


class OBJ:
    def __init__(self, str, *args):
        self.op = str
        self.args = map(make_object, args)
        self.t_flag = 0

    def __call__(self, *args):
        #assert is_symbol(self.op) and not self.args
        return OBJ(self.op, *args)

    def __and__(self, other):
        return OBJ("&", self, other)

    def __invert__(self):
        return OBJ("~", self)
    
    def __rshift__(self, other):
        return OBJ(">>", self, other)
    
    def __hash__(self):
        #print "====================== in hash =================="
        "Need a hash method so Exprs can live in dicts." 
        return hash(self.op) ^ hash(tuple(self.args))

    def __eq__(self, other):
        """x and y are equal iff their ops and args are equal."""
        return (other is self) or (isinstance(other, OBJ)
            and self.op == other.op and self.args == other.args)

    def __repr__(self):
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)'"
        if not self.args:         # Constant or proposition with arity 0
            return str(self.op)
        elif is_symbol(self.op):  # Functional or propositional operator
            return '%s(%s)' % (self.op, ', '.join(map(repr, self.args)))
        elif len(self.args) == 1: # Prefix operator
            return self.op + repr(self.args[0])
        else:                     # Infix operator
            return '(%s)' % (' '+self.op+' ').join(map(repr, self.args))


def make_object(s):
    if isinstance(s, OBJ):
        return s
    
    if isinstance(s, int):
        return OBJ(s)

    s = s.replace(" && ", " & ")
    s = s.replace(" => ", " >> ")
    
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'OBJ("\1")', s)

    return eval(s, {'OBJ':OBJ})

def prepare_KB_n_Query_from_file(file_name):
    fol_kb = None
    print "in read_input_file()"

    fp = open(file_name, "r")
 
    query = fp.readline()
    count = fp.readline()

    clause_list = []
    for line in fp:
         clause_list.append(line)

    fp.close()

    return FOL_KB(query, map(make_object, clause_list)), query

def is_symbol(stmt):
    return isinstance(stmt, str) and stmt[0].isupper()

def is_variable(stmt):
    #print stmt
    return isinstance(stmt, str) and stmt[0].islower() and len(stmt) == 1
''' 
   if isinstance(stmt, str): print "isinstance str"
    if stmt[0].islower(): print "islower"
    if len(stmt) == 1: print "len is 1"
'''

def std_var(stmt, book = None):
    #print "in std_var"
    if book == None:
        book = {}
    
    if not isinstance(stmt, OBJ):
        #print "in std_var: not isisntance"
        return stmt


    if is_variable(stmt.op):
        #print "is_variable"
        if stmt in book:
            #print "in book"
            return book[stmt]
        else:
            #print "not in book"
            val_obj = OBJ("V%d" %std_var.counter.next())
            #print "returning not in book"
            book[stmt] = val_obj
            print book
            #print "returning not in book"
            return val_obj

    else:
        #print "about to return"
        return OBJ(stmt.op, *[std_var(rule, book) for rule in stmt.args])

std_var.counter = itertools.count()

def FOL_BC_OR(KB, goal, theta):
    for rule in KB.fetch_rules_for_goal:
        pass #lhs, rhs = 
        

#TODO: Think about the query with multiple predicates
def FOL_BC_ASK(KB, query):
    #print "in FOL_BC_ASK()"
    #display_kb(KB, query)
    return FOL_BC_OR(KB, query, {})
    pass


def main(argv):
    fol_kb = None
    query = ' '
    file_name = ' '
    try:
        if (argv[0] == '-i'):
            file_name = argv[1]
        else:
            sys.exit(2)
    except:
        print '<filename>.py -i <inputfile>'
        sys.exit(2)
    
    reset_ouput_file()
    fol_kb, query = prepare_KB_n_Query_from_file(file_name)
    
    for rule in fol_kb.fetch_rules_for_goal():
        std_var(rule)

#   FOL_BC_ASK(fol_kb, query)
    
#    display_kb_tree(fol_kb, query)
#    display_kb(fol_kb, query)



if __name__ == "__main__":
    main(sys.argv[1:])




















'''
Algo:
    Read input file
   line 1): parse the query (it'll have atmost one unknown variable) (if && is in query then there is no unknown variable)
        find type of query (there are total 3 type of queries)
        keep count of facts as per type
    
   line 2): count of number of cluauses 'n'
   line 3 to 2+n): n clauses (each of either of 2 types specified in pdf)

    find a value for queried variable "x". or make the replacement of queried value in KB predicate.

NOTE:=
1) can we change the order of claueses given in input file: NO
2) prevent from infinite loop, as backward chaining can get into one
3) All implication have atmost 5 predicates on its left.
4) each predicate have (1 to 3), both inclusive, arguments.
5) Variable are specified by "single lower case letter"
6) Predicates are specified by "Upper camel letter" (at max 20 letter)

7) if you come accross ~(predicate) with unresolved unknown variable then something went wrong

QUESTIONS:

3) How to differentiate between a "variable" and a "value"?


'''
