from sanic import Blueprint, response
from sanic.exceptions import NotFound, MethodNotSupported, Forbidden, Unauthorized
from sanic_routes.exceptions import InvalidParam, InvalidRoute
from . import InvalidUsage
import config

handler = Blueprint('exceptions')

@handler.exception(NotFound)
async def not_found(request, exception):
    return response.json({
			"status": "NotFound",
			"message": "Yep, I totally found the page"
		}
		,status=404)

@handler.exception(MethodNotSupported)
async def not_allowed(request, e):
    return response.json({
			"status": "NotAllowed",
			"message": str(e)
		}
		, status=405)
		
@handler.exception(Forbidden)
async def forbidden(request, e):
    return response.json({
			"status": "Forbidden",
			"message": str(e)
		}
		,status=403)

@handler.exception(InvalidParam)
async def bad_request(request, e):
	
	return response.json({
		"status": "BadRequest",
		"message": "Some fields are invalid",
		"fields": {
			e.field: e.message
		}
	},
	status=400)

@handler.exception(InvalidUsage)
async def invalid_usage(request, e):
	
	return response.json({
		"status": e.status,
		"message": e.message,
		**e.data
	},
	status=e.status_code,
	headers=e.headers)

@handler.exception(Unauthorized)
async def unauthorized(request, e):
	
	return response.json({
		"status": "Unauthorized",
		"message": str(e)
	},
	status=e.status_code,
	headers=e.headers)


'''
@handler.exception(Exception)
async def any_exception(request, e):
	if (config.DEBUG):
		print(e)
	
	return response.json({
		"status": "ServerError",
		"message": "Something went wrong." if not config.DEBUG else str(e)
	},
	status=500)
'''