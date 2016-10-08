import sys
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
        self.op = op
        args = prepare_object(args)

    def __call__(self, *args):
        return STD_Query(self.op, args)

    def __and__(self, other):
        return STD_Query("&", self, other)

    def __invert__(self):
        return STD_Query("~", self)
    
    def __rshift__(self, other):
        return STD_Query(">>", self, other)

def prepare_object(s):
    if isinstance(s, OBJ):
        return s

    print "before replace %s:" % s
    s.replace(" && ", " & ")
    s.replace(" => ", " >> ")
    print "after replace %s:" % s
    
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
 #       print line

    fp.close()

    return FOL_KB(query, map(prepare_object, clause_list)), query

def FOL_BC_OR(KB, goal, theta):
    for rule in KB.fetch_rules_for_goal:
        pass #lhs, rhs = 
        

#TODO: Think about the query with multiple predicates
def FOL_BC_ASK(KB, query):
    #print "in FOL_BC_ASK()"
    #display_kb(KB, query)
    return FOL_BC_OR(KB, query, {})
    pass

def replace_string(s)
    print "before replace %s:" % s
    s.replace(" && ", " & ")
    s.replace(" => ", " >> ")
    print "after replace %s:" % s

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

'''    
    reset_ouput_file()
    fol_kb, query = prepare_KB_n_Query_from_file(file_name)
    
    FOL_BC_ASK(fol_kb, query)
    
 #   display_kb(fol_kb, query)
'''

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
