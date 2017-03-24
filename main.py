from file_parsers import parse_inputs, parse_csv_file, parse_bio_netlist, parse_outputs
from cello_client import CtxObject
from score_calculation import topology_score_finder
from optimization_functions import increase_slope, decrease_slope, increase_stretch, decrease_stretch, optimize_promoters, change_y_values
import os

if __name__ == '__main__':
    inputs = parse_inputs("resources/Inputs.txt")
    gates = parse_csv_file("resources/gates_Eco1C1G1T1.csv")

    ctx = CtxObject()
    # bio_netlist = get_netlist(ctx, "j4", "resources/Inputs.txt", "resources/Outputs.txt", "resources/0xFE.v", "JSON.UCF.json -plasmid false -eugene false")

    script_dir = os.path.dirname(__file__)
    bio_netlist_name = os.path.join(script_dir, "resources/bionetlist.txt")
    bio_netlist_txt = open(bio_netlist_name, 'r').read()

    print bio_netlist_txt

    initial_inputs, used_inputs, used_gates = parse_bio_netlist(bio_netlist_txt, inputs, gates)
    original_score = topology_score_finder(initial_inputs)

    # for gate in reversed(used_gates):
    change_y_values(initial_inputs, used_gates[3], original_score)
    new_score = topology_score_finder(initial_inputs)

    print original_score
    print new_score

    # increase_stretch(used_gates)
    # increase_slope(used_gates)
    # print topology_score_finder(initial_inputs)

    # decrease_stretch(used_gates)
    # decrease_stretch(used_gates)
    # print topology_score_finder(initial_inputs)


    # increase_slope(used_gates)
    # print topology_score_finder(initial_inputs)
    #
    # decrease_slope(used_gates)
    # decrease_slope(used_gates)
    # print topology_score_finder(initial_inputs)

    # csv_file_path = write_back_to_csv(repressor_dict)
    # convert_csv_to_ucf(csv_file_path)


