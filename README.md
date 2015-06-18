unitz
=====

What is unitz?
--------------
__unitz__ allows you to __compose__ python programs by assembling resuable code called __units__. Its written in python 2.7 and python 3 version will be added soon. Its being tested only with CPython for now.


Why it was developed?
---------------------
One of the primary use case was to enable developers quickly write automation code for their tests (both unit test & black box test). Also the design from start is geared to address automation reuse at company level specially where one team uses code of other teams.

Features
--------

1. Assemble or compose programs from smaller components (or units)
2. Inherit units and flows from existing configuration (allows for across team re-usability)
3. Polymorphism at configuration level (explained in wiki)
3. Chain the units i.e. feed output of one as input to another

Checkout [Wiki Tutorial](https://github.com/sudeep9/unitz/wiki/Tutorial) for demo of features

Stability
---------
Pre-Alpha

Installation
------------
Right now unitz is not available on Pypi. It will be in future.  
Note: only *nix platforms & OSX are supported out of the box. There is no technical problem in supporting windows its just that the bat file to source the env vars has not been written right now.

For now clone the repository and source the `setenv_unitz`:

```shell
sj:/Users/sudeepjathar/lab/unitz> source setenv_unitz
```
The `source` may not work if you have KSH and you can use the dot `.` to source

For windows ... try changing setenv_unitz to its bat file equivalent and source it. I will do it eventually.


Enough said ... Show me the code
================================

Lets say Bob wrote a function to add numbers

```python
def add(a, b):
    return a + b
```

Now he does not want others to reinvent the wheel and wishes to make this reusable. (I know that for some this example is lame ... but imagine instead that this could be something like connecting to database and create test data or transfer a file from machine A to B ...) 

So he converts the function into a unit:

```python
#bobunits.py
from unitz import unit, done

@unit('add_numbers')
def add(a, b):
    o_addition_result = a + b
    print '{0} + {1} = {2}'.format(a,b, o_addition_result)
    return done()
```

Lets add 3 + 2 by creating a __flow__ in a config file (YAML file):

```yaml
bobconfig.yml

include: unitz
unit_modules: [bobunits]

flows:
    math:
        - add_numbers:
            a: 3
            b: 2
```

Before we run ... we first export the envrironment variables:

```shell
sj:/Users/sudeepjathar/lab/unitz> source setenv_unitz
```

Now run the `math` flow:

```shell
sj:/Users/sudeepjathar/lab/py> unitz run bobconfig math
add_numbers ..................................................................... start
3 + 2 = 5
add_numbers ..................................................................... ok
```

Concept: __units__ are regular python functions and it should have the following traits:

* They should be stateless (although nothing prevents you to do otherwise)
* Any output of the computation should be captured in variables starting with name `o_`
* More than one output can be captured. 
* Should return using inbuilt function `done()` (working on to remove this limitation) 
Note: Since its YAML file, indentation is important.


Lets modify the flow in bobconfig.py to add 3 + 2 + 4:

```yaml
bobconfig.yml

include: unitz
unit_modules: [bobunits]

flows:
    math:
        - add_numbers:
            a: 3
            b: 2
        - add_numbers:
            +a: addition_result
            b: 2
```

The result:

```shell
sj:/Users/sudeepjathar/lab/py> unitz run bobconfig math
add_numbers ..................................................................... start
3 + 2 = 5
add_numbers ..................................................................... ok

add_numbers ..................................................................... start
5 + 2 = 7
add_numbers ..................................................................... ok
```

The `o_addition_result` was stripped of its `o_` and it was used in the second addition. The `'+a' : 'addition_result'` means that before executing copy into the arg `a` the value from `o_addition_result` which was computed by previous unit. In other words we sort of daisy-chained the two additions... I call this feature `chaining`.

The leading '+' in `+a` means that set the value __before__ execution whereas trailing '+' (as in `'a+'`) would have meant setting value of the param __after__ the execution.

Enough for readme ... checkout the wiki for more features & details like inheriting flows & units, chaining.

Wishlist and further scope
--------------------------
1. Add UI where one can compose by drag and dropping units
2. Dry run (or simulation) of the flow
3. Infrastructure libraries for reuse
4. Interoperate with units developed in other languages
5. Move the flow configuration outside python program (something like YAML)
