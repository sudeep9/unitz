
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
        for inst in instances_to_run:
            print "Starting thread: {0}".format(inst['unit'])
            t = threading.Thread(target = runInstance, args = (c, inst))
            threads.append(t)
            t.start()

        print "Waiting for all threads to complete" 
        for t in threads:
             t.join()

    except Exception:
        pass
    finally:
        return done()
