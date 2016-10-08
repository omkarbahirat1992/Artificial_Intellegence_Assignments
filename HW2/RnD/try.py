import re

class obj1:
  def __init__(self, str, *args):
    print "in __init__"
    self.op = str
    self.args = map(expr, args)
    print "str = %s" % self.op
    print "args = %s" % self.args
    print "hello obj1"
  
  def __call__(self, *args):
    print "in __call__"
    print "in __call__ op: %s" %self.op 
    return obj1(self.op, *args)


def expr(s):
    print "in expr s: %s" % s.op
    if isinstance(s, obj1):
      print "isinstance"
      return s
    
    print "in expr1 s: %s" % s
    
  ## Replace a symbol or number, such as 'P' with 'Expr("P")'
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'obj1("\1")', s)
    
## Now eval the string.  (A security hole; do not use with an adversary.)
    return eval(s, {'obj1':obj1})

#====================================================================================
#print "hello world"
#s = 'Farmer(a) & Person(b) & ~Son(c) > Farmer(c)'
s = 'Farmer(a) > son(c)'
#s = "Farmer(a)"

print "before re.sub: %s" %s
s = re.sub(r'([a-zA-Z0-9_.]+)', r'obj1("\1")', s)     #carve out predicate and arguments
print "after re.sub1: %s" %s

'''
if "inst" is an instance of class obj1 then 
  inst.op = predicate
  inst.args = list of arguments
'''
#print "eval = %s" % eval (s, {'obj1':obj1}).args[0].op    #"s" is an agrument to "obj1" due to the global specified, s = obj1("some string")
print "eval = %s" % eval (s, {'obj1':obj1}).args[0].op    #"s" is an agrument to "obj1" due to the global specified, s = obj1("some string")
print "after eval: %s" %s


