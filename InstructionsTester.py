from tester import *
from Instructions import *

check_expect(instruction_builder('ADD 0 1 2').compile(), '2600', 'Test the add instruction compilation 1')
check_expect(instruction_builder('ADD 3 1 0').compile(), '24c0', 'Test the add instruction compilation 2')

check_expect(instruction_builder('AND 0 1 2').compile(), '5600', 'Test the and instruction compilation 1')
check_expect(instruction_builder('AND 3 1 0').compile(), '54c0', 'Test the and instruction compilation 2')

check_expect(instruction_builder('OR 2 1 0').compile(), '7480', 'Test the or instruction compilation 1')
check_expect(instruction_builder('OR 1 2 0').compile(), '7840', 'Test the or instruction compilation 2')

check_expect(instruction_builder('CLR 3').compile(), 'd3c0', 'Test the clear instruction compilation 1')
check_expect(instruction_builder('CLR 2').compile(), 'd280', 'Test the clear instruction compilation 2')

check_expect(instruction_builder('INV 3 1').compile(), '41c0', 'Test the invert instruction compilation 1')
check_expect(instruction_builder('INV 2 0').compile(), '4080', 'Test the invert instruction compilation 2')

check_expect(instruction_builder('ORI 3, 2, 4').compile(), '8b04', 'Test the ori instruction compilation 1')
check_expect(instruction_builder('ORI 2, 3, 255').compile(), '8eff', 'Test the ori instruction compilation 2')

check_expect(instruction_builder('ANDI 3, 2, 4').compile(), '6b04', 'Test the andi instruction compilation 1')
check_expect(instruction_builder('ANDI 2, 1, -10').compile(), '660a', 'Test the andi instruction compilation 2')

check_expect(instruction_builder('SLL 3, 2, 1').compile(), 'ab01', 'Test the sll instruction compilation 1')
check_expect(instruction_builder('SLL 2, 1, 1').compile(), 'a601', 'Test the sll instruction compilation 2')

check_expect(instruction_builder('SRA 3, 0, 1').compile(), '9301', 'Test the sra instruction compilation 1')
check_expect(instruction_builder('SRA 0, 2, 1').compile(), '9801', 'Test the sra instruction compilation 2')

check_expect(instruction_builder('ADDI 0, 1, 14').compile(), '340e', 'Test the addi instruction compilation 1')
check_expect(instruction_builder('ADDI 1, 2, 17').compile(), '3911', 'Test the addi instruction compilation 2')

check_expect(instruction_builder('LW 0, 1, 2').compile(), '0402', 'Test the lw instruction compilation 1')
check_expect(instruction_builder('LW 2, 1, 3').compile(), '0603', 'Test the lw instruction compilation 2')

check_expect(instruction_builder('SW 3, 2, 1').compile(), '1b01', 'Test the sw instruction compilation 1')
check_expect(instruction_builder('SW 2, 1, 3').compile(), '1603', 'Test the sw instruction compilation 2')

check_expect(instruction_builder('BNE 3 2 14').compile(), 'ce0e', 'Test the bne instruction compilation 1')
check_expect(instruction_builder('BNE 0 1 18').compile(), 'c112', 'Test the bne instruction compilation 2')

check_expect(instruction_builder('BEQ 2 3 20').compile(), 'bb14', 'Test the beq instruction compilation 1')
check_expect(instruction_builder('BEQ 0 3 -21').compile(), 'b3eb', 'Test the beq instruction compilation 2')

check_expect(get_hex(-1), 'ff', 'Testing get_hex for negative values')
