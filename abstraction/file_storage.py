from google.cloud import storage
import os
import tempfile
import abstraction.gcp_constants as constants

storage_client = storage.Client()
bucket = storage_client.get_bucket(constants.BUCKET_NAME)

def put_file(local_file_path, remote_file_path):
    blob = bucket.blob(remote_file_path)
    blob.upload_from_filename(local_file_path)

def get_file(remote_file_path):
    blob = bucket.get_blob(remote_file_path)
    if blob is None:
        return None

    fd, tmp_file_name = tempfile.mkstemp()
    os.close(fd)
    blob.download_to_filename(tmp_file_name)
    return tempfile