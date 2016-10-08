'''
========================================================
KB in the from of object tree is created.
std_var() is implemented

implemented following and their requirements
unify()
unify_var()
subst()
FOL_BC_OR()
FOL_BC_AND()
parse_definite_clause()
changed the __rshift__ to __gt__ due to priority issue
basic loging mechanism is implemented
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
#            print "in __init__: clause = %s$" %clause
            self.tell(clause)

    def tell(self, sentence):
        self.clauses.append(sentence)

    #TODO: try to make it goal specific
    def fetch_rules_for_goal(self):
        return self.clauses


class OBJ:
    def __init__(self, str, *args):
#        print "in __init__"
        self.op = str
        self.args = map(make_object, args)
        self.t_flag = 0

    def __call__(self, *args):
#       print "in __call__"
        #assert is_symbol(self.op) and not self.args
        return OBJ(self.op, *args)

    def __and__(self, other):
#        print "in and"
        return OBJ("&", self, other)

    def __gt__(self, other):
#        print "in gt"
        return OBJ(">", self, other)
    
    def __hash__(self):
        #print "====================== in hash =================="
        "Need a hash method so OBJ can live in dicts." 
        return hash(self.op) ^ hash(tuple(self.args))

    def __eq__(self, other):
#        print "in __eq__"
        """x and y are equal iff their ops and args are equal."""
        return (other is self) or (isinstance(other, OBJ)
            and self.op == other.op and self.args == other.args)

    def __repr__(self):
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)'"
#        print "in __repr__"
        if not self.args:         # Constant or proposition with arity 0
            return str(self.op)
        elif is_symbol(self.op):  # Functional or propositional operator
            return '%s(%s)' % (self.op, ', '.join(map(repr, self.args)))
        elif len(self.args) == 1: # Prefix operator
            return self.op + repr(self.args[0])
        else:                     # Infix operator
#            print " (%s)" % (' '+self.op+' ').join(map(repr, self.args))
            return '(%s)' % (' '+self.op+' ').join(map(repr, self.args))


def make_object(s):
    if isinstance(s, OBJ):
        return s
    
    if isinstance(s, int):
        return OBJ(s)

    s = s.replace(" && ", " & ")
    s = s.replace(" => ", " > ")
    
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'OBJ("\1")', s)
    #print "in make_objects: s = %s$" % s

    return eval(s, {'OBJ':OBJ})

def prepare_KB_n_Query_from_file(file_name):
    fol_kb = None
#    print "in read_input_file()"

    fp = open(file_name, "r")
 
    query = fp.readline()
    count = fp.readline()

    clause_list = []
    for line in fp:
         clause_list.append(line)

    fp.close()

    return FOL_KB(query, map(make_object, clause_list)), query

def is_symbol(stmt):
    return isinstance(stmt, str) and stmt[0].isalpha()

def is_var_symbol(stmt):
    #print stmt
    return is_symbol(stmt) and stmt[0].islower()

def std_var(stmt, book = None):
    if book == None:
        book = {}
    
    if not isinstance(stmt, OBJ):
        return stmt

    if is_var_symbol(stmt.op):
        if stmt in book:
            return book[stmt]
        else:
            val_obj = OBJ("v%d" %std_var.counter.next())
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

def unify(rhs, goal, theta):
    """Unify expressions rhs, goal with substitution theta; return a substitution that
    would make rhs, goal equal, or None if rhs, goal can not unify. rhs and goal can be
    variables (e.g. OBJ('rhs')), constants, lists, or OBJ. [Fig. 9.1]
    >>> ppsubst(unify(rhs + goal, goal + C, {}))
    {rhs: goal, goal: C}
    """
#    print "in Unify rhs = %s$" % rhs
#    print "in Unify goal = %s$" % goal
#    print "in Unify theta = %s$" % theta
    
    if theta is None:
#        print "in Unify returning None"
        return None

    elif rhs == goal:
#        print "in Unify: ======== rhs = goal ========="
        return theta

    elif is_variable(rhs):
#        print "in Unify: is_variable(rhs)"
        return unify_var(rhs, goal, theta)

    elif is_variable(goal):
#        print "===== in Unify: is_variable(goal) ======="
#        print "in Unify: rhs1 = %s" %rhs
#        print "in Unify: goal1 = %s" %goal
#        print "in Unify: theta1 = %s" %theta
        return unify_var(goal, rhs, theta)

    elif isinstance(rhs, OBJ) and isinstance(goal, OBJ):
#        print "in Unify: isinstance(rhs, OBJ) and isinstance(goal, OBJ)"
        return unify(rhs.args, goal.args, unify(rhs.op, goal.op, theta))

    elif isinstance(rhs, str) or isinstance(goal, str):
#        print "in Unify: isinstance(rhs, str) or isinstance(goal, str)"
        return None

    elif issequence(rhs) and issequence(goal) and len(rhs) == len(goal):
#        print "rhs[0] = %s" % rhs[0]
#        print "goal[0] = %s" % goal[0]
#        print "theta = %s" % theta
#        print rhs[1:]
  
         if not rhs: 
#            print "=========not rhs==============="
            return theta
         return unify(rhs[1:], goal[1:], unify(rhs[0], goal[0], theta))

    else:
#        print "in Unify: in else, returning none"
        return None

def issequence(x):
    return hasattr(x, '__getitem__')

def some(predicate, seq):
    for x in seq: 
        px = predicate(x)
        if  px: return px
    return False

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



def write_log(log, str_OBJ=None, theta={}):
    log_str = "%s: " % log
    if str_OBJ == None:
        log_str = log

    else:
        log_str +=  "%s(" % str_OBJ.op
        for obj in str_OBJ.args:
            if is_variable(obj):
                if theta.has_key(obj):
                    log_str += "%s, " % theta[obj]
                else:
                    log_str += "_, "
#                    print str_OBJ
#                    print theta
#                    log_str += obj.op + ", "
            else:
                log_str += obj.op + ", "
        log_str = re.sub(', $', ')', log_str)
    print "%s\r" % log_str

def FOL_BC_AND(KB, goals, theta):
    print "\n==========in fol_bc_and: goals: %s ===========" % goals
    print "in fol_bc_and: theta: %s" % theta
    if theta is None:
        print "in fol_bc_and: not_theta theta: %s" % theta
        #yield None
        pass
    elif not goals:
        print "in fol_bc_and: not_goals theta: %s" % theta
        print "in fol_bc_and: not_goals: goals: %s" % goals
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        print "in fol_bc_and: first: %s" % goals[0]
        print "in fol_bc_and: rest: %s" % goals[1:]
        for theta1 in FOL_BC_OR(KB, subst(theta, first), theta):
            for theta2 in FOL_BC_AND(KB, rest, theta1):
                write_log("True1", first, theta2)
                yield theta2
                write_log("False", first, theta2)

def FOL_BC_OR(KB, goal, theta):
    print "\n============in FRESH FOL_BC_OR. goal = %s=======" %goal

    # Need to ask the query again iff previous attempt was "False"
    # prev_attempt is said to be false if "ALL PREDICATES" in KB matching the "GOAL PREDICATE" turn out to be FALSE
  
    prev_attempt = False
    false_attempt = True

    for rule in KB.fetch_rules_for_goal():
        lhs, rhs = parse_definite_clause(std_var(rule))
        if goal.op != rhs.op: continue
        print "\n=======in fol_bc_or: rule==========: %s" % rule
        if not prev_attempt: 
            prev_attempt = True
            write_log("Ask", goal, theta)
        print "in fol_bc_or: goal: %s" % goal
        print "in fol_bc_or: lhs: %s" % lhs
        print "in fol_bc_or: rhs: %s" % rhs
        print "in fol_bc_or: theta: %s \n" % theta

        temp_theta = unify(rhs, goal, theta)
        if temp_theta == None:
            continue
        false_attempt = True

        attempt = False
        #TODO: pass "temp_theta" instead of "unify()"
        for theta1 in FOL_BC_AND(KB, lhs, unify(rhs, goal, theta)):
            print "$$$$$$$$$$FOL_BC_OR theta1 = %s$$$$$$" %theta1
            attempt = True
            write_log("True", goal, theta1)
            yield theta1 

        if not attempt:
            prev_attempt = False

    if false_attempt:
            pre_attempt = False
            write_log("False", goal, theta)

    
#TODO: Think about the query with multiple predicates
def FOL_BC_ASK(KB, query):
 
    query_obj = make_object(query)

    #print "in FOL_BC_ASK()"
    #display_kb(KB, query)
#    print "in FOL_BC_ASK"
    #for obj in FOL_BC_OR(KB, query_obj, {}):
    #    print "HI %s" % obj
#    print "in FOL_BC_ASK end"
    val = FOL_BC_OR(KB, query_obj, {})
#    print "in FOL_BC_ASK: returning val"
    return val
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

    log = "False"
    for obj in FOL_BC_ASK(fol_kb, query):
        log = "True"
    
    write_log(log)
    
#    print "This is output: %s" % FOL_BC_ASK(fol_kb, query)

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
