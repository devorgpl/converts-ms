from flask import send_from_directory

from domain.convert_service import create_convert_from_file, find_converts, convert_parse, convert_generate, \
    convert_download_file


def list(request):
    """list of users conversions"""
    pass


def create_from_file(document_file, company_id, user_id):
    """create new conversion with given file"""
    return create_convert_from_file(document_file, company_id, user_id)


def find_all(company_id, user_id):
    result = find_converts(company_id)
    return result


def parse(convert_id, user_id):
    result = convert_parse(convert_id)
    return result


def generate(convert_id, user_id):
    result = convert_generate(convert_id)
    return result


def download(convert_id, component_type, user_id):
    file = convert_download_file(convert_id, component_type)
    return send_from_directory("/tmp", file, as_attachment=True)
