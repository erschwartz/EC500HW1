def calculate_response_function_not(input, gate, is_promoter_op):
    """
    This function is responsible for calculating the score or response functions values of a single
    not gate.

    :param input: The input into the gate.
    :param gate: The gate in question.
    :param needed_gate: This is useful for our optimization functions only. It will return the xmin and xmax of the gate early.
    :return: The return value will be None if not for the needed_gate, or at the end of the graph.
    """

    if not is_promoter_op:
        gate.output.xmin = calculate_response_function(input.xmax, gate)
        gate.output.xmax = calculate_response_function(input.xmin, gate)

    # AT END
    if gate.output.gate is None:
        return calculate_score(gate.output.xmin, gate.output.xmax)

def calculate_response_function_nor(input_1, input_2, gate, is_promoter_op):
    """
    This function is responsible for calculating the score or response functions values of a single
    nor gate.

    :param input_1: The first input into the gate.
    :param input_2: The second input into the gate.
    :param gate: The gate in question.
    :return: The return value will be None if not for the needed_gate, or at the end of the graph.
    """

    if not is_promoter_op:
        #ON-MIN
        gate.output.xmax = calculate_response_function(input_1.xmin + input_2.xmin, gate)

        #OFF-MAX
        y1 = calculate_response_function(input_1.xmax + input_2.xmax, gate)
        y2 = calculate_response_function(input_1.xmax + input_2.xmin, gate)
        y3 = calculate_response_function(input_1.xmin + input_2.xmax, gate)
        gate.output.xmin = max(y1, y2, y3)

    if gate.output.gate is None:
        return calculate_score(gate.output.xmin, gate.output.xmax)

def calculate_response_function(x, gate):
    """
    This is useful for calculating the response function values of a given x value and a gate,
    without respect to the type of gate (this is done in the previous two functions).
    :param x: The needed x value.
    :param gate: The gate for which the values will be calculated with.
    :return: The calculated y response function value of the gate.
    """
    return gate.ymin + (gate.ymax - gate.ymin) / (1 + pow((x / gate.k), gate.n))

def calculate_score(xmin, xmax):
    """
    This function is responsible for calculating the score given the xmin and xmax values.

    :param xmin
    :param xmax
    :return: The score.
    """
    return xmax / xmin

def topology_score_finder(starting_inputs, is_promoter_op=False):
    """
    This algorithm is influenced by a topological sort algorithm in which inputs needed to be completed in a certain order.
    Because our data structure is based off of a graph, we thought this would be most efficient.

    One improvement we have made to our algorithm is to automatically complete gates that only require one input, as these
    gates will automatically have all of the necessary information to computer the response function values.

    Otherwise, our algorithm continues until myScore is none. myScore will be None unless it is determined in the functions
    aboved that the algorithm has reached the end (because the gate.output value will be None, as discussed
    in the data types file).

    :param starting_inputs: The initial inputs into the circuit.
    :param needed_gate: This value is only used for certain optimization functions. When not None, it will indicate that
                        calculation should stop at a certain gate and return early.
    :return: The calculated score of the system.
    """
    seen_inputs = {input.name: input for input in starting_inputs}
    score = None

    while (score == None):
        for name, input in seen_inputs.iteritems():
            if input.gate is not None and len(input.gate.inputs) == 1:
                score = calculate_response_function_not(input, input.gate, is_promoter_op)
                seen_inputs[input.gate.output.name] = input.gate.output
                del seen_inputs[input.name]
                break
            elif ((input.gate.inputs[0] == input or input.gate.inputs[0].name in seen_inputs.keys()) and (input.gate.inputs[1] == input or input.gate.inputs[1].name in seen_inputs.keys())):
                input_2_name = input.gate.inputs[0].name if input.gate.inputs[0].name != name else input.gate.inputs[1].name
                input_2 = seen_inputs[input_2_name]
                score = calculate_response_function_nor(input, input_2, input.gate, is_promoter_op)
                seen_inputs[input.gate.output.name] = input.gate.output
                del seen_inputs[input.name]
                del seen_inputs[input_2.name]
                break

    return score










