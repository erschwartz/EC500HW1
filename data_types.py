"""
    The Gate class represents a repressor as from a given CSV file. It includes many
    attributes that are related to the data needed to construct it.

    Attributes:
        name
        type
        color
        promoter
        promoter_dna
        ribozyme
        ribozyme_dna
        rbs
        rbs_dna
        cds
        cds_dna
        terminator
        terminator_dna
        ymax
        ymin
        k
        n
        il
        ih
        equation
        inputs: [[Input]] The inputs of the gate
        output: [Input] The output of the gate. If the gate name is K1_Exmpl, the output will be pExmpl.
                The only exception is when the output is the final output, in which case the output is None.
                While it may seem counterintuitive that the output is also the input, it is best to think
                of every output, besides the last one, being an input into another Gate.
"""
class Gate:
    def __init__(self, name, type, color, promoter, promoter_dna,
                 ribozyme, ribozyme_dna, rbs, rbs_dna, cds, cds_dna,
                 terminator, terminator_dna, ymax, ymin, k, n, il,
                 ih, equation, inputs, output):
        self.name = name
        self.type = type
        self.color = color
        self.promoter = promoter
        self.promoter_dna = promoter_dna
        self.ribozyme = ribozyme
        self.ribozyme_dna = ribozyme_dna
        self.rbs = rbs
        self.rbs_dna = rbs_dna
        self.cds = cds
        self.cds_dna = cds_dna
        self.terminator = terminator
        self.terminator_dna = terminator_dna
        self.ymax = ymax
        self.ymin = ymin
        self.k = k
        self.n = n
        self.il = il
        self.ih = ih
        self.equation = equation
        self.inputs = inputs
        self.output = output

"""
    The Input class is supposed to represent a single Input. The input may either be outputs of a gate (
    as described above), or they may be actual inputs into the circuit.

    Attributes:
        name
        xmin: [Float] The xmin value will initially be set to None for gate outputs and calculated later.
        xmax: [Float] The xmax value will initially be set to None for gate outputs and calculated later.
        gate: [Gate] The gate to which the input leads (not the gate from which the input came).
"""
class Input:
    def __init__(self, name, xmin, xmax, gate):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.gate = gate