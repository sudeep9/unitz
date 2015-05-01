#bobunits.py
from unitz import unit, done

@unit('add_numbers')
def add(a, b):
    o_addition_result = a + b
    print '{0} + {1} = {2}'.format(a,b, o_addition_result)
    return done()
