ADDRESS_LENGTH = 2
OPCODE_LENGTH = 4
IMMEDIATE_LENGTH = 8


def check_address(addr):
    # Make sure that the address is in our range.
    global ADDRESS_LENGTH
    if len(bin(addr).split('b')[1]) > ADDRESS_LENGTH:
        print 'Address {0} at line {1} is not in our scope'.format(addr)
        exit(0)
    return addr


def check_opcode(opcode):
    # Make sure that our opcode is in our range.
    global OPCODE_LENGTH
    if len(bin(opcode).split('b')[1]) > OPCODE_LENGTH:
        print 'Opcode {0} at line {1} is not recognized'.format(opcode)
        exit(0)
    return opcode


def check_immediate(imm):
    # Make sure that the immediate is in our range.
    global IMMEDIATE_LENGTH
    if len(bin(imm).split('b')[1]) > IMMEDIATE_LENGTH:
        print 'Immediate {0} at line {1} is too many digits'.format(imm)
        exit(0)
    return imm


def get_hex(value, max_value=256):
    # Return the hex string corresponding to the input value.
    if value < 0:
        return get_hex(max_value + value)
    else:
        return hex(value).split('x')[1].lower()


def pad(in_string, to_length, padding_value):
    # Pad the in_string to length to_length with padding padding_value
    if not to_length:
        raise ValueError("to_length field must have length greater than 0")
    out_string = in_string
    while len(out_string) < to_length:
        out_string = padding_value + out_string
    return out_string


# The dictionary of functions that know how to produce Instruction objects.
opcode_dict = {'LW': lambda x: i_builder(0, x),
               'SW': lambda x: i_builder(1, x),
               'ADD': lambda x: r_builder(2, x),
               'ADDI': lambda x: i_builder(3, x),
               'INV': lambda x: r_builder(4, [x[0], 0, x[1]]),
               'AND': lambda x: r_builder(5, x),
               'ANDI': lambda x: i_builder(6, x),
               'OR': lambda x: r_builder(7, x),
               'ORI': lambda x: i_builder(8, x),
               'SRA': lambda x: i_builder(9, x),
               'SLL': lambda x: i_builder(10, x),
               'BEQ': lambda x: j_builder(11, x),
               'BNE': lambda x: j_builder(12, x),
               'CLR': lambda x: r_builder(13, [x[0], 0, x[0]])}


def r_builder(opcode, args):
    # Builds an r type instruction.
    if len(args) != 3:
        raise ValueError('Bad number of arguments')
    return RInstruction(opcode, args[0], args[1], args[2])


def i_builder(opcode, args):
    # Builds an i type instruction.
    if len(args) != 3:
        raise ValueError('Bad number of arguments')
    return IInstruction(opcode, args[0], args[1], args[2])


def j_builder(opcode, args):
    # Builds a j type instruction.
    if len(args) != 3:
        raise ValueError('Bad number of arguments')
    return JInstruction(opcode, args[1], args[0], args[2])


class Instruction:
    # This is the base class for all of the instructions.
    def __init__(self, opcode):
        self.opcode = opcode

    def compile(self):
        raise NotImplementedError("Called compile on the default class")


class RInstruction(Instruction):
    # The class for r type instructions, its fields should be self explanatory.
    def __init__(self, opcode, rd, rs, rt):
        Instruction.__init__(self, opcode)
        self.rd = check_address(rd)
        self.rs = check_address(rs)
        self.rt = check_address(rt)

    def compile(self):
        return get_hex(self.opcode) + get_hex(self.rs * 4 + self.rt) + get_hex(self.rd * 4) + '0'


class IInstruction(Instruction):
    # The class for i type instructions, its fields should be self explanatory.
    def __init__(self, opcode, rd, rs, imm):
        Instruction.__init__(self, opcode)
        self.rd = check_address(rd)
        self.rs = check_address(rs)
        self.imm = check_immediate(imm)

    def compile(self):
        return get_hex(self.opcode) + get_hex(self.rs * 4 + self.rd) + pad(get_hex(self.imm), 2, '0')


class JInstruction(IInstruction):
    # Alias IInstruction for JInstruction in case they end up being different in the future.
    pass


def instruction_builder(instruction_text, opcode_dictionary=opcode_dict):
    # This is the function to actually build instructions.
    split_instruction = filter(lambda x: x, instruction_text.replace(',', '').split(' '))
    key = split_instruction[0].upper()
    if key not in opcode_dictionary.keys():
        raise ValueError('Found illegal instruction')
    return opcode_dictionary[key](map(lambda x: int(x, 16), split_instruction[1:]))
