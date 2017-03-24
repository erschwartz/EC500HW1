import os

def write_back_to_csv(gate_dict):
    """
    This function is responsible for writing back the gates to a CSV file. We do this by first appending the csv_labels to the list,
    and then appending all of the gates we used to the list. We felt that directly editing the CSV would be easier than parsing the JSON.
    :param gate_dict: The dictionary of gates that needs to be written back to CSV.
    :return: The file name of the newly created csv file.
    """
    csv_labels = "name,type,color,promoter,promoterDNA,ribozyme,ribozymeDNA,rbs,rbsDNA,cds,cdsDNA,terminator,terminatorDNA,ymax,ymin,K,n,IL,IH,equation"
    alphabetical_keys = sorted(gate_dict.keys())
    csv_strings = [csv_labels]
    for key in alphabetical_keys:
        gate = gate_dict[key]
        csv_list = [gate.name,
                    gate.type,
                    gate.color,
                    gate.promoter,
                    gate.promoter_dna,
                    gate.ribozyme,
                    gate.ribozyme_dna,
                    gate.rbs,
                    gate.rbs_dna,
                    gate.cds,
                    gate.cds_dna,
                    gate.terminator,
                    gate.terminator_dna,
                    gate.ymax,
                    gate.ymin,
                    gate.k,
                    gate.n,
                    gate.il,
                    gate.ih,
                    gate.equation]
        csv_string = ",".join(csv_list)
        csv_strings.append(csv_string)

    csv = "\n".join(csv_strings)
    file_name = "new_file.csv"

    file = open(file_name, "w")
    file.write(str(csv))
    file.close()

    script_dir = os.path.dirname(__file__)
    csv_file_name = os.path.join(script_dir, file_name)
    return csv_file_name
