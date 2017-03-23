def calculate_response_function_not(input, gate):
    gate.output.xmin = calculate_response_function(input.xmax, gate)
    gate.output.xmax = calculate_response_function(input.xmin, gate)

    # AT END
    if gate.output.gate is None:
        return calculate_score(gate.output.xmin, gate.output.xmax)

def calculate_response_function_nor(input_1, input_2, gate):
    #ON-MIN
    gate.output.xmax = calculate_response_function(input_1.xmin + input_2.xmin, gate)

    #OFF-MAX
    y1 = calculate_response_function(input_1.xmax + input_2.xmax, gate)
    y2 = calculate_response_function(input_1.xmax + input_2.xmin, gate)
    y3 = calculate_response_function(input_1.xmin + input_2.xmax, gate)
    gate.output.xmin = max(y1, y2, y3)

    #AT END
    if gate.output.gate is None:
        return calculate_score(gate.output.xmin, gate.output.xmax)

def calculate_response_function(x, gate):
    return gate.ymin + (gate.ymax - gate.ymin) / (1 + pow((x / gate.k), gate.n))

def calculate_score(xmin, xmax):
    return xmax / xmin

def topology_score_finder(starting_inputs):
    inputs = starting_inputs
    seen_inputs = {}

    while (len(inputs) > 1):
        for input in inputs:
            if input.gate is not None and len(input.gate.inputs) == 1:
                calculate_response_function_not(input, input.gate)
                seen_inputs[input.gate.output.name] = input.gate.output
                inputs.remove(input)
                break
            elif ((input.gate.inputs[0] == input or input.gate.inputs[0].name in seen_inputs.keys()) and (input.gate.inputs[1] == input or input.gate.inputs[1].name in seen_inputs.keys())):
                input_2 = seen_inputs[input.gate.inputs[0]] if input.gate.inputs[0] in seen_inputs else seen_inputs[input.gate.inputs[1]]
                calculate_response_function_not(input, input_2, input.gate)
                seen_inputs[input.gate.output.name] = input.gate.output
                inputs.remove(input)
                break

    if inputs[0].gate.output.gate is not None:
        print "There has been an error, abort mission :("
    else:
        if len(inputs[0].gate.inputs) == 1:
            return calculate_response_function_not(inputs[0], inputs[0].gate)
        else:
            input_2 = seen_inputs[inputs[0].gate.inputs[0].name] if inputs[0].gate.inputs[0].name in seen_inputs else seen_inputs[inputs[0].gate.inputs[1].name]
            return calculate_response_function_nor(inputs[0], input_2, inputs[0].gate)






# Input: pTet gate: S1_Srpr
# Input: pLuxStar gate: P1_PhlF
# Gate: S1_Srpr input(s): pTet output: pSrpr
# Gate: P1_Phlf input(s): pSrpr, PLuxStar output: pPhlF
# Input pPhlF gate: None









