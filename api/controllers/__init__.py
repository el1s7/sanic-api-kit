from sanic import response
from sanic.exceptions import Forbidden
from functions import md5, objectify
from db import db
from api.models.auth import auth


async def login(request):
	params = request.ctx.params

	token = auth.login(
		params.username,
		params.password,
		request.ip,
		request.headers.get("user-agent")
    )

	return {
		"message": "Logged in successfully",
		"token": token
	}
	
async def dashboard(request):
	params = request.ctx.params
	session = request.ctx.session
	
	return "Welcome to your dashboard"