import os
from data_types import Input, Gate

def parse_inputs(inputs_file_name):
    """
    This function is responsible for taking in a file name, which corresponds to the file name
    where the inputs file is relative to the main function, and returning a dictionary of
    parsed inputs.

    :param inputs_file_name: [String] The file name of the inputs file relative to the main function.
    :return: [Dict[String, Input]] A dictionary of parsed inputs. (key = name, value = corresponding Input)
    """
    script_dir = os.path.dirname(__file__)
    inputs_file_name = os.path.join(script_dir, inputs_file_name)
    inputs_text = open(inputs_file_name, 'r').read()
    inputs_list = inputs_text.split("\n")
    inputs = {}

    for input in inputs_list:
        input_parts = input.split()
        if len(input_parts) > 0:
            input = Input(input_parts[0],
                          float(input_parts[1]),
                          float(input_parts[2]),
                          None)
            inputs[input.name] = input

    return inputs

def parse_csv_file(csv_file_name):
    """
    This function is responsible for taking in a file name which corresponds to the file name
    where the CSV file is relative to the main function, and returning a dictionary of the parsed
    gates.

    :param csv_file_name: [String] The file name of the csv file relative to the main function.
    :return: [Dict[String, Gate]]: A dictionary of the parsed gates. (key = name, value = corresponding Gate)
    """
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
    """
        This function is responsible for parsing the Bio Netlist and output a graph like structure
        that connects Inputs to Gates and Gates to Inputs and Outputs.

    :param bio_netlist: The text of the bionetlist.
    :param inputs: The dictionary of inputs that have been parsed from the inputs file.
    :param gates: The dictionary of gates that have been parsed from the csv file.
    :return: [([Input], [Input], [Gate])]: A tuple containing the initial inputs, all used inputs, and all used
            gates respectively
    """
    bio_netlist_list = bio_netlist.split("\n")
    bio_netlist_list.reverse()

    used_gates = []
    used_inputs = []
    initial_inputs = []

    # Because multiple gates can have the same repressor name, we obtain chunks of the list in order
    # to check which gate is the one that actually matches the repressor we need.
    string_chunks = bio_netlist.split()


    # If the bio_netlist_list length is less than 0, we had an issue with parsing it, so we return early
    if len(bio_netlist_list) <= 0:
        print "Error parsing netlist"
        return

    def parse_single_gate_input(bionetlist_str_list):
        """
        This will parse a single bionetlist line that has only one input (therefore it is a NOT gate).

        For example, given the following input: [P1_PhlF, pTet], a gate will be added to the used_gates
        from P1_PhlF, and pTet will be set as the input. pTet's gate will be set to P1_Phlf. Moreover,
        if pPhlF exists, that will be added to P1_PhlF's output.

        :param bionetlist_str_list: A list of the strings on a single line of the bionetlist.
        """
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
        """
            This will parse a single bionetlist line that has only one input (therefore it is a NOT gate).

            For example, given the following input: [P1_PhlF, pTet, pBad], a gate will be added to the used_gates
            from P1_PhlF, and pTet and pBad will be set as the inputs. pTet's gate and pBad's gate will be set to P1_Phlf.
            Moreover, if pPhlF exists, that will be added to P1_PhlF's output.

            :param bionetlist_str_list: A list of the strings on a single line of the bionetlist.
        """
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
            actual_gate = gates[[chunk for chunk in string_chunks if gate_ext in chunk and chunk != input_two.name][0]]
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

    #This while loop will continue until we have reached the part where only the inputs exist,
    #not gate connections. It checks that there is no binary.
    while bio_netlist_index < len(bio_netlist_list) and (len(bio_netlist_list[bio_netlist_index]) < 2 or not bio_netlist_list[bio_netlist_index].split()[1].isdigit()):
        bio_netlist_str_list = bio_netlist_list[bio_netlist_index].split()
        if len(bio_netlist_str_list) == 2:
            parse_single_gate_input(bio_netlist_str_list)
        elif len(bio_netlist_str_list) == 3:
            parse_double_gate_input(bio_netlist_str_list)
        bio_netlist_index += 1

    #We determine the initial inputs in order to allow for easier graph traversal.
    while bio_netlist_index < len(bio_netlist_list):
        initial_input = inputs[bio_netlist_list[bio_netlist_index].split()[0]]
        print "Initial input: " + initial_input.name
        initial_inputs.append(initial_input)
        bio_netlist_index += 1

    return (initial_inputs, used_inputs, used_gates)