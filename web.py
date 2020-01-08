from flask import Flask
from flask_restplus import Api, Resource

import abstractions.tiingo
from abstractions.env import get_env_variables
import job_scheduler as jobs

app = Flask(__name__)
api = Api(app=app)
ns_tasks = api.namespace('jobs', description='Jobs to perform')

if __name__ == "__main__":
  app.run(debug=True)

@ns_tasks.route('/download_tickers')
class DownloadTickers(Resource):
    def get(self):
        abstractions.tiingo.save_tickers()
        return 'Success'


@ns_tasks.route('/download_prices')
class DownloadPrices(Resource):
    def get(self):
        jobs.schedule_download()
        return 'Success'

@ns_tasks.route('/transpose_prices')
class TransposePrices(Resource):
    def get(self):
        jobs.schedule_transpose()
        return 'Success'

@ns_tasks.route('/preprocess_prices')
class PreprocessPrices(Resource):
    def get(self):
        jobs.schedule_preprocess()
        return 'Success'

@ns_tasks.route('/concat_daily_prices')
class ConcatDailyPrices(Resource):
    def get(self):
        jobs.schedule_concat()
        return 'Success'

@ns_tasks.route('/env')
class PrintEnvVariables(Resource):
    def get(this):
        vars = [
            'RMQ_HOST',
            'RMQ_PORT',
            'RMQ_USERNAME',
            'RMQ_PASSWORD',
            'TIINGO_API_KEY',
            'GOOGLE_APPLICATION_CREDENTIALS'
        ]
        return get_env_variables(vars)
