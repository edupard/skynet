from flask import Flask
from flask_restplus import Api, Resource
from env import get_env_variables
from rmq import publish_strings
from tickers import get_tickers


app = Flask(__name__)
api = Api(app=app)
ns_tasks = api.namespace('tasks', description='Operations')

if __name__ == "__main__":
  app.run(debug=True)


@ns_tasks.route('/download')
class Download(Resource):
    def get(self):
        tickers = get_tickers()
        publish_strings(tickers, 'tasks', 'download')
        return 'Success'

@ns_tasks.route('/enrich')
class Enrich(Resource):
    def get(self):
        tickers = get_tickers()
        publish_strings(tickers, 'tasks', 'enrich')
        return 'Success'

@ns_tasks.route('/transpose')
class Transpose(Resource):
    def get(self):
        tickers = get_tickers()
        publish_strings(tickers, 'tasks', 'transpose')
        return 'Success'

@ns_tasks.route('/env')
class Env(Resource):
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
