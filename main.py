from file_parsers import parse_inputs, parse_csv_file, parse_bio_netlist
from file_writers import write_back_to_csv
from cello_client import CtxObject, get_netlist, post_result, cli
from optimization_functions import optimize_gates
from ucf_writer import convert_csv_to_ucf
from datetime import datetime
import os

if __name__ == '__main__':
    inputs = parse_inputs("resources/Inputs.txt")
    gates = parse_csv_file("resources/gates_Eco1C1G1T1.csv")

    original_job_id = str(datetime.now())
    # client_connector(original_job_id, "resources/Inputs.txt", "resources/Outputs.txt", "resources/AND.v", "JSON.UCF.json -plasmid false -eugene false")
    # ctx = CtxObject()
    # submit()
    # original_job_id = str(datetime.now())
    # # bio_netlist = get_netlist(ctx, original_job_id, "resources/Inputs.txt", "resources/Outputs.txt", "resources/AND.v", "JSON.UCF.json -plasmid false -eugene false")
    #
    script_dir =    os.path.dirname(__file__)
    bio_netlist_name = os.path.join(script_dir, "resources/bionetlist.txt")
    bio_netlist_txt = open(bio_netlist_name, 'r').read()


    print bio_netlist_txt
    print "\n"
    #
    initial_inputs, used_inputs, used_gates = parse_bio_netlist(bio_netlist_txt, inputs, gates)
    optimize_gates(initial_inputs, used_gates)

    new_gates_file_name = write_back_to_csv(gates)
    json_file_name = convert_csv_to_ucf(new_gates_file_name)
    print "\n"
    print "Modified UCF relative path: " + json_file_name
    #
    modified_job_id = str(datetime.now())
    # cli(modified_job_id, "resources/Inputs.txt", "resources/Outputs.txt", "resources/0xFE.v", "resources/new_gates.UCF.json -plasmid false -eugene false")
    # post_result(ctx, modified_job_id, "resources/Inputs.txt", "resources/Outputs.txt", "resources/0xFE.v", "resources/new_gates.UCF.json -plasmid false -eugene false")
    print "\n"
    print "Original job ID: " + original_job_id
    print "Modified job ID: " + modified_job_id

