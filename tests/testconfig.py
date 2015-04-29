
from unitzcore import *

unit_modules.append('testunits')

flows['params'] = {
  'order' : ['args', 'print_c', 'p'],
  'instances' : {
    'args' : {
      'unit' : 'cli_args_positional',
      'arglist' : ['param_file']
    },
    'print_c' : {
      'unit' : 'print_ctx',
      'params' : ['input_param_file']
    },
    'p' : {
      'unit' : 'export_params_from_file',
      '+param_file' : '=C:\\SJ\\param.txt'
    },
  }
}

flows['math'] = {
    'order' : ['Addition', 'Multiplication'],
    'instances' : {
        'Addition' : {
            'unit' : 'add', 
            'a' : 3, 
            'b' : 2
        },
        'Multiplication' : {
            'unit' : 'mul', 
            '+a' : 'result', 
            'b' : 4
        },
    }
}

flows['math_parallel'] = {
    'order' : ['Parallel math'],
    'instances' : {
        'Parallel math' : {
            'unit' : 'run_parallel', 
                'instances_to_run' : [
                    {
                        'unit' : 'add',
                        'a' : 3, 
                        'b' : 2
                    },
                    {
                        'unit' : 'mul',
                        'a' : 10, 
                        'b' : 20
                    },
                ]
        },
    }
}

flows['std_test'] = {
    'order' : ['cmd1', 'print_stream'],
    'instances' : {
        'cmd1' : {
            'unit' : 'run_command',
            'cmd' : 'ls -lrt'
        },
        'print_stream' : {
            'unit' : 'print_stream',
            '+stream' : 'stdout'
        }
    }
}
