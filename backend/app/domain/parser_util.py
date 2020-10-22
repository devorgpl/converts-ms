import pickle

from invoiceconverterlib import invoiceconverter as ic


def parse_input_file(filename):
    parser = ic.ffind_format_parser(filename)
    if parser is None:
        print('Skip: ' + filename)
        return
    invoice_obj = ic.fget_invoice(filename, parser)
    ic.fgenerate_epp(filename, invoice_obj)
    return invoice_obj


def generate_epp(filename: str, parsed):
    tempfile = "/tmp/" + filename + ".epp"
    invoice_obj = pickle.loads(parsed['data'])
    ic.fgenerate_epp(filename, invoice_obj)
    return tempfile
