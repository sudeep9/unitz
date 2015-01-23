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

@unit('add numbers')
def add(a, b):
    o_addition_result = a + b
    print '{0} + {1} = {2}'.format(a,b, o_addition_result)
    return done()
```

Concept: __units__ are regular python functions and it should have the following traits:

* They should be stateless (although nothing prevents you to do otherwise)
* Any output of the computation should be captured in variables starting with name `o_`
* More than one output can be captured. 
* Should return using inbuilt function `done()` (working on to remove this limitation) 

Now that we can add 2 numbers ... we can use it to create __flow__ out of it. Flow is nothing but assembling units to be run in a certain sequence like below:

```python
#bobconfig.py

# We import everything from unitzcore .. 
from unitzcore import *

# Here we say from which module we want units to be used
unit_modules.append('bobunits') 

#flows is a python dict ...
flows['math'] = {  # 'math' is the name of the flow
    'order' : ['Addition'],
    'instances' : {
        'Addition' : {
            'unit' : 'add numbers', 
            'a' : 3, 
            'b' : 2
        },
    }
}
```

The config which is a python file already has a dict called `flow` with name of the flow as key. We then specify the order of the execution using `order`. What we execute are the instances of units defined in `instances`. In this case Bob decided to name it as `Addition` and specified which unit he intends to execute in `unit` and followed by params `a` & `b`.

Now we run ... we first export the envrironment variables:

```shell
sj:/Users/sudeepjathar/lab/unitz> source setenv_unitz
```

The go to the dir where bobconfig & bobunits are present and do this:

```shell
sj:sj:/Users/sudeepjathar/lab/py> unitz listf bobconfig
 1. math
sj:sj:/Users/sudeepjathar/lab/py> unitz listu bobconfig
 1. dummy
 2. print_ctx
 3. delete_ctx
 4. run_parallel
 5. add numbers

```

`unitz listf <config>` will list all the flows available in the specified config file.

`unitz listu <config>` will list all the units available from the modules that were specified in `unit_modules.append` .. ignore the rest of units for now .. this is explained in wiki

Now run the `math` flow:

```shell
sj:/Users/sudeepjathar/lab/py> unitz run bobconfig math
Addition ........................................................................ start
3 + 2 = 5
Addition ........................................................................ ok
```

Lets modify the flow in bobconfig.py to add 3 + 2 + 4:

```python
flows['math'] = { 
    'order' : ['Addition1', 'Addition2'],
    'instances' : {
        'Addition1' : {
            'unit' : 'add numbers', 
            'a' : 3, 
            'b' : 2
        },
        'Addition2' : {
            'unit' : 'add numbers', 
            '+a' : 'addition_result', 
            'b' : 4
        },
    }
}
```

The result:

```shell
sj:/Users/sudeepjathar/lab/py> unitz run bobconfig math
Addition1 ....................................................................... start
3 + 2 = 5
Addition1 ....................................................................... ok
Addition2 ....................................................................... start
5 + 4 = 9
Addition2 ....................................................................... ok
```

The `o_addition_result` was stripped of its `o_` and it was used in Addition2. The `'+a' : 'addition_result'` means that before executing Addtion2 copy into the arg `a` the value from `o_addition_result` which was computed by previous unit. In other words we sort of daisy-chained Addition1 and Addtion2 ... I call this feature `chaining`.

The leading '+' in `+a` means that set the value __before__ execution whereas trailing '+' (as in `'a+'`) would have meant setting value of the param __after__ the execution.

Enough for readme ... checkout the wiki for more features & details like inheriting flows & units, chaining.

Wishlist and further scope
--------------------------
1. Add UI where one can compose by drag and dropping units
2. Dry run (or simulation) of the flow
3. Infrastructure libraries for reuse
4. Interoperate with units developed in other languages
