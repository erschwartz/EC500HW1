from score_calculation import topology_score_finder

def increase_slope(gate):
    """
        This function will increase the slope of the gate. We generally found that using the highest possible
        value to affect the slope caused the highest increase/decrease in score, so we decided to use that.

        Attributes:
            gate [Gate]: The gates for which the slope will be increased
    """
    gate.n *= 1.05

def decrease_slope(gate):
    """
        This function will decrease the slope of the gate. We generally found that using the highest possible
        value to affect the slope caused the highest increase/decrease in score, so we decided to use that.

        Attributes:
            gate [Gate]: The gates for which the slope will be decreased
    """
    gate.n /= 1.05


def increase_stretch(gate):
    """
        This function will increase the stretch of the gate. We generally found that using the highest possible
        value to affect the stretch caused the highest increase/decrease in score, so we decided to use that.

        Attributes:
            gate [Gate]: The gates for which the slope will be decreased
    """
    gate.ymax *= 1.5
    gate.ymin /= 1.5

def decrease_stretch(gate):
    """
        This function will decrease the stretch of the gate. We generally found that using the lowest possible
        value to affect the stretch caused the highest increase/decrease in score, so we decided to use that.

        Attributes:
            gate [Gate]: The gates for which the slope will be decreased
    """
    gate.ymax *= 0.1
    gate.ymin /= 0.1

def change_y_values(inputs, gate, score):
    print gate.name
    lower = 1.03726 - .0001
    upper = 1.03726 + .0001

    original_ymin = gate.ymin
    original_ymax = gate.ymax
    best_multiply_value = 1
    best_score = score

    while (lower < upper):
        gate.ymin = lower * original_ymin
        gate.ymax = lower * original_ymax

        new_score = topology_score_finder(inputs)

        print "Score: " + str(new_score) + " Delta value: " + str(lower)

        if new_score > best_score:
            best_score = new_score
            best_multiply_value = lower

        lower += .00000002

    gate.ymin = original_ymin * best_multiply_value
    gate.ymax = original_ymax * best_multiply_value


def optimize_promoters(gates, inputs):
    gate_values = topology_score_finder(inputs, gates[0])
    score = gate_values[1] / gate_values[0]

    if gates[0].ymax < topology_score_finder(inputs, gates[0])[1]:
        change_y_values(inputs, gates[0], score)



