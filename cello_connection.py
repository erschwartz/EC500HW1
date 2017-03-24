import requests
import json

CELLO_URL = "http://cellocad.org:8080"


class CelloConnectionError(Exception):
    def __init__(self):
        self.message = "Cello connection refused"


class CelloResultHandle:
    def download_to_file(self, file_name):
        r = requests.get(CELLO_URL + "/results/" +
                         self._job_name + "/" + self._file_name,
                         auth=self._connection.authentication)
        if r.status_code != 200:
            raise CelloConnectionError()
        f = open(file_name, "w")
        f.write(r.text)
        f.close()


class CelloConnection:

    def __init__(self, authentication):
        self.authentication = authentication

    def submit_job(self, job_id, verilog_path, inputs_path, outputs_path, opt_str=""):
        with open(verilog_path, "r") as verilog, open(inputs_path, "r") as inputs, open(outputs_path, "r") as outputs:
            verilog_txt = verilog.read()
            inputs_txt = inputs.read()
            outputs_txt = outputs.read()
            r = requests.post(CELLO_URL + "/submit",
                              auth=self.authentication,
                              data={"id": job_id, "verilog_text": verilog_txt, "input_promoter_data": inputs_txt, "output_gene_data": outputs_txt,"options": opt_str})
            if r.status_code != 200:
                print "Unable to connection to Cello: " + r.text
                raise Exception()

    def get_netlist(self, job_id):
        filename = job_id + "_A000_bionetlist.txt"
        endpoint = CELLO_URL + "/results/" + job_id + "/" + filename
        r = requests.get(endpoint, auth=self.authentication)
        if r.status_code != 200:
            print "Unable to get bionetlist from Cello: " + r.text
            raise Exception()
        return r.text