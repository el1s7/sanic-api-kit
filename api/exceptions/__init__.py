class InvalidUsage(Exception):

	def __init__(self, message="Something went wrong", status="error", status_code=403, data = {}):
		self.message = message
		self.data = data
		self.status = status
		self.status_code = status_code
		super().__init__(self.message)
	
	def __str__(self):
	    return '{}'.format(self.message)