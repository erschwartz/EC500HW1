RUNNING THE PROGRAM:

To run, you must use the command:

py main.py <inputs filename> <outputs filename> <verilog filename> <UCF filename> <cello user> <cello pass>

It is assumed that the plasmid and eugene options are always false.

INTERPRETING RESULTS:

The output of your file should be something like this:

pTac            01010101
pTet            00110011
pBAD            00001111
S2_SrpR         pPhlF
P2_PhlF         pBM3R1    pHlyIIR
H1_HlyIIR       pBetI
E1_BetI         pAmtR     pAmeR
B3_BM3R1        pTac
F1_AmeR         pTet
A1_AmtR         pBAD
YFP             pSrpR


Input one: pBAD with gate: A1_AmtR
Input one: pTet with gate: F1_AmeR
Input one: pTac with gate: B3_BM3R1
Input one: pAmtR Input two: pAmeR with gate: E1_BetI
Input one: pBetI with gate: H1_HlyIIR
Input one: pBM3R1 Input two: pHlyIIR with gate: P2_PhlF
Input one: pPhlF with gate: S2_SrpR
Initial input: pBAD
Initial input: pTet
Initial input: pTac
Gate: E1_BetI changed slope value to: 0.99 n value: 2.376
Gate: H1_HlyIIR changed slope value to: 1.0 n value: 2.6
Gate: P2_PhlF changed slope value to: 1.05 n value: 4.095
Gate: S2_SrpR changed slope value to: 1.05 n value: 2.73
Gate: B3_BM3R1 changed stretch value to: 1.5 ymax: 1.2 ymin: 0.00666666666667
Original score: 569.344509705
Improved score: 602.601862104
Score percentage gain: 5.84134067016%


Modified UCF relative path: /Users/admin/Desktop/EC500/pycello/resources/new_gates.UCF.json


Original job ID: 2017-03-24 17:43:24.586170
Modified job ID: 2017-03-24 17:43:24.597500

The bionetlist will be shown that shows the overall structure of the gate. Next, construction of the "graph" will be shown. After that, the slope, stretch, and promoter value changes will be shown. The original score, the imroved score, and the score percentage gain will be shown. Then, the modified UCF path, relative to main.py, will be displayed. Lastly, the original job ID and the modified job ID will be displayed.

REQUIREMENTS:
Python 2.7 is required. Outside of the packages required by Cello, no other packages need to be installed to run. This can be run from the command line. 

