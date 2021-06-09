from sanic import Sanic, response as sanic_res

def cors(app, origins=[], headers=['*']):
	@app.middleware('response')
	def handle_cors(request, response):
		cors_headers = {}

		origin = request.headers.get("origin")
		if origins == '*':
			cors_headers['Access-Control-Allow-Origin'] = '*'
		elif isinstance(origins,list) and origin in origins:
			cors_headers['Access-Control-Allow-Origin'] = origin

		cors_headers['Access-Control-Allow-Headers'] = ','.join(headers)
		cors_headers['Access-Control-Max-Age'] = 86400


		if request.method.lower() == "options" and not request.name:
			return sanic_res.HTTPResponse(status=204, headers=cors_headers)
		else:
			response.headers.update(cors_headers)