def num():
    for i in range(3):
        yield(i)

def num1(alpha):
    i = 2
    print "in num1"
    print alpha
    
    if alpha:
        print "in num1 if"
        pass
    else:
        for i in range(3):
            if i <= 1:
                print "pass %d" % i
                pass
            else:
                print "yield %d" % i
                yield i
    print "leaving num1"

def num2():
    print "in num2"
    for i in num1(False):
        print i
    print "leaving num2"

def test_generator():
#    generator = num1(False)
    val = True
    ret = False
    num1(val)
    if ret:
        print ret
    print "leaving generator"
'''
    for i in num1(val):
        print val
        print i
        print val
        print "==="
        if val: val = False
        else: val = True
#        num2()
'''

test_generator()


def gen1(val):
    print "in gen1()"
    if val == False:
        pass
    for i in gen2():
        print i
        yield i

def gen2():
    print "in gen2()"
    for i in gen1(True):
        print i
        yield i

def test_self_recursive_generator():
    print "in self_re"
    for i in gen1(True):
        print i

#test_self_recursive_generator()


'''
for letter in 'Python': 
    if letter == 'h':
        pass
        print 'This is pass block'
    else:
        print "in else"
    print 'Current Letter :', letter

'''
print "Good bye!"
