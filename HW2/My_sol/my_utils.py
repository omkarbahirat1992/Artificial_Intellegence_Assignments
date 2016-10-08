from hw2cs561s16 import *

def display_kb(KB, query):
    print "\n========================================"
    print "Given Query is:"
    print query
    print "========================================"
    print "Given KB is:"
    print "========================================"
    for rule in KB.fetch_rules_for_goal():
        print(rule)
    print "========================================"




def replace_string(s):
    print "before replace :%s" % s
    s = s.replace("&&", "&")
    s = s.replace(" => ", " >> ") 
    print "after replace :%s" % s



'''
==========================================================================================
To see the result need to move below two function into the main file
'''

def display_kb_tree(KB, query): 
    for rule in KB.fetch_rules_for_goal():
        #print "in tree"
        #if isinstance(rule, OBJ):
            #print "isinstance"
        print display_rule_tree(rule, ' ' + rule.op + ' ')
        #print display_rule_tree(rule, ' ')
'''   
        display_rule_tree(rule.args[0], ' ' + rule.args[0].op + ' ')
        display_rule_tree(rule.args[1], ' ' + rule.args[1].op + ' ')
        display_rule_tree(rule.args[0].args[0], ' ' + rule.args[0].args[0].op + ' ')
        display_rule_tree(rule.args[1].args[0], ' ' + rule.args[1].args[0].op + ' ')
        display_rule_tree(rule.args[1].args[1], ' ' + rule.args[1].args[1].op + ' ')
'''  


def display_rule_tree(obj_rule, str):
    final_str = ' '
    for obj in obj_rule.args:
        #print "pushinig %s" %obj.op 
        final_str = ' ' + display_rule_tree(obj, obj.op) 
        if (obj_rule.t_flag == 0):
            obj_rule.t_flag = 1
            str = final_str + ' ' + str 
        else:   
            str += final_str + ' '

    #print "returning %s" %str
    return str

#==========================================================================================








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
4) can given sentence contain number?

'''
