from zassemble import *
from tester import *

check_expect(convert_keys_to_numbers(['LW $1, 67($0)'], {}, default_register_names),
             ['LW 1, 0 67'], 'Test convert_keys_to_numbers 1')

check_expect(convert_keys_to_numbers(['BNE $1 $2 main'], {'main': 40}, default_register_names),
             ['BNE 1 2 40'], 'Test convert_keys_to_numbers 2')

check_expect(remove_symbols(['ANDI $0 $0 0',
                             'SW $0 0($0)',
                             'main:',
                             'BEQ $0 $0 main']),
             ['ANDI 0 0 0',
              'SW 0 0 0',
              'BEQ 0 0 0'], 'Test remove symbols 1')

check_expect(remove_symbols(['ANDI $0 $0 0',
                             'ANDI $1 $1 0',
                             'ADDI $1 $1 10',
                             'loop_start: ADDI $0 $0 1',
                             'BNE $0 $1 loop_start',
                             'ANDI $2 $2 0',
                             'SW $0 0($2)']),
             ['ANDI 0 0 0',
              'ANDI 1 1 0',
              'ADDI 1 1 10',
              'ADDI 0 0 1',
              'BNE 0 1 -1',
              'ANDI 2 2 0',
              'SW 0 2 0'], 'Test remove symbols 2')