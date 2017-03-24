from score_calculation import topology_score_finder

def change_slope(gate, x):
    """
        This function will change the slope of the gate.

        Attributes:
            gate [Gate]: The gates for which the slope will be increased
    """
    gate.n *= x

def change_stretch(gate, x):
    """
        This function will change the stretch of the gate.

        Attributes:
            gate [Gate]: The gates for which the slope will be decreased
    """

    gate.ymax *= x
    gate.ymin /= x

def change_promoter_value(gate, x):
    """
    This function will change the promoter value of the gate. If it is determined that the promoter value
    is not within a given bounds, it will not continue.
    :param gate: The gate for which the promoter value is changed.
    :param x: The x value to affect the promoter value.
    :return: True if the value is within a given range, False if the value is not in the given range
    """

    gate.ymax = gate.ymax / x
    gate.ymin = gate.ymin / x

    if gate.ymax < 1000 and gate.ymax > .001 and gate.ymin < 1000 and gate.ymin > .001:
        return True
    else:
        return False

def perform_stretch_operation(inputs, gate, original_score):
    """
        This function will perform a stretch operation on a gate. It will go through a range of stretch
        values and record the best score received as a result and use that stretch value.

        :param inputs: The inputs in order to perform the score calculation.
        :param gate: The gate that the stretch operations will be performed on.
        :param original_score: The original score before any operations are performed.
    """

    original_ymax = gate.ymax
    original_ymin = gate.ymin

    if original_ymax - original_ymin > 1:
        return

    best_score = original_score
    best_stretch_value = 1
    minimum_stretch_value = 0.1
    maximum_stretch_value = 1.5
    current_stretch_value = minimum_stretch_value
    delta = 0.1

    while current_stretch_value <= maximum_stretch_value + .001:
        change_stretch(gate, current_stretch_value)

        new_score = topology_score_finder(inputs)
        if new_score > best_score:
            best_stretch_value = current_stretch_value

        gate.ymax = original_ymax
        gate.ymin = original_ymin
        current_stretch_value += delta

    change_stretch(gate, best_stretch_value)
    print "Gate: " + gate.name + " changed stretch value to: " + str(best_stretch_value) + " ymax: " + str(gate.ymax) + " ymin: " + str(gate.ymin)

def perform_slope_operation(inputs, gate, original_score):
    """
    This function will perform a slope operation on a gate. It will go through a range of slope
    values and record the best score received as a result and use that slope value.

    :param inputs: The inputs in order to perform the score calculation.
    :param gate: The gate that the slope operations will be performed on.
    :param original_score: The original score before any operations are performed.
    """
    original_n_value = gate.n
    midpoint_x = (gate.output.xmax + gate.output.xmin) / 2
    midpoint_y = (gate.ymax + gate.ymin) / 2

    if midpoint_x >= midpoint_y - .1 and midpoint_x <= midpoint_y + .1:
        return

    best_score = original_score
    best_slope_value = 1
    minimum_slope_value = 0.95
    maximum_slope_value = 1.05
    current_slope_value = minimum_slope_value
    delta = 0.01

    while current_slope_value <= maximum_slope_value + .001:
        change_slope(gate, current_slope_value)
        new_score = topology_score_finder(inputs)

        if new_score > best_score:
            best_slope_value = current_slope_value

        current_slope_value += delta
        gate.n = original_n_value

    change_slope(gate, best_slope_value)
    print "Gate: " + gate.name + " changed slope value to: " + str(best_slope_value) + " n value: " + str(gate.n)

def perform_promoter_operations(inputs, gate, original_score):
    """
    This function is responsible for performing any promoter operations. It will go through a range of
    promoter values and record the best score that it finds as a result.
    :param inputs: The inputs needed in order to find the new score.
    :param gate: The gate to perform a promoter operation on.
    :param original_score: The original score to compare against.
    """
    gate_ymin = gate.ymin
    gate_ymax = gate.ymax

    if gate.ymax > gate.output.xmax or gate.ymin > gate.output.xmin:
        return

    best_score = original_score
    best_promoter_value = 1
    minimum_promoter_value = .001
    maximum_promoter_value = 1000
    current_promoter_value = minimum_promoter_value
    delta = 0.1

    while current_promoter_value <= maximum_promoter_value + .001:
        valid_bounding_conditions = change_promoter_value(gate, current_promoter_value)

        if valid_bounding_conditions is True:
            new_score = topology_score_finder(inputs, True)

            if new_score > best_score:
                best_promoter_value = current_promoter_value
                best_score = new_score

        current_promoter_value += delta
        gate.ymin = gate_ymin
        gate.ymax = gate_ymax

    change_promoter_value(gate, best_promoter_value)
    if best_promoter_value is not 1:
        print "Gate: " + gate.name + " changed promoter value to: " + str(best_promoter_value)

def optimize_gates(inputs, gates):
    """
    This function is responsible for going through and optimizing all of the gates. It will output
    the improve score and the percentage gain.
    :param inputs: The list of initial inputs in order to find the improved scores
    :param gates: The list of gates of which changes can be made on.
    """
    original_score = topology_score_finder(inputs)

    for gate in gates:
        perform_slope_operation(inputs, gate, original_score)

    for gate in gates:
        perform_stretch_operation(inputs, gate, original_score)

    for gate in gates:
        perform_promoter_operations(inputs, gate, original_score)

    new_score = topology_score_finder(inputs)

    print "Original score: " + str(original_score)
    print "Improved score: " + str(new_score)
    print "Score percentage gain: " + str(((new_score - original_score) / original_score) * 100) + "%"


