from score_calculation import topology_score_finder

def increase_slope(gates):
    for gate in gates:
        gate.n *= 1.05

def decrease_slope(gates):
    for gate in gates:
        gate.n /= 1.05

def increase_stretch(gates):
    for gate in gates:
        gate.ymax *= 1.5
        gate.ymin /= 1.5

def decrease_stretch(gates):
    odd = True
    for gate in gates:
        if odd is True:
            gate.ymax *= 0.5
            gate.ymin /= 0.5
            odd = False
        else:
            odd = True

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



