
from unitz import unit, done
from time import sleep

@unit('add')
def add(a,b):
    sleep(2)
    o_result = a + b
    print "{0} + {1} = {2}".format(a,b,o_result)
    return done()

@unit('mul')
def add(a,b):
    sleep(5)
    o_result = a * b
    print "{0} * {1} = {2}".format(a,b,o_result)
    return done()
