from google.cloud import datastore


def create_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

class SamplesRepo:
    def __init__(self):
        self.db = datastore.Client('skynet-1984')

    def create_multi(self, samples):
        entities = []
        for batch_id, ticker, i_date in samples:
            entity = datastore.Entity(key=self.db.key('samples'))
            entity['batch_id'] = batch_id
            entity['ticker'] = ticker
            entity['date'] = i_date
            entities.append(entity)
        chunks = create_chunks(entities, 500)
        for chunk in chunks:
            self.db.put_multi(chunk)


    def create(self, batch_id, ticker, i_date):
        entity = datastore.Entity(key=self.db.key('samples'))
        entity['batch_id'] = batch_id
        entity['ticker'] = ticker
        entity['date'] = i_date
        self.db.put(entity)

    def get(self, ticker):
        query = self.db.query(kind='samples')
        query.add_filter('ticker', '=', ticker)
        return list(query.fetch())



    def remove(self, batch_id):
        query = self.db.query(kind='samples')
        query.add_filter('batch_id', '=', batch_id)
        query.keys_only()
        entities = list(query.fetch())
        keys = list(map(lambda e: e.key, entities))
        chunks = create_chunks(keys, 500)
        for chunk in chunks:
            self.db.delete_multi(chunk)