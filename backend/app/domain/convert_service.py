import pickle
from datetime import datetime

from bson import ObjectId
from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists, ResponseError
from werkzeug.datastructures import FileStorage

from domain.convert_model import StorePath, Convert, ConvertMetadata, Component
from domain.parser_util import parse_input_file, generate_epp
from utils.db_utils import converts_collection


def _find_component(convert, role):
    for com in convert['components']:
        if com['role'] == role:
            return com
    return None


def _upload_file_to_store(file, company_id):
    path = StorePath()
    path.bucket = company_id
    path.name = str(ObjectId()) + "_" + file.filename
    minio_client = Minio('localhost:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)
    # Make a bucket with the make_bucket API call.
    try:
        minio_client.make_bucket(path.bucket)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise
    print(file.stream)
    f = file.stream
    f.seek(0, 2)
    length = f.tell()
    f.seek(0)
    try:
        minio_client.put_object(path.bucket, path.name, file.stream, length)
    except ResponseError as err:
        print(err)

    print('uploading ...')
    return path


def create_convert_from_file(file: FileStorage, company_id, user_id):
    convert = Convert()
    convert.company = company_id
    convert.user_created = user_id
    convert.name = file.filename
    convert.global_status = 'upload'
    convert.components = []
    convert.source = 'form'
    convert.date_created = datetime.now()
    convert.metadata = ConvertMetadata()

    store_path = _upload_file_to_store(file, company_id)
    file_component = Component()
    file_component.filename = file.filename
    file_component.type = 'file'
    file_component.status = 'done'
    file_component.role = 'root_file'
    file_component.order = 1
    file_component.store_path = store_path
    convert.components.append(file_component)

    collection = converts_collection()
    print(vars(convert))
    to_dict = convert.to_dict()
    print(to_dict)
    res = collection.insert_one(to_dict)
    print(res.inserted_id)
    print(file.filename)
    print(company_id)
    return str(res.inserted_id)


def find_converts(company_id):
    collection = converts_collection()
    result = collection.find({"company": company_id})
    data = []
    for r in result:
        newres = r
        newres["id"] = str(r["_id"])
        newres["_id"] = None
        for c in newres["components"]:
            c["data"] = None
        data.append(r)
    return data


def _download_temp_file(store_path):
    tempfile = '/tmp/' + store_path['name']
    minio_client = Minio('localhost:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)
    minio_client.fget_object(store_path['bucket'], store_path['name'], tempfile)
    print(tempfile)
    return tempfile


def _insert_component(convert_id, parsed_component: Component):
    collection = converts_collection()
    dict_component = parsed_component.to_dict()
    print(dict_component)
    collection.find_one_and_update({"_id": ObjectId(convert_id)}, {'$push': {'components': dict_component}})
    pass


def convert_parse(convert_id):
    print('parse')
    collection = converts_collection()
    one = collection.find_one({"_id": ObjectId(convert_id)})
    c = _find_component(one, 'root_file')
    tempfile = _download_temp_file(c['store_path'])
    parsed = parse_input_file(tempfile)
    parsed_component = Component()
    parsed_component.type = 'data'
    parsed_component.role = 'parsed'
    parsed_component.order = 2
    parsed_component.status = 'done'
    parsed_component.filename = ''
    parsed_component.data = pickle.dumps(parsed)
    parsed_component.store_path = StorePath()
    parsed_component.store_path.name = ''
    parsed_component.store_path.bucket = ''
    _insert_component(convert_id, parsed_component)
    return 1


def convert_generate(convert_id):
    print('generate')
    collection = converts_collection()
    one = collection.find_one({"_id": ObjectId(convert_id)})
    c = _find_component(one, 'parsed')
    uniq_filename = str(ObjectId()) + "_" + one['name']
    tempfile = generate_epp(uniq_filename, c)

    epp_component: Component = Component()
    epp_component.filename = one['name'] + ".epp"
    epp_component.store_path = StorePath()
    epp_component.store_path.bucket = one['company']
    epp_component.store_path.name = uniq_filename + ".epp"
    epp_component.type = 'file'
    epp_component.role = 'generated'
    epp_component.order = 10
    epp_component.status = 'done'
    minio_client = Minio('localhost:9000',
                         access_key='AKIAIOSFODNN7EXAMPLE',
                         secret_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
                         secure=False)
    minio_client.fput_object(epp_component.store_path.bucket, epp_component.store_path.name, tempfile)
    _insert_component(convert_id, epp_component)
    return 1


def convert_download_file(convert_id, component_type):
    print('download')
    collection = converts_collection()
    one = collection.find_one({"_id": ObjectId(convert_id)})
    c = _find_component(one, component_type)
    _download_temp_file(c['store_path'])
    return c['store_path']['name']
