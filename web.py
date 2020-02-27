from flask import Flask
from flask_restplus import Api, Resource

import utils.messaging as messaging
import utils.gcs as gcs
import pandas as pd
import os

app = Flask(__name__)
api = Api(app=app)
ns_tasks = api.namespace('jobs', description='Jobs to perform')

if __name__ == "__main__":
    app.run(debug=True)


@ns_tasks.route('/push_tickers')
class PushTickers(Resource):
    def get(self):
        if not os.path.exists('/tmp/tickers.csv'):
            gcs_client = gcs.GcsClient()
            gcs_client.get('tiingo/tickers.csv', '/tmp/tickers.csv')
        df = pd.read_csv('/tmp/tickers.csv')

        publisher = messaging.Publisher()
        publisher.send_messages('tickers', df.ticker.values)
        return 'Success'
