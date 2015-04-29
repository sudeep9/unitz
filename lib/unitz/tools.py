
from unitz import unit, done, Context, REGISTRY
from importlib import import_module
import unitz.flow
import sys


def loadConfig(configname):
    config = import_module(configname)
    return config


def loadUnitModules(config):
    for path in config.unit_modules:
        import_module(path)

def runFlow(args):
    configname = args[0]
    flowname = args[1]
    ctx = Context()

    config = import_module(configname)

    if flowname not in config.flows:
        print "Error: flow name {0} not found".format(flowname)
        return False

    loadUnitModules(config)
    flowconfig = config.flows[flowname]
    for progress in unitz.flow.runFlow(flowname, flowconfig, ctx):
        if progress[0] == 'instance-start':
            print "{0} {1} start".format(progress[1], "." * (80 - len(progress[1])))
        elif progress[0] == 'instance-status':
            print "{0} {1} {2}".format(progress[1], "." * (80 - len(progress[1])), "ok" if progress[2] else "failed")
            print
            if not progress[2]:
                return False
        sys.stdout.flush()

            
def listFlows(args):
    configname = args[0]
    config = import_module(configname)

    for i, f in enumerate(config.flows):
        print "{0:2}. {1}".format(i + 1, f)

def listUnits(args):
    configname = args[0]
    config = import_module(configname)
    loadUnitModules(config)

    for i, name  in enumerate([k for k in REGISTRY if not ':' in k]):
        print "{0:2}. {1}".format(i + 1, name)

def getUnitList(configname):
    config = import_module(configname)
    loadUnitModules(config)

    return [k for k in REGISTRY if not ':' in k]
