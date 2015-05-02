
from unitz import unit, done

@unit('Parse file newline')
def parse_file_newline(filename):
    o_parsed_ints = []
    with open(filename) as f:
        for line in f:
            o_parsed_ints.append(int(line))
            
    return done()
    
@unit('Sum integer list')
def sum_integer_list(int_list):
    o_sum = 0
    for n in int_list:
        o_sum += n
    print 'Sum =', o_sum
    
    return done()
