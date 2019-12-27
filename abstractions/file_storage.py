from google.cloud import storage
import os
import tempfile

def put_file(local_file_path, remote_dir_name, remote_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(remote_dir_name)
    blob = bucket.blob(remote_file_name)
    blob.upload_from_filename(local_file_path)

def get_file(remote_dir_name, remote_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(remote_dir_name)
    blob = bucket.get_blob(remote_file_name)
    if blob is None:
        return None

    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    blob.download_to_filename(tmp_file_name)
    return tmp_file_name

def remove_file(remote_dir_name, remote_file_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(remote_dir_name)
    blob = bucket.get_blob(remote_file_name)
    if blob is not None:
        blob.delete()