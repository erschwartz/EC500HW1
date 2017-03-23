import requests
import json
import sys
import os
import click
from requests.auth import HTTPBasicAuth
from Bio import SeqIO
from ucf_writer import convert_csv_to_ucf
import io
import re

class CtxObject(object):
    def __init__(self):
        self.url_root = "http://cellocad.org:8080"

        self.username = os.environ.get('CELLOUSER')
        self.password = os.environ.get('CELLOPASS')

        self.auth = HTTPBasicAuth(self.username, self.password)


def result(r):
    click.echo(click.style(str(r.status_code), fg='green' ))
    try:
        arr = json.loads(r.text)
        click.echo(json.dumps(arr, indent=4))
    except:
        click.echo(r.text)


@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """Command-line interface for Cello genetic circuit design"""
    print "hey"
    ctx.obj = CtxObject()



@cli.command()
@click.option('--jobid', type=click.STRING, help='job name.')
@click.option('--keyword', type=click.STRING, help='file name contains substring.')
@click.option('--extension', type=click.STRING, help='file name ends with substring.')
@click.option('--filename', type=click.STRING, help='file name.')
@click.pass_context
def get_results(ctx, jobid, keyword, extension, filename):

    if jobid == None:
        endpoint = ctx.obj.url_root + "/results"
        r = requests.get(endpoint, auth=ctx.obj.auth)
        result(r)

    elif jobid != None and filename == None:
        params = {}
        if keyword:
            params['keyword'] = keyword
        if extension:
            params['extension'] = extension

        endpoint = ctx.obj.url_root + "/results/" + jobid
        r = requests.get(endpoint, params=params, auth=ctx.obj.auth)
        result(r)

    elif jobid != None and filename != None:
        endpoint = ctx.obj.url_root + "/results/" + jobid + "/" + filename
        r = requests.get(endpoint, auth=ctx.obj.auth)
        result(r)



@cli.command()
@click.option('--name', type=click.STRING, help='promoter name.')
@click.pass_context
def get_inputs(ctx, name):

    if name:
        filename = "input_" + name + ".txt"
        endpoint = ctx.obj.url_root + "/in_out/" + filename
        r = requests.get(endpoint, auth=ctx.obj.auth)
        result(r)

    else:
        params = {}
        params['keyword'] = "input_"
        params['extension'] = "txt"
        endpoint = ctx.obj.url_root + "/in_out"
        r = requests.get(endpoint, params=params, auth=ctx.obj.auth)
        result(r)


@cli.command()
@click.pass_context
@click.option('--name', type=click.STRING, help='output name.')
def get_outputs(ctx, name):

    if name:
        filename = "output_" + name + ".txt"
        endpoint = ctx.obj.url_root + "/in_out/" + filename
        r = requests.get(endpoint, auth=ctx.obj.auth)
        result(r)

    else:
        params = {}
        params['keyword'] = "output_"
        params['extension'] = "txt"
        endpoint = ctx.obj.url_root + "/in_out"
        r = requests.get(endpoint, params=params, auth=ctx.obj.auth)
        result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='promoter name.')
@click.option('--low', type=click.FLOAT, required=True, help='low REU.')
@click.option('--high', type=click.FLOAT, required=True, help='high REU.')
@click.option('--dnaseq', type=click.STRING, required=True, help='dna sequence.')
@click.pass_context
def post_input(ctx, name, low, high, dnaseq):
    filename = "input_" + name + ".txt"
    input_string = name + " " + str(low) + " " + str(high) + " " + dnaseq + "\n"
    params = {}
    params['filetext'] = input_string
    endpoint = ctx.obj.url_root + "/in_out/" + filename
    r = requests.post(endpoint, params=params, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='output name.')
@click.option('--dnaseq', type=click.STRING, required=True, help='dna sequence.')
@click.pass_context
def post_output(ctx, name, dnaseq):
    filename = "output_" + name + ".txt"
    output_string = name + " " + dnaseq + "\n"
    params = {}
    params['filetext'] = output_string
    endpoint = ctx.obj.url_root + "/in_out/" + filename
    r = requests.post(endpoint, params=params, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='promoter name.')
@click.pass_context
def delete_input(ctx, name):
    filename = "input_" + name + ".txt"
    endpoint = ctx.obj.url_root + "/in_out/" + filename
    r = requests.delete(endpoint, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='output name.')
@click.pass_context
def delete_output(ctx, name):
    filename = "output_" + name + ".txt"
    endpoint = ctx.obj.url_root + "/in_out/" + filename
    r = requests.delete(endpoint, auth=ctx.obj.auth)
    result(r)




