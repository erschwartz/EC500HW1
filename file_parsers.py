import os
from data_types import Input, Output, Gate

def parse_inputs(inputs_file_name):
    script_dir = os.path.dirname(__file__)
    inputs_file_name = os.path.join(script_dir, inputs_file_name)
    inputs_text = inputs_text = open(inputs_file_name, 'r').read()
    input_str_list = inputs_text.split("\n")
    inputs = {}

    for input in input_str_list:
        input_strs = input.split()
        if len(input_strs) > 0:
            input = Input(input_strs[0],
                          float(input_strs[1]),
                          float(input_strs[2]),
                          None)
            inputs[input.name] = input

    return inputs

def parse_outputs(output_file_name):
    script_dir = os.path.dirname(__file__)
    output_file_name = os.path.join(script_dir, output_file_name)
    outputs_txt = open(output_file_name, 'r').read()
    output_str_list = outputs_txt.split("\n")
    outputs = {}

    for output in output_str_list:
        output_strs = output.split()
        if len(output_strs) > 0:
            output = Output(output_strs[0], None)
            outputs[output.name] = output

    return outputs

def parse_csv_file(csv_file_name):
    script_dir = os.path.dirname(__file__)
    csv_file_name = os.path.join(script_dir, csv_file_name)
    csv_text = inputs_text = open(csv_file_name, 'r').read()
    csv_list = csv_text.split()

    first_line = True
    gate_dict = {}
    for csv in csv_list:
        if first_line:
            first_line = False
        else:
            string_list = csv.split(",")
            gate_dict[string_list[0]] = Gate(string_list[0],
                                             string_list[1],
                                             string_list[2],
                                             string_list[3],
                                             string_list[4],
                                             string_list[5],
                                             string_list[6],
                                             string_list[7],
                                             string_list[8],
                                             string_list[9],
                                             string_list[10],
                                             string_list[11],
                                             string_list[12],
                                             float(string_list[13]), #ymax
                                             float(string_list[14]), #ymin
                                             float(string_list[15]), #k
                                             float(string_list[16]), #n
                                             string_list[17],
                                             string_list[18],
                                             string_list[19],
                                             None,
                                             None)

    return gate_dict

def parse_bio_netlist(bio_netlist, inputs, gates):
    bio_netlist_strs = bio_netlist.split("\n")
    bio_netlist_strs.reverse()

    used_gates = []
    used_inputs = []
    initial_inputs = []

    string_chunks = bio_netlist.split()

    if len(bio_netlist_strs) <= 0:
        print "Error parsing netlist"
        return

    def parse_single_gate_input(bionetlist_str_list):
        input_one = None
        gate = gates[bio_netlist_str_list[0]] if bio_netlist_str_list[0] in gates else None
        if bio_netlist_str_list[1] in inputs:
            input_one = inputs[bio_netlist_str_list[1]]
        else:
            input_one = Input(bio_netlist_str_list[1], None, None, gate)
            inputs[bio_netlist_str_list[1]] = input_one

            gate_ext = input_one.name[1:]

            actual_gate = gates[[chunk for chunk in string_chunks if gate_ext in chunk and chunk != input_one.name][0]]
            actual_gate.output = input_one

        used_inputs.append(input_one)
        input_one.gate = gate

        if gate is not None:
            gate.inputs = [input_one]
            used_gates.append(gate)
            print 'Input one: ' + input_one.name + ' with gate: ' + gate.name

    def parse_double_gate_input(bionetlist_str_list):
        input_one = None
        input_two = None
        gate = gates[bio_netlist_str_list[0]] if bio_netlist_str_list[0] in gates else None
        if bio_netlist_str_list[1] in inputs:
            input_one = inputs[bio_netlist_str_list[1]]
        else:
            input_one = Input(bio_netlist_str_list[1], None, None, gate)
            inputs[bio_netlist_str_list[1]] = input_one

            gate_ext = input_one.name[1:]
            actual_gate = gates[[chunk for chunk in string_chunks if gate_ext in chunk and chunk != input_one.name][0]]
            actual_gate.output = input_one

        if bio_netlist_str_list[2] in inputs:
            input_two = inputs[bio_netlist_str_list[2]]
        else:
            input_two = Input(bio_netlist_str_list[2], None, None, gate)
            inputs[bio_netlist_str_list[2]] = input_one

            gate_ext = input_two.name[1:]
            actual_gate = gates[[chunk for chunk in string_chunks if gate_ext in chunk and chunk != input_one.name][0]]
            actual_gate.output = input_two

        input_one.gate = gate
        input_two.gate = gate
        used_inputs.append(input_one)
        used_inputs.append(input_two)

        if gate is not None:
            used_gates.append(gate)
            gate.inputs = [input_one, input_two]
            print 'Input one: ' + input_one.name + ' Input two: ' + input_two.name + ' with gate: ' + gate.name

    bio_netlist_index = 0
    while not bio_netlist_strs[bio_netlist_index].split()[1].isdigit(): #until we get binary (2+ digits)
        bio_netlist_str_list = bio_netlist_strs[bio_netlist_index].split()
        if len(bio_netlist_str_list) == 2:
            parse_single_gate_input(bio_netlist_str_list)
        else:
            parse_double_gate_input(bio_netlist_str_list)
        bio_netlist_index += 1

    while bio_netlist_index < len(bio_netlist_strs):
        initial_input = inputs[bio_netlist_strs[bio_netlist_index].split()[0]]
        print "Initial input: " + initial_input.name
        initial_inputs.append(initial_input)
        bio_netlist_index += 1

    return (initial_inputs, used_inputs, used_gates)