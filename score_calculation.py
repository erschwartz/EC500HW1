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
    seen_inputs = {input.name: input for input in starting_inputs}

    myScore = None

    while (myScore == None):
        for name, input in seen_inputs.iteritems():
            if input.gate is not None and len(input.gate.inputs) == 1:
                myScore = calculate_response_function_not(input, input.gate)
                seen_inputs[input.gate.output.name] = input.gate.output
                del seen_inputs[input.name]
                break
            elif ((input.gate.inputs[0] == input or input.gate.inputs[0].name in seen_inputs.keys()) and (input.gate.inputs[1] == input or input.gate.inputs[1].name in seen_inputs.keys())):
                input_2_name = input.gate.inputs[0].name if input.gate.inputs[0].name != name else input.gate.inputs[1].name
                input_2 = seen_inputs[input_2_name]
                myScore = calculate_response_function_nor(input, input_2, input.gate)
                seen_inputs[input.gate.output.name] = input.gate.output
                del seen_inputs[input.name]
                del seen_inputs[input_2.name]
                break

    return myScore






# Input: pTet gate: S1_Srpr
# Input: pLuxStar gate: P1_PhlF
# Gate: S1_Srpr input(s): pTet output: pSrpr
# Gate: P1_Phlf input(s): pSrpr, PLuxStar output: pPhlF
# Input pPhlF gate: None









