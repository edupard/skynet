from google.cloud import datastore

class ChunksRepo:
    def __init__(self):
        self.db = datastore.Client('skynet-1984')

    def store_chunk(self, date, sUuid):
        entity = datastore.Entity(key=self.db.key('chunks'))
        entity['date'] = date
        entity['uuid'] = sUuid
        self.db.put(entity)

    def get_chunks(self, date):
        query = self.db.query(kind='chunks')
        query.add_filter('date', '=', date)
        return list(query.fetch())
