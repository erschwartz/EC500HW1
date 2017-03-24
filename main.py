from file_parsers import parse_inputs, parse_csv_file, parse_bio_netlist
from file_writers import write_back_to_csv
from optimization_functions import optimize_gates
from ucf_writer import convert_csv_to_ucf
from cello_connection import CelloConnection
from sys import argv

if __name__ == '__main__':
    inputs_filename = argv[1]
    outputs_filename = argv[2]
    verilog_filename = argv[3]
    ucf_filename = argv[4]
    cello_user = argv[5]
    cello_pass = argv[6]

    inputs = parse_inputs(inputs_filename)
    gates = parse_csv_file("resources/gates_Eco1C1G1T1.csv")

    cello = CelloConnection((cello_user, cello_pass))
    original_job_id = "OriginalJob"
    cello.submit_job(original_job_id, verilog_filename, inputs_filename, outputs_filename,
                     "options=-UCF " + ucf_filename + " -plasmid false -eugene false")

    bio_netlist = cello.get_netlist(original_job_id)

    print bio_netlist
    print "\n"

    initial_inputs, used_inputs, used_gates = parse_bio_netlist(bio_netlist, inputs, gates)
    optimize_gates(initial_inputs, used_gates)

    new_gates_file_name = write_back_to_csv(gates)
    new_ucf_filename = convert_csv_to_ucf(new_gates_file_name)
    print "\n"
    print "Modified UCF relative path: " + new_ucf_filename

    modified_job_id = "ModifiedJob"
    cello.submit_job(modified_job_id, verilog_filename, inputs_filename, outputs_filename,
                     "options=-UCF " + new_ucf_filename + " -plasmid false -eugene false")
    print "\n"
    print "Original job ID: " + original_job_id
    print "Modified job ID: " + modified_job_id

