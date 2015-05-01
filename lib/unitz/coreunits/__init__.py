
from unitz import unit, done

@unit('dummy')
def dummyUnit():
    return done()


@unit('print_ctx', enableContext =True)
def printContext(c, params):
    for p in params:
        print p, "=", c.p[p]
    return done()

@unit('delete_ctx')
def deleteContext(c, params):
    for p in params:
        del c.p[p]

@unit('run_parallel', enableContext =True)
def runParallel(c, instances_to_run):
    try:
        import threading
        from unitz.flow import runInstance
        threads = []
        for inst, params in instances_to_run.iteritems():
            print "Starting thread: {0}".format(inst)
            t = threading.Thread(target = runInstance, args = (c, inst, params))
            threads.append(t)
            t.start()

        print "Waiting for all threads to complete" 
        for t in threads:
             t.join()

    except Exception:
        pass
    finally:
        return done()

@unit('export_params_from_file', enableContext = True)
def exportParamsInFile(c, param_file):
    try:
        with open(param_file) as f:
            for line in f:
                line = line.rstrip()
                var, value = line.split(' = ')
                dataType, param = var.split()
                print dataType, param
                if dataType == 'int':
                    c.p[param] = int(value)
                else:
                    c.p[param] = value
    except Exception, fault:
        print str(fault)
        return done(False)

    return done()

@unit('cli_args_positional', enableContext = True)
def cli_args_positional(c, arglist):
    import sys    
    if len(sys.argv[4:]) < len(arglist):
        print "Error: not enough args"
        print "args:", " ".join(["<{0}>".format(a) for a in arglist])
        return done(False)

    for i, arg in enumerate(arglist):
        c.p['input_' + arg] = sys.argv[3 + i+1]

    return done()

@unit('add_builtin', enableContext = True)
def add_builtin(c):
    __builtins__['myvar'] = 1
    return done()

@unit('test_unit', enableContext = True)
def test_unit(c):
    print myvar
    return done()    


@unit('assert', enableContext = True)
def unit_assert(c, checks, equality = True):
    for param, value in checks.iteritems():
        if param not in c.p:
            print 'Error: param [%s] not in context' % param
            return done(False)
        actual_value = c.p[param]
        if (equality and actual_value != value) or (not equality and actual_value == value):
            print 'Error: assert failed equality: %s param: [%s]  value: [%s] actual value: [%s]' % (equality, 
            param, value, actual_value)
            return done(False)
            
    return done()
