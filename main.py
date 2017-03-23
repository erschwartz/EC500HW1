from file_parsers import parse_inputs, parse_csv_file, parse_bio_netlist, parse_outputs
from cello_client import CtxObject
from score_calculation import topology_score_finder
import os

if __name__ == '__main__':
    inputs = parse_inputs("resources/Inputs2.txt")
    gates = parse_csv_file("resources/gates_Eco1C1G1T1.csv")

    ctx = CtxObject()
    # bio_netlist = get_netlist(ctx, "j4", "resources/Inputs.txt", "resources/Outputs.txt", "resources/0xFE.v", "JSON.UCF.json -plasmid false -eugene false")

    script_dir = os.path.dirname(__file__)
    bio_netlist_name = os.path.join(script_dir, "resources/bionetlist2.txt")
    bio_netlist_txt = open(bio_netlist_name, 'r').read()

    print bio_netlist_txt

    initial_inputs, used_inputs, used_gates = parse_bio_netlist(bio_netlist_txt, inputs, gates)

    print topology_score_finder(initial_inputs)

    # csv_file_path = write_back_to_csv(repressor_dict)
    # convert_csv_to_ucf(csv_file_path)


