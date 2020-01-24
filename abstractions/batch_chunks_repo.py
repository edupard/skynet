from google.cloud import datastore
from abstractions.chunks import create_chunks

class BatchChunksRepo:
    def __init__(self):
        self.db = datastore.Client('skynet-1984')

    def create(self, worker_idx, batch_id, sUuid):
        entity = datastore.Entity(key=self.db.key('batch-chunks'))
        entity['worker_idx'] = worker_idx
        entity['batch_id'] = batch_id
        entity['uuid'] = sUuid
        self.db.put(entity)

    def get_by_batch(self, batch_id):
        query = self.db.query(kind='batch-chunks')
        query.add_filter('batch_id', '=', batch_id)
        return list(query.fetch())

    def get_by_worker(self, worker_idx):
        query = self.db.query(kind='batch-chunks')
        query.add_filter('worker_idx', '=', worker_idx)
        return list(query.fetch())

    def remove_by_worker(self, worker_idx):
        query = self.db.query(kind='batch-chunks')
        query.add_filter('worker_idx', '=', worker_idx)
        query.keys_only()
        entities = list(query.fetch())
        keys = list(map(lambda e: e.key, entities))
        chunks = create_chunks(keys, 500)
        for chunk in chunks:
            self.db.delete_multi(chunk)