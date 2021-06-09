import config
import jwt
from time import time
from db import db
from functions import md5, objectify
from sanic.exceptions import Forbidden, Unauthorized
import bcrypt

class Auth:
	
	def __init__(self):
		self.secret = config.JWT_SECRET
		self.expiry = 60 * 60 * 4 # 4 Hours

	def login(self, username, password, ip, ua):
		user = db.getOne('users', '*', ('username=%s OR email=%s', [username, username]))
		
		if not user:
			raise Forbidden("Invalid username or password")

		is_valid_password = bcrypt.checkpw(password.encode(), user.password.encode())

		if not is_valid_password:
			raise Forbidden("Invalid username or password")
		
		return self.get_token(user, ip, ua)

	def get_token(self, user, ip, ua):
		return jwt.encode(
			{
				"user_id": user.id,
				"exp": time() + self.expiry,
				"ip": ip,
				"ua":  self.ua_hash(ua)
			}, self.secret, algorithm="HS256")

	def verify(self, token, ua, ip):
		try:
			user = jwt.decode(token, self.secret, algorithms=["HS256"])
			
			if (user["ua"] != self.ua_hash(ua) or user["ip"] != str(ip)):
				raise jwt.exceptions.InvalidTokenError("Session not matching user browser")

		except jwt.exceptions.InvalidTokenError as jwt_error:
			raise Unauthorized("Auth required.", scheme="Bearer") from jwt_error

		return user

	def ua_hash(self, ua):
		return md5(ua)[:12] # First 12 characters of useragent hash

	def password_hash(self, password):
		return md5(password)

auth = Auth()