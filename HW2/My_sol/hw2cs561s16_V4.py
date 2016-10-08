'''
========================================================
KB in the from of object tree is created.
std_var() is implemented

implemented following and their requirements
Unify()
unify_var()
subt()
FOL_BC_OR()
FOL_BC_AND()
parse_definite_clause()
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
        "Need a hash method so OBJ can live in dicts." 
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
    if book == None:
        book = {}
    
    if not isinstance(stmt, OBJ):
        return stmt

    if is_variable(stmt.op):
        if stmt in book:
            return book[stmt]
        else:
            val_obj = OBJ("V%d" %std_var.counter.next())
            book[stmt] = val_obj
            #print book
            return val_obj

    else:
        return OBJ(stmt.op, *[std_var(rule, book) for rule in stmt.args])

std_var.counter = itertools.count()

#______________________________________________________________________________
def dissociate(op, args):
    """Given an associative op, return a flattened list result such
    that OBJ(op, *result) means the same as OBJ(op, *args)."""
    result = []
    def collect(subargs):
        for arg in subargs:
            if arg.op == op: collect(arg.args)
            else: result.append(arg)
    collect(args)
    return result

def conjuncts(s):
    """Return a list of the conjuncts in the sentence s.
    >>> conjuncts(A & B)
    [A, B]
    >>> conjuncts(A | B)
    [(A | B)]
    """
    return dissociate('&', [s])
#=================================================================================#

#______________________________________________________________________________

def unify(x, y, s):
    """Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. OBJ('x')), constants, lists, or OBJ. [Fig. 9.1]
    >>> ppsubst(unify(x + y, y + C, {}))
    {x: y, y: C}
    """
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, OBJ) and isinstance(y, OBJ):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x: return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None

def is_variable(x):
    "A variable is an OBJ with no args and a lowercase symbol as the op."
    return isinstance(x, OBJ) and not x.args and is_var_symbol(x.op)


def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif occur_check(var, x, s):
        return None
    else:
        return extend(s, var, x)

def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, OBJ):
        return (occur_check(var, x.op, s) or
                occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return some(lambda element: occur_check(var, element, s), x)
    else:
        return False


def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val;
    return copy.
    >>> ppsubst(extend({x: 1}, y, 2))
    {x: 1, y: 2}
    """
    s2 = s.copy()
    s2[var] = val
    return s2

def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, OBJ):
        return x
    elif is_var_symbol(x.op):
        return s.get(x, x)
    else:
        return OBJ(x.op, *[subst(s, arg) for arg in x.args])


#=================================================================================#

def parse_definite_clause(s):
    "Return the antecedents and the consequent of a definite clause."
    #assert is_definite_clause(s)
    if is_symbol(s.op):
        return [], s
    else:
        antecedent, consequent = s.args
        return conjuncts(antecedent), consequent

def FOL_BC_AND(KB, goals, theta):
    print "in fol_bc_and: goals: %s" % goals
    #print "in fol_bc_and: theta: %s" % theta
    if theta is None:
        pass
    elif not goals:
        #print "in fol_bc_and: not_goals theta: %s" % theta
        #print "in fol_bc_and: not_goals: goals: %s" % goals
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        #print "in fol_bc_and: first: %s" % goals[0]
        #print "in fol_bc_and: rest: %s" % goals[1]
        for theta1 in fol_bc_or(KB, subst(theta, first), theta):
            for theta2 in fol_bc_and(KB, rest, theta1):
                yield theta2

def FOL_BC_OR(KB, goal, theta):
    #print "in FOL_BC_OR"
    for rule in KB.fetch_rules_for_goal():
        lhs, rhs = parse_definite_clause(std_var(rule))
        print "in fol_bc_or: rule: %s" % rule
        #print "in fol_bc_or: lhs: %s" % lhs
        #print "in fol_bc_or: rhs: %s" % rhs
        #print "_____________________________________________"
        for theta1 in FOL_BC_AND(KB, lhs, unify(rhs, goal, theta)):
            print theta1
            yield theta1


#TODO: Think about the query with multiple predicates
def FOL_BC_ASK(KB, query):
    #print "in FOL_BC_ASK()"
    #display_kb(KB, query)
    print "in FOL_BC_ASK"
    for obj in FOL_BC_OR(KB, query, {}):
        print "HI %s" % obj
    print "in FOL_BC_ASK end"
    #return FOL_BC_OR(KB, query, {})
    #pass


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
    
#    for rule in fol_kb.fetch_rules_for_goal():
#        std_var(rule)

    FOL_BC_ASK(fol_kb, query)
    
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
