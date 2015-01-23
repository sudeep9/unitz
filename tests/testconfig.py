
from unitzcore import *

unit_modules.append('testunits')

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