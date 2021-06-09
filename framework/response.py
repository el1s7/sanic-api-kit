from sanic import Sanic, response as sanic_res

def response_serializer(response):
	if isinstance(response, sanic_res.HTTPResponse):
		return response

	message = {"status": "success", "message": ""}
	
	if(isinstance(response,dict)):
		message = {**message, **response}
	if(isinstance(response,str)):
		message["message"] = response
	if (isinstance(response, bool)):
		message["message"] = "Success" if response else "Failed"
	if(isinstance(response,tuple)):
		message["items"] = response
	
	return sanic_res.json(message)