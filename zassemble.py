# This file is derived from zassemble.c written by Emily Shaffer and James Massucco
#
# Author: David Frymoyer
# Compiles assembly into code usable by our version of the MIPS processor.

from Instructions import instruction_builder
import re
import argparse

default_register_names = {'$0': 0,
                          '$1': 1,
                          '$2': 2,
                          '$3': 3}


def convert_keys_to_numbers(lines, branch_names, register_names):
    # This converts symbols in the lines (so register names and branch names) into
    # numbers which are actually usable by the instructions.
    out_lines = []
    for line in lines:
        new_line = line
        # Remove branch names from the line.
        for k in branch_names.keys():
            if k in new_line:
                new_line = new_line.replace(k, str(branch_names[k] - len(out_lines)))
        # Remove register names from the line.
        for k in register_names.keys():
            if k in new_line:
                new_line = new_line.replace(k, str(register_names[k]))
        data_memory_expressions = re.findall(r'[0-9]+\([0-9]+\)', new_line)
        # Change data memory expressions (so things in the form <number>(<register>)) into
        # base and offset usable by sw and lw.
        if data_memory_expressions:
            values = re.findall(r'[0-9]+', data_memory_expressions[0])
            new_line = new_line.replace(data_memory_expressions[0], values[1] + ' ' + values[0])
        out_lines.append(new_line)
    return out_lines


def remove_symbols(lines):
    # Remove symbols from the lines. (So change labels and register names into integers).
    test_lines = []
    branch_dict = {}
    counter = 0
    for line in lines:
        counter += 1
        # We're just gonna have two comment schemes here...
        if line and re.match(r'[a-zA-Z0-9_:]', line.split('//')[0]) and re.match(r'[a-zA-Z0-9_:]', line.split('#')[0]):
            if ':' in line:
                # If there is a label in the line put the label in branch dict and check if there is also
                # code on the line
                split_line = line.split(':')
                goto_name = re.findall(r'[a-zA-Z0-9_]+', split_line[0])
                if not goto_name:
                    # This is if the line contains ": <rest of line>" because that is a blank branch name.
                    print 'Blank branch name at line {0}'.format(counter)
                    exit(0)
                # Add the name to the branch dict with a line number.
                if goto_name[0] not in branch_dict.keys():
                    branch_dict[goto_name[0]] = len(test_lines)
                else:
                    print 'Redefined branch label {0} at line {1}'.format(goto_name[0], counter)
                    exit(0)
                if re.match(r'[a-zA-Z0-9$_, ]', split_line[1]):
                    line = split_line[1]
                    while line[0] == ' ':
                        line = line[1:]
                else:
                    continue
            test_lines.append(line)
    return convert_keys_to_numbers(test_lines, branch_dict, default_register_names)


def main():
    # Set up the argument parser.
    parser = argparse.ArgumentParser(description='Compile a file for our implementation of MIPS')
    parser.add_argument('source', type=str, help='The source file')
    parser.add_argument('-d', '--dest', type=str, help='The destination file', default='output.coe', dest='dest')

    parsed_args = parser.parse_args()

    # Read in the lines.
    with open(parsed_args.source, 'r') as f:
        lines = f.readlines()

    # Take the raw code and turn it into something that our classes understand.
    lines = remove_symbols(lines)

    # Make our classes spit out the compiled output.
    compiled_output = map(lambda x: instruction_builder(x).compile(), lines)

    # Print out the resulting text.
    with open(parsed_args.dest, 'w') as f:
        f.write('memory_initialization_radix=16;\nmemory_initialization_vector=')
        exp_line = ''
        for line in compiled_output:
            exp_line += line + ','
        exp_line = exp_line[0:-1]
        f.write(exp_line + ';')
    pass


if __name__ == '__main__':
    main()