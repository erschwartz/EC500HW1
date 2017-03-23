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

class Input:
    def __init__(self, name, xmin, xmax, gate):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.gate = gate

class Output:
    def __init__(self, name, gate):
        self.name = name
        self.gate = gate