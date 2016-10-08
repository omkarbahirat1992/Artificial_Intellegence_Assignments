'''
========================================================
KB in the from of object tree is created.
std_var() is implemented

implemented following and their requirements
unify()
unify_var()
substitute()
FOL_BC_OR()
FOL_BC_AND()
parse_definite_clause()
changed the __rshift__ to __gt__ due to priority issue
basic loging mechanism is implemented
working perfect with sample 1, 2 and 3

Done with handling of a QUERY consist of "&&" in it.

Done with handling of the CHUTYA case in tc 5.
Added "query count" check while reading the "input.txt"
========================================================
'''


import sys, re, itertools
log_list = []

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

    def fetch_rules_for_goal(self):
        return self.clauses


class OBJ:
    def __init__(self, str, *args):
        self.op = str
        self.args = map(make_object, args)
        self.t_flag = 0

    def __call__(self, *args):
        return OBJ(self.op, *args)

    def __and__(self, other):
        return OBJ("&", self, other)

    def __gt__(self, other):
        return OBJ(">", self, other)
    
    def __hash__(self):
        return hash(self.op) ^ hash(tuple(self.args))

    def __eq__(self, other):
        return (other is self) or (isinstance(other, OBJ)
            and self.op == other.op and self.args == other.args)

    def __repr__(self):
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
    s = s.replace(" => ", " > ")
    
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'OBJ("\1")', s)

    return eval(s, {'OBJ':OBJ})

def prepare_KB_n_Query_from_file(file_name):
    fol_kb = None

    fp = open(file_name, "r")
 
    query = fp.readline()
    count = (int)(fp.readline())

    clause_list = []
    for line in fp:
        if count == 0: break
        clause_list.append(line)
        count = count - 1

    fp.close()

    return FOL_KB(query, map(make_object, clause_list)), query

def is_symbol(stmt):
    return isinstance(stmt, str) and stmt[0].isalpha()

def is_var_symbol(stmt):
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

def break_apart(op, args):
    """Given an associative op, return a flattened list result such
    that OBJ(op, *result) means the same as OBJ(op, *args)."""
    result = []
    def collect(subargs):
        for arg in subargs:
            if arg.op == op: collect(arg.args)
            else: result.append(arg)
    collect(args)
    return result

def make_conjunct_list(stmt_OBJ):
    return break_apart('&', [stmt_OBJ])


def unify(rhs, goal, theta):
    if theta is None:
        return None

    elif rhs == goal:
        return theta

    elif is_variable(rhs):
        return unify_var(rhs, goal, theta)

    elif is_variable(goal):
        return unify_var(goal, rhs, theta)

    elif isinstance(rhs, OBJ) and isinstance(goal, OBJ):
        return unify(rhs.args, goal.args, unify(rhs.op, goal.op, theta))

    elif isinstance(rhs, str) or isinstance(goal, str):
        return None

    elif is_list(rhs) and is_list(goal) and len(rhs) == len(goal):
         if not rhs: 
            return theta
         return unify(rhs[1:], goal[1:], unify(rhs[0], goal[0], theta))
    else:
        return None


def is_list(x):
    return hasattr(x, '__getitem__')


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif occur_check(var, x, theta):
        return None
    else:
        return add_to_theta(theta, var, x)


def add_to_theta(theta, var, val):
    temp_theta = theta.copy()
    temp_theta[var] = val
    return temp_theta


"""Return True if variable var occurs anywhere in x
(or in substitute(theta, x), if theta has a binding for x)."""
def occur_check(var, x, theta):
    if var == x:
        return True

    elif is_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)

    elif isinstance(x, OBJ):
        return (occur_check(var, x.op, theta) or
                occur_check(var, x.args, theta))

    elif isinstance(x, (list, tuple)):
        return some(lambda element: occur_check(var, element, theta), x)

    else:
        return False


def some(predicate, seq):
    for x in seq: 
        px = predicate(x)
        if  px: return px
    return False


def is_variable(x):
    return isinstance(x, OBJ) and not x.args and is_var_symbol(x.op)


def substitute(theta, x):
    if isinstance(x, list):
        return [substitute(theta, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([substitute(theta, xi) for xi in x])
    elif not isinstance(x, OBJ):
        return x
    elif is_var_symbol(x.op):
        return theta.get(x, x)
    else:
        return OBJ(x.op, *[substitute(theta, arg) for arg in x.args])


def parse_definite_clause(rule_OBJ):
    if is_symbol(rule_OBJ.op):
        return [], rule_OBJ
    else:
        antecedent, consequent = rule_OBJ.args
        return make_conjunct_list(antecedent), consequent


def write_log(log, str_OBJ=None, theta={}):
    global log_list
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
            else:
                log_str += obj.op + ", "
        log_str = re.sub(', $', ')', log_str)
    log_list.append("%s\r\n" % log_str)


def FOL_BC_AND(KB, goals, theta):
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for theta1 in FOL_BC_OR(KB, substitute(theta, first), theta):
            for theta2 in FOL_BC_AND(KB, rest, theta1):
                yield theta2


def all_var_grounded(goal):
    for obj in goal.args:
        if is_variable(obj):
            return False
    return True


def all_var_in_theta(goal, theta):
    if not all_var_grounded(goal):
        if theta == None:
            return False
    for obj in goal.args:
        if is_variable(obj):
            if not theta.has_key(obj):
                return False
    return True


def FOL_BC_OR(KB, goal, theta):
    prev_attempt = False
    false_attempt = True
    not_present_in_KB = True

    for rule in KB.fetch_rules_for_goal():
        lhs, rhs = parse_definite_clause(std_var(rule))

        if goal.op != rhs.op: 
            continue
        not_present_in_KB = False

        if not prev_attempt and all_var_grounded(goal):
            prev_attempt = True
            write_log("Ask", goal, theta)

        temp_theta = unify(rhs, goal, theta)
        if temp_theta == None:
            continue

        if not all_var_grounded(goal):
            write_log("Ask", goal, theta)

        false_attempt = True
        
        for theta1 in FOL_BC_AND(KB, lhs, temp_theta):
            false_attempt = False

            if all_var_in_theta(goal, theta1):
                write_log("True", goal, theta1)

            yield theta1 

        if false_attempt:
            prev_attempt = False

    if false_attempt:
        if not all_var_grounded(goal) or not_present_in_KB:
            write_log("Ask", goal, theta)
        write_log("False", goal, theta)

    
def FOL_BC_FIRE_QUERY(KB, query):
 
    query_obj = make_object(query)
    goal_list = make_conjunct_list(query_obj)
    
    log = "True"
    for goal in goal_list:
        try:
            theta = FOL_BC_OR(KB, goal, {}).next()
            if not all_var_in_theta(goal, theta):
                log = "False"
                break
        except:
            log = "False"
            break
    write_log(log)


def write_log_output_file():
    global log_list
    fp = open("output.txt", "w")
    for log in log_list:
        fp.write(log)
    fp.close()


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
    
    FOL_BC_FIRE_QUERY(fol_kb, query)
    write_log_output_file()

if __name__ == "__main__":
    main(sys.argv[1:])
