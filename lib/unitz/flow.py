
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

    prefix = val[0]
    if prefix == '=':
        return val
    elif prefix == '@':
        return eval(prefix[1:])

def __preRun(unit, ctx, params):
    for param, value in params.iteritems():
        if param != 'unit':
            if param.startswith('+'):
                if isinstance(value, str):
                    ctx.p[param[1:]] = __evaluate(ctx, ctx.p[value])
                else:
                    ctx.p[param[1:]] = value
            elif param[-1] not in ('+', '-') :
                ctx.p[param] = value

def __postRun(unit, ctx, params, status):
    for param, value in params.iteritems():
        if param != 'unit':
            if status is True:
                if param.endswith('+'):
                    if isinstance(value, str):
                        ctx.p[param[:-1]] = __evaluate(ctx, ctx.p[value])
                    else:
                        ctx.p[param[:-1]] = value
            else:
                if param.endswith('!'):
                    if isinstance(value, str):
                        ctx.p[param[:-1]] = __evaluate(ctx, ctx.p[value])
                    else:
                        ctx.p[param[:-1]] = value


def runInstance(ctx, params):
    name = params['unit']
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

    order = config['order']
    instances = config['instances']

    for instName in order:
        yield ('instance-start', instName)
        instParams = instances[instName]
        status = runInstance(ctx, instParams)
        yield ('instance-status', instName, status)


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
