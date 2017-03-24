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




