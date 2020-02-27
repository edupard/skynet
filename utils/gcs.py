from google.cloud import storage

class GcsClient():
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.get_bucket('skynet-1984-data')

    def save(self, local_file_path, remote_file_path):
        blob = self.bucket.blob(remote_file_path)
        blob.upload_from_filename(local_file_path)

    def get(self, remote_file_path, local_file_path):
        blob = self.bucket.get_blob(remote_file_path)
        if blob is None:
            return False
        blob.download_to_filename(local_file_path)

    def remove(self, remote_file_path):
        blob = self.bucket.get_blob(remote_file_path)
        if blob is not None:
            blob.delete()
