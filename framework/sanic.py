from sanic import Sanic as BaseSanic
from sanic.response import BaseHTTPResponse, HTTPResponse
from asyncio import CancelledError
from inspect import isawaitable
from sanic.exceptions import ServerError

class Sanic(BaseSanic):
	
	__fake_slots__ = (
		*BaseSanic.__fake_slots__,
		"_response_serializer"
	)
	
	_response_serializer = None
	
	def response_serializer(self, serializer):
		"""
		Register the response serializer. 
		The value returned by a route handler will be serialized by this function.
		The serializer function should return a HTTPResponse.
		:param serializer: callable
		:return: serializer
		"""
	
		self._response_serializer = serializer
		
	
	async def handle_request(self, request):
		"""Take a request from the HTTP Server and return a response object
		to be sent back The HTTP Server only expects a response object, so
		exception handling must be done here
		:param request: HTTP Request object
		:return: Nothing
		"""
		# Define `response` var here to remove warnings about
		# allocation before assignment below.
		response = None
		try:
			# Fetch handler from router
			route, handler, kwargs = self.router.get(
				request.path,
				request.method,
				request.headers.getone("host", None),
			)
	
			request._match_info = kwargs
			request.route = route
	
			if (
				request.stream.request_body  # type: ignore
				and not route.ctx.ignore_body
			):
	
				if hasattr(handler, "is_stream"):
					# Streaming handler: lift the size limit
					request.stream.request_max_size = float(  # type: ignore
						"inf"
					)
				else:
					# Non-streaming handler: preload body
					await request.receive_body()
	
			# -------------------------------------------- #
			# Request Middleware
			# -------------------------------------------- #
			response = await self._run_request_middleware(
				request, request_name=route.name
			)
	
			# No middleware results
			if not response:
				# -------------------------------------------- #
				# Execute Handler
				# -------------------------------------------- #
	
				if handler is None:
					raise ServerError(
						(
							"'None' was returned while requesting a "
							"handler from the router"
						)
					)
	
				# Run response handler
				response = handler(request, **kwargs)
				if isawaitable(response):
					response = await response
				
				if self._response_serializer and callable(self._response_serializer):
					response = self._response_serializer(response)
				
	
			if response:
				response = await request.respond(response)
			else:
				response = request.stream.response  # type: ignore
			# Make sure that response is finished / run StreamingHTTP callback
	
			if isinstance(response, BaseHTTPResponse):
				await response.send(end_stream=True)
			else:
				try:
					# Fastest method for checking if the property exists
					handler.is_websocket  # type: ignore
				except AttributeError:
					raise ServerError(
						f"Invalid response type {response!r} "
						"(need HTTPResponse)"
					)
	
		except CancelledError:
			raise
		except Exception as e:
			# Response Generation Failed
			await self.handle_exception(request, e)