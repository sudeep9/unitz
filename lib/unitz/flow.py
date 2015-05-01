
import unitz
from unitz import Context
import logging
import threading

log = logging.getLogger()

runInstanceLock = threading.Lock()

def __evaluate(ctx, val):
    if not isinstance(val, str):
        return val

    if len(val) <= 1:
        return ctx.p[val]

    print val
    if val.startswith('= '):
        return val[2:]
    elif val.startswith('eval '):
        return eval(val[5:])
    else:
        return ctx.p[val]

def __preRun_evaluate(ctx, param, value):
    if param.startswith('+'):
        if isinstance(value, str):
            ctx.p[param[1:]] = __evaluate(ctx, value)
        else:
            ctx.p[param[1:]] = value
    elif param[-1] not in ('+', '-') :
        ctx.p[param] = value
    
def __preRun(unit, ctx, params):
    if isinstance(params, dict):
        for param, value in params.iteritems():
            __preRun_evaluate(ctx, param, value)
    elif isinstance(params, list    ):
        for param_dict in params:
            param = param_dict.keys()[0]
            value = param_dict[param]
            __preRun_evaluate(ctx, param, value)
            

def __postRun_evaluate(ctx, status, param, value):            
    if status is True:
        if param.endswith('+'):
            if isinstance(value, str):
                ctx.p[param[:-1]] = __evaluate(ctx, value)
            else:
                ctx.p[param[:-1]] = value
    else:
        if param.endswith('!'):
            if isinstance(value, str):
                ctx.p[param[:-1]] = __evaluate(ctx, value)
            else:
                ctx.p[param[:-1]] = value

def __postRun(unit, ctx, params, status):
    if isinstance(params, dict):
        for param, value in params.iteritems():
            __postRun_evaluate(ctx, status, param, value)
    elif isinstance(params, list):
        for param_dict in params:
            param = param_dict.keys()[0]
            value = param_dict[param]
            __postRun_evaluate(ctx, status, param, value)


def runInstance(ctx, name, params):
    unit = unitz.getunit(name)
    
    with runInstanceLock:
        __preRun(unit, ctx, params)

    status, output = unit(ctx)

    with runInstanceLock:
        ctx.p.update(output)
        __postRun(unit, ctx, params, status)
    return status


def runFlow(name, config, ctx = None):
    if ctx is None:
        ctx = Context()

    for instance in config:
        unit_name = instance.keys()[0]
        if unit_name[0] == '~':
            continue
        yield ('instance-start', unit_name)
        instParams = instance[unit_name]
        status = runInstance(ctx, unit_name, instParams)
        yield ('instance-status', unit_name, status)


if __name__ == "__main__":
    from unitz import unit, done

    @unit(name = 'add')
    def add(a, b):
        try:
            o_result = a + b
            o_whatever = "abcd"
            print o_result
        finally:
            return done()

    @unit(name = 'mul')
    def mul(a, b, c = 3):
        try:
            o_result = a * b * c
            print o_result
        finally:
            return done()

    d = {
        'order' : ['init', ],
        'instances' : {
            'init' : {
                'unit' : 'dummy',
                'a' : 0,
                'b' : 1,
                'result': 0
            },
            'I1' : {
                'unit' : 'add',
                '+a': 'result',
                'b+': 'a'
            },
            'I2' : {
                'unit' : 'mul',
                '+a' : 'result', 
                'b' : 10,
                'c' : 4
            },
        }
    }

    for n in range(10):
        d['order'].append('I1')

    runFlow('testflow', d)
