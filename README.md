unitz
=====

What is unitz?
--------------
__unitz__ allows you to __compose__ python programs by assembling resuable code called __units__. Its written in python 2.7 and python 3 version will be added soon. Its being tested only with CPython for now.


Why it was developed?
---------------------
One of the primary use case was to enable developers quickly write automation code for their tests (both unit test & black box test). Also the design from start is geared to address automation reuse at company level specially where one team uses code of other teams.

Enough said ... Show me the code
================================

Lets add & multiply two numbers:

```
#mathunits.py

from unitz import unit, done

@unit('add numbers')
def add(a, b):
    o_addition_result = a + b
    return done()

@unit('multiply numbers')
def multiply(a,b):
    o_multiplication_result = a * b
    return done()
```

__units__ are 

