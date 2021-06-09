import config, warnings, json, os
from framework import Sanic, cors, response_serializer
from api.routes import routes
from api.exceptions.handler import handler

if not config.DEBUG:
	warnings.filterwarnings("ignore")

def create_app():
	app = Sanic(__name__)
	app.config.FALLBACK_ERROR_FORMAT = "json"
	app.static('/', './public')
	app.blueprint(routes)
	app.blueprint(handler)
	app.response_serializer(response_serializer)

	cors(app, ['http://localhost:3000','http://192.168.1.11:3000'])

	return app


if __name__ == '__main__':
	app = create_app()
	app.run(host="0.0.0.0", port=8001, debug=config.DEBUG)