@cli.command()
@click.option('--verilog', type=click.Path(exists=True), required=True, help='verilog file path.')
@click.pass_context
def netsynth(ctx, verilog):
    endpoint = ctx.obj.url_root + "/netsynth"
    verilog_text = open(verilog, 'r').read()

    params = {}
    params['verilog_text'] = verilog_text

    r = requests.post(endpoint, params=params, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--jobid', type=click.STRING, required=True, help='job id/name.')
@click.option('--verilog', type=click.Path(exists=True), required=True, help='verilog file.')
@click.option('--inputs', type=click.Path(exists=True), required=True, help='input promoters file.')
@click.option('--outputs', type=click.Path(exists=True), required=True, help='output genes file.')
@click.option('--options', type=click.STRING, help='additional dash-separated options.')
@click.pass_context
def submit(ctx, jobid, verilog, inputs, outputs, options):

    endpoint = ctx.obj.url_root + "/submit"

    inputs_text = open(inputs, 'r').read()
    outputs_text = open(outputs, 'r').read()
    verilog_text = open(verilog, 'r').read()


    params = {}
    params['id'] = jobid
    params['input_promoter_data'] = inputs_text
    params['output_gene_data'] = outputs_text
    params['verilog_text'] = verilog_text
    params['options'] = options

    r = requests.post(endpoint, params=params, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--jobid', type=click.STRING, required=True, help='job id/name.')
@click.option('--assignment', type=click.STRING, help='e.g. A000')
@click.pass_context
def show_parts(ctx, jobid, assignment):

    params = {}
    if assignment:
        if len(assignment) is not 4 or not assignment.startswith('A'):
            click.echo('invalid assignment name')
            return
        else:
            params['keyword'] = assignment

    params['extension'] = 'part_list.txt'

    endpoint = ctx.obj.url_root + "/results/" + jobid
    r = requests.get(endpoint, params=params, auth=ctx.obj.auth)
    if r.status_code is 200:
        filenames = json.loads(r.text)

        for filename in filenames:
            endpoint = ctx.obj.url_root + "/results/" + jobid + "/" + filename
            r = requests.get(endpoint, auth=ctx.obj.auth)
            name = r.text.split('[')[0]
            parts = '[' + r.text.split('[')[1]
            parts = parts.replace('[', '[\"')
            parts = parts.replace(']', '\"]')
            parts = parts.replace(', ', '\", \"')
            parts = json.loads(parts)
            click.echo(json.dumps(parts, indent=4))



@click.pass_context
def show_files_contents(ctx, jobid, assignment, extension):
    params = {}
    if assignment:
        if len(assignment) is not 4 or not assignment.startswith('A'):
            click.echo('invalid assignment name')
            return
        else:
            params['keyword'] = assignment

    params['extension'] = extension


    endpoint = ctx.obj.url_root + "/results/" + jobid
    r = requests.get(endpoint, params=params, auth=ctx.obj.auth)
    if r.status_code is 200:
        filenames = json.loads(r.text)

        for filename in filenames:
            endpoint = ctx.obj.url_root + "/results/" + jobid + "/" + filename
            r = requests.get(endpoint, auth=ctx.obj.auth)
            click.echo(r.text)
            click.echo("\n================================================================================\n")


@cli.command()
@click.option('--jobid', type=click.STRING, required=True, help='job id/name.')
@click.option('--assignment', type=click.STRING, help='e.g. A000')
@click.pass_context
def show_circuit_info(ctx, jobid, assignment):
    ctx.invoke(show_files_contents, jobid=jobid, assignment=assignment, extension='logic_circuit.txt')



@cli.command()
@click.option('--jobid', type=click.STRING, required=True, help='job id/name.')
@click.option('--assignment', type=click.STRING, help='e.g. A000')
@click.pass_context
def show_reu_table(ctx, jobid, assignment):
    ctx.invoke(show_files_contents, jobid=jobid, assignment=assignment, extension='reutable.txt')


@cli.command()
@click.option('--jobid', type=click.STRING, required=True, help='job id/name.')
@click.option('--filename', type=click.STRING, required=True, help='file name (.ape)')
@click.option('--seq', is_flag=True, help='also print the dna sequence')
@click.pass_context
def read_genbank(ctx, jobid, filename, seq):

    r = requests.get(ctx.obj.url_root + "/resultsroot", auth=ctx.obj.auth)
    server_root = r.text
    filepath = server_root + "/" + ctx.obj.username + "/" + jobid + "/" + filename

    gb_record = SeqIO.read(open(filepath,"r"), "genbank")

    if seq:
        for gb_feature in gb_record.features:
            print gb_feature.location, gb_feature.type, gb_feature.qualifiers['label'], gb_feature.extract(gb_record.seq)
    else:
        for gb_feature in gb_record.features:
            print gb_feature.location, gb_feature.type, gb_feature.qualifiers['label']


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='UCF name')
@click.option('--filepath', type=click.Path(exists=True), required=True, help='UCF file.')
@click.pass_context
def post_ucf(ctx, name, filepath):

    if not name.endswith(".UCF.json"):
        click.echo("UCF file name must end with the extension .UCF.json")
        return

    filetext = open(filepath, 'r').read()
    filejson = json.loads(filetext)

    params = {}
    params['filetext'] = json.dumps(filejson)

    endpoint = ctx.obj.url_root + "/ucf/" + name
    r = requests.post(endpoint, data=params, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='UCF name')
@click.pass_context
def validate_ucf(ctx, name):

    if not name.endswith(".UCF.json"):
        click.echo("UCF file name must end with the extension .UCF.json")
        return

    endpoint = ctx.obj.url_root + "/ucf/" + name + "/validate"
    r = requests.get(endpoint, auth=ctx.obj.auth)
    result(r)


@cli.command()
@click.option('--name', type=click.STRING, required=True, help='UCF name')
@click.pass_context
def delete_ucf(ctx, name):

    if not name.endswith(".UCF.json"):
        click.echo("UCF file name must end with the extension .UCF.json")
        return

    endpoint = ctx.obj.url_root + "/ucf/" + name
    r = requests.delete(endpoint, auth=ctx.obj.auth)
    result(r)



def get_netlist(ctx, jobid, inputs, outputs, verilog, options):
    endpoint = ctx.url_root + "/submit"

    script_dir = os.path.dirname(__file__)
    inputs = os.path.join(script_dir, inputs)
    outputs = os.path.join(script_dir, outputs)
    verilog = os.path.join(script_dir, verilog)

    inputs_text = open(inputs, 'r').read()
    outputs_text = open(outputs, 'r').read()
    verilog_text = open(verilog, 'r').read()

    params = {}
    params['id'] = jobid
    params['input_promoter_data'] = inputs_text
    params['output_gene_data'] = outputs_text
    params['verilog_text'] = verilog_text
    params['options'] = options

    r = requests.post(endpoint, params=params, auth=ctx.auth)


    filename = jobid + "_A000_bionetlist.txt"
    endpoint = ctx.url_root + "/results/" + jobid + "/" + filename
    r = requests.get(endpoint, auth=ctx.auth)

    return r.text
    #return parse_bio_netlist(r.text)

def parse_bio_netlist(file_contents):
    list = []
    for string in file_contents.split().reverse():
        if not string.isdigit():
            list.append(string)

    return list

def parse_csv_file(csv_file_name):
    script_dir = os.path.dirname(__file__)
    csv_file_name = os.path.join(script_dir, csv_file_name)
    csv_text = inputs_text = open(csv_file_name, 'r').read()
    csv_list = csv_text.split()

    first_line = True
    repressor_dict = {}
    for csv in csv_list:
        if first_line:
            first_line = False
        else:
            string_list = csv.split(",")
            repressor_dict[string_list[0]] = Repressor(string_list[0],
                                                       string_list[1],
                                                       string_list[2],
                                                       string_list[3],
                                                       string_list[4],
                                                       string_list[5],
                                                       string_list[6],
                                                       string_list[7],
                                                       string_list[8],
                                                       string_list[9],
                                                       string_list[10],
                                                       string_list[11],
                                                       string_list[12],
                                                       string_list[13],
                                                       string_list[14],
                                                       string_list[15],
                                                       string_list[16],
                                                       string_list[17],
                                                       string_list[18],
                                                       string_list[19],
                                                       None,
                                                       None)

    return repressor_dict

class Repressor:
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

def improve_scores(repressor_dict, repressor_list):
    for repressor in repressor_list:
        if repressor_dict.get(repressor) is None:
            print repressor
        # print repressor_dict[repressor].equation


def improve_score(repressor):

    if repressor.ymax - repressor.ymin > 5:
        pass


def make_promoter_more_active(repressor):
    pass

def make_promoter_less_active(repressor):
    pass

def write_back_to_csv(repressor_dict):
    csv_labels = "name,type,color,promoter,promoterDNA,ribozyme,ribozymeDNA,rbs,rbsDNA,cds,cdsDNA,terminator,terminatorDNA,ymax,ymin,K,n,IL,IH,equation"
    alphabetical_keys = sorted(repressor_dict.keys())
    csv_strings = [csv_labels]
    for key in alphabetical_keys:
        repressor = repressor_dict[key]
        csv_list = [repressor.name,
                    repressor.type,
                    repressor.color,
                    repressor.promoter,
                    repressor.promoter_dna,
                    repressor.ribozyme,
                    repressor.ribozyme_dna,
                    repressor.rbs,
                    repressor.rbs_dna,
                    repressor.cds,
                    repressor.cds_dna,
                    repressor.terminator,
                    repressor.terminator_dna,
                    repressor.ymax,
                    repressor.ymin,
                    repressor.k,
                    repressor.n,
                    repressor.il,
                    repressor.ih,
                    repressor.equation]
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


def parse_inputs(inputs_file_name):
    script_dir = os.path.dirname(__file__)
    inputs_file_name = os.path.join(script_dir, inputs_file_name)
    inputs_text = inputs_text = open(inputs_file_name, 'r').read()
    input_str_list = inputs_text.split("\n")
    inputs = {}

    for input in input_str_list:
        input_strs = input.split()
        if len(input_strs) > 0:
            input = Input(input_strs[0],
                          input_strs[1],
                          input_strs[2],
                          None)
            inputs[input.name] = input

    return inputs

def parse_outputs(output_file_name):
    script_dir = os.path.dirname(__file__)
    output_file_name = os.path.join(script_dir, output_file_name)
    outputs_txt = open(output_file_name, 'r').read()
    output_str_list = outputs_txt.split("\n")
    outputs = {}

    for output in output_str_list:
        output_strs = output.split()
        if len(output_strs) > 0:
            output = Output(output_strs[0], None)
            outputs[output.name] = output

    return outputs


def parse_bio_netlist(bio_netlist, inputs, gates):
    bio_netlist_strs = bio_netlist.split("\n")
    bio_netlist_strs.reverse()
    # print bio_netlist_strs
    if len(bio_netlist_strs) <= 0:
        print "Error parsing netlist"
        return

    def parse_single_gate_input(bionetlist_str_list):
        input_one = None
        gate = gates[bio_netlist_str_list[0]] if bio_netlist_str_list[0] in gates else None
        if bio_netlist_str_list[1] in inputs:
            input_one = inputs[bio_netlist_str_list[1]]
        else:
            input_one = Input(bio_netlist_str_list[1], None, None, gate)
            inputs[bio_netlist_str_list[1]] = input_one

            gate_ext = input_one.name[1:]
            actual_gate = gates[[key for key, value in gates.iteritems() if gate_ext in key][0]]
            actual_gate.output = input_one

        input_one.gate = gate
        if gate is not None:
            gate.inputs = [input_one]
            print 'Input one: ' + input_one.name + ' with gate: ' + gate.name

    def parse_double_gate_input(bionetlist_str_list):
        input_one = None
        input_two = None
        gate = gates[bio_netlist_str_list[0]] if bio_netlist_str_list[0] in gates else None
        if bio_netlist_str_list[1] in inputs:
            input_one = inputs[bio_netlist_str_list[1]]
        else:
            input_one = Input(bio_netlist_str_list[1], None, None, gate)
            inputs[bio_netlist_str_list[1]] = input_one

            gate_ext = input_one.name[1:]
            actual_gate = gates[[key for key, value in gates.iteritems() if gate_ext in key][0]]
            actual_gate.output = input_one

        if bio_netlist_str_list[2] in inputs:
            input_two = inputs[bio_netlist_str_list[2]]
        else:
            input_two = Input(bio_netlist_str_list[2], None, None, gate)
            inputs[bio_netlist_str_list[2]] = input_one

            gate_ext = input_two.name[1:]
            actual_gate = gates[[key for key, value in gates.iteritems() if gate_ext in key][0]]
            actual_gate.output = input_two

        input_one.gate = gate
        input_two.gate = gate
        if gate is not None:
            gate.inputs = [input_one, input_two]
            print 'Input one: ' + input_one.name + ' Input two: ' + input_two.name + ' with gate: ' + gate.name

    bio_netlist_index = 0
    while not bio_netlist_strs[bio_netlist_index].split()[1].isdigit(): #until we get binary (2+ digits)
        bio_netlist_str_list = bio_netlist_strs[bio_netlist_index].split()
        if len(bio_netlist_str_list) == 2:
            parse_single_gate_input(bio_netlist_str_list)
        else:
            parse_double_gate_input(bio_netlist_str_list)
        bio_netlist_index += 1

if __name__ == '__main__':
    inputs = parse_inputs("resources/Inputs.txt")
    gates = parse_csv_file("resources/gates_Eco1C1G1T1.csv")

    ctx = CtxObject()
    # bio_netlist = get_netlist(ctx, "j4", "resources/Inputs.txt", "resources/Outputs.txt", "resources/0xFE.v", "JSON.UCF.json -plasmid false -eugene false")

    script_dir = os.path.dirname(__file__)
    bio_netlist_name = os.path.join(script_dir, "resources/bionetlist.txt")
    bio_netlist_txt = open(bio_netlist_name, 'r').read()

    print bio_netlist_txt

    parse_bio_netlist(bio_netlist_txt, inputs, gates)

    # csv_file_path = write_back_to_csv(repressor_dict)
    # convert_csv_to_ucf(csv_file_path)


