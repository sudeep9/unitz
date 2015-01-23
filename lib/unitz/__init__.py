
from __future__ import print_function
from collections import OrderedDict
from functools import wraps
from inspect import getargspec
import sys

REGISTRY = OrderedDict()

class Context:
    def __init__(self):
        self.p = {}

    def getParams(self, plist):
        return (self.p[p] for p in plist)

class Unit:
    def __init__(self, name, func, enableContext = False):
        self.name = name
        self.func = func
        self.spec = None
        self.args = None
        self.defargs = None
        self.enableContext = enableContext 
        self.__initSpec()

    def __initSpec(self):
        spec = getargspec(self.func)
        defcount = 0

        if spec.defaults is not None:
            self.defargs = {}
            defcount = len(spec.defaults)
            for i, defvalue in enumerate(spec.defaults):
                varname = spec.args[-(i+1)]
                self.defargs[varname] = defvalue

        if defcount > 0:
            self.args = spec.args[:-defcount]
        else:
            self.args = spec.args


    def __constructCallingArgs(self, ctx):
        args = {}
        if self.defargs is not None:
            for argname, value in self.defargs.iteritems():
                if argname in ctx.p:
                    args[argname] = ctx.p[argname]
                else:
                    args[argname] = value

        for i, varname in enumerate(self.args):
            if i == 0 and self.enableContext:
                args[varname] = ctx
            else:
                args[varname] = ctx.p[varname]

        return args

    def __call__(self, ctx):
        args = self.__constructCallingArgs(ctx)
        return self.func(**args)

def unit(name, enableContext = False):
    def __unit(func):
        u = Unit(name, func, enableContext)
        REGISTRY[name] = u
        REGISTRY["{0}:{1}".format(func.__module__, name)] = u

        #@wraps(func)
        #def __unitWrapper(*args, **kargs):
        #    func(*args, **kargs)
        #todo: why to pre-create the object. make it lazy creation.

        return func
    return __unit


def done(status = True):
    caller = sys._getframe(1)
    op = {k[2:] : v  for k,v in caller.f_locals.iteritems() if k.startswith('o_')}
    return (status, op)

    

def getunit(name):
    return REGISTRY[name]



@unit('dummy')
def dummyUnit():
    return done()

if __name__ == "__main__":
    @unit('math')
    def mathOp(op, a, b = 10):
        if op == '+':
            o_sum = a + b
        elif op == '*':
            o_prod = a * b

        return done()
    
    c = Context()
    c.p['op'] = '+'
    c.p['a'] = 1
    u = getunit('math')
    print(u(c))
    print("context:", c.p)

    c.p['op'] = '*'
    c.p['a'] = 1
    print(u(c))
    print("context:", c.p)
    

