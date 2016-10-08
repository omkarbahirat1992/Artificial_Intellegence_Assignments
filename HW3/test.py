from decimal import Decimal

a = Decimal(str(1.0))

if (isinstance(a, Decimal)):
    print "isinstance"
else:
    print "not isinstance"
