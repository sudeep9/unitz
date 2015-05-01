
import sys
import importlib

def load_config(configfile):
    base_config = None
    with open(configfile + '.py') as f:
        for line in f:
            if line.startswith('from '):
                line = line.rstrip()
                arr = line.split(' ')
                base_config = arr[1]
                break
     
    importlib.import_module(configfile)
    m = sys.modules[configfile]
    return (base_config, m)

def println(indent, s):
    print "    " * indent,
    print s

def convert_to_yaml(base_config_name, config):
    print base_config_name
    
    if base_config_name is not None:
        print "include:", base_config_name
    
    if hasattr(config, 'unit_modules'):
        print 'unit_modules: [%s]' % ", ".join([m for m in config.unit_modules])
        
    print "flows:"
    indent = 0
    for flow_name, flow_config in config.flows.iteritems():
        indent += 1
        println(indent, flow_name + ':')
        for instance in flow_config['order']:
            inst_params = flow_config['instances'][instance]
            indent += 1
            println(indent, '- ' + inst_params['unit'] + ':')
            indent += 1
            for param, value in inst_params.iteritems():
                if param == 'unit': continue
                println(indent, '%s: %s' % (param, value))
            indent -= 1
            indent -= 1
        println(indent, "#--------------------------------------------------------")
        indent -= 1
        
        

if len(sys.argv[1:]) < 1:
    print "Error: missing config file"
    exit(1)

configfile = sys.argv[1]

base_config_name, m = load_config(configfile)
convert_to_yaml(base_config_name, m)
