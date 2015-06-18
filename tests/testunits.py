
from unitz import unit, done
from time import sleep

@unit('add')
def add(a,b):
    o_result = a + b
    print "{0} + {1} = {2}".format(a,b,o_result)
    return done()

@unit('mul')
def add(a,b):
    o_result = a * b
    print "{0} * {1} = {2}".format(a,b,o_result)
    return done()
