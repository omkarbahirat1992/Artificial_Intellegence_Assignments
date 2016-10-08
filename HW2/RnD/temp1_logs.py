import itertools, re
from utils import *

class Expr:

    def __init__(self, op, *args):
        #print "in __init__"
        "Op is a string or number; args are Exprs (or are coerced to Exprs)."
        assert isinstance(op, str) or (isnumber(op) and not args)
        self.op = num_or_str(op)
        self.args = map(expr, args) ## Coerce args to Exprs

    def __call__(self, *args):
        #print "in __call__"
        """Self must be a symbol with no args, such as Expr('F').  Create a new
        Expr with 'F' as op and the args as arguments."""
        assert is_symbol(self.op) and not self.args
        return Expr(self.op, *args)

    def __repr__(self):
        #print "in __repr__"
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)'"
        if not self.args:         # Constant or proposition with arity 0
            return str(self.op)
        elif is_symbol(self.op):  # Functional or propositional operator
            return '%s(%s)' % (self.op, ', '.join(map(repr, self.args)))
        elif len(self.args) == 1: # Prefix operator
            return self.op + repr(self.args[0])
        else:                     # Infix operator
            return '(%s)' % (' '+self.op+' ').join(map(repr, self.args))

    def __eq__(self, other):
        #print "in __eq__"
        """x and y are equal iff their ops and args are equal."""
        return (other is self) or (isinstance(other, Expr)
            and self.op == other.op and self.args == other.args)

    def __ne__(self, other):
        print "in __ne__"
        return not self.__eq__(other)

    def __hash__(self):
        print "in __hash__:op = %s" % self.op
        "Need a hash method so Exprs can live in dicts."
        return hash(self.op) ^ hash(tuple(self.args))

    # See http://www.python.org/doc/current/lib/module-operator.html
    # Not implemented: not, abs, pos, concat, contains, *item, *slice
    def __lt__(self, other):     return Expr('<',  self, other)
    def __le__(self, other):     return Expr('<=', self, other)
    def __ge__(self, other):     return Expr('>=', self, other)
    def __gt__(self, other):     return Expr('>',  self, other)
    def __add__(self, other):    return Expr('+',  self, other)
    def __sub__(self, other):    return Expr('-',  self, other)
    def __and__(self, other):    return Expr('&',  self, other)
    def __div__(self, other):    return Expr('/',  self, other)
    def __truediv__(self, other):return Expr('/',  self, other)
    def __invert__(self):        return Expr('~',  self)
    def __lshift__(self, other): return Expr('<<', self, other)
    def __rshift__(self, other): 
      #print "in __rshift__"
      return Expr('>>', self, other)
    def __mul__(self, other):    return Expr('*',  self, other)
    def __neg__(self):           return Expr('-',  self)
    def __or__(self, other):     return Expr('|',  self, other)
    def __pow__(self, other):    return Expr('**', self, other)
    def __xor__(self, other):    return Expr('^',  self, other)
    def __mod__(self, other):    return Expr('<=>',  self, other)



def expr(s):
    #print "s1: %s" %s
    if isinstance(s, Expr): return s
    if isnumber(s): return Expr(s)
    
    #print "s2: %s" %s
  ## Replace the alternative spellings of operators with canonical spellings
    s = s.replace('==>', '>>').replace('<==', '<<')
    s = s.replace('<=>', '%').replace('=/=', '^')
    
    #print "s3: %s" %s
  ## Replace a symbol or number, such as 'P' with 'Expr("P")'
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'Expr("\1")', s)
    
    #print "s4: %s" %s
  ## Now eval the string.  (A security hole; do not use with an adversary.)
    return eval(s, {'Expr':Expr})



def is_symbol(s):
    "A string s is a symbol if it starts with an alphabetic char."
    return isinstance(s, str) and s[:1].isalpha()

def is_var_symbol(s):
    "A logic variable symbol is an initial-lowercase string."
    return is_symbol(s) and s[0].islower()

def is_prop_symbol(s):
    """A proposition logic symbol is an initial-uppercase string other than
    TRUE or FALSE."""
    return is_symbol(s) and s[0].isupper() and s != 'TRUE' and s != 'FALSE'

def variables(s):
    result = set([])
    def walk(s):
        if is_variable(s):
            result.add(s)
        else:
            for arg in s.args:
                walk(arg)
    walk(s)
    return result

#===================================================================================
class FolKB():
    def __init__(self, initial_clauses=[]):
        self.clauses = [] # inefficient: no indexing
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        #if isinstance(sentence, Expr): print "isinstance:%s" % sentence.op
        self.clauses.append(sentence)

    def ask_generator(self, query):
        return fol_bc_ask(self, query)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self):
        return self.clauses

test_kb = FolKB(
    map(expr, [
                  #'Mother(Jean)',
                  '(Mother(m, c)) ==> Loves(m, c)'
                  #'(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)'
               ])
)
'''
test_kb = FolKB(
    map(expr, ['Farmer(Mac)',
               'Rabbit(Pete)',
               'Mother(MrsMac, Mac)',
               'Mother(MrsRabbit, Pete)',
               '(Rabbit(r) & Farmer(f)) ==> Hates(f, r)',
               '(Mother(m, c)) ==> Loves(m, c)',
               '(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)',
               '(Farmer(f)) ==> Human(f)',
               # Note that this order of conjuncts
               # would result in infinite recursion:
               #'(Human(h) & Mother(m, h)) ==> Human(m)'
               '(Mother(m, h) & Human(h)) ==> Human(m)'
               ])
)
'''

def standardize_variables(sentence, dic=None):
    """Replace all the variables in sentence with new variables.
    >>> e = expr('F(a, b, c) & G(c, A, 23)')
    >>> len(variables(standardize_variables(e)))
    3
    >>> variables(e).intersection(variables(standardize_variables(e)))
    set([])
    >>> is_variable(standardize_variables(expr('x')))
    True
    """
    if dic is None: dic = {}
    if not isinstance(sentence, Expr):
        print " not is instance"
        return sentence
    elif is_var_symbol(sentence.op):
        print "is_var_symbol: op=%s" % sentence.op
        if sentence in dic:
            print "in if: stmt is in dic[]"
            return dic[sentence]
        else:
            print "in else: stmt not in dic[]"
            v = Expr('v_%d' % standardize_variables.counter.next())
            dic[sentence] = v
            print dic
            return v
    else:
        print dic
        print "in else: about to return: op=%s" %sentence.op
        return Expr(sentence.op,
                    *[standardize_variables(a, dic) for a in sentence.args])

standardize_variables.counter = itertools.count()


#==================================
#========= Main program ===========
#================================== 


for rule in test_kb.fetch_rules_for_goal():
    standardize_variables(rule)

