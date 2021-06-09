from api.models.auth import auth


def auth_verify(request):
	request.ctx.session = auth.verify(
		request.token,
		request.headers.get("user-agent"),
		request.ip
	)