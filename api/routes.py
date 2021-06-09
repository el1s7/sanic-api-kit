from sanic_routes import make_routes
import api.controllers as controllers
import api.middlewares as middlewares

routes_config = {
	'login': {
		'method': 'POST',
		'path': '/login',
		'params': {
			'username': {
				'required': True,
				'type': str,
				'help': 'The login username is required',
				'min': 1,
				'max': 20
			},
			'password': {
				'required': True,
				'help': 'The login password is required',
				'type': str,
				'min': 8,
				'max': 32
			}
		}
	},
	'dashboard':{
		'path': '/dashboard',
		'before': ['auth_verify'],
	}
}


routes = make_routes(routes_config ,controllers=controllers, middlewares=middlewares)

'''
# Controllers
def dashboard(request):
	request.params = ''

# Middlewares
def logged(request, response):
	response.headers['X-Limit'] = 'test'
	request.ctx.test = ''

'''
