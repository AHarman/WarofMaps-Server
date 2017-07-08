import webapp2
from oauth2client import client, crypt
import logging
import credentials
import time

def oauth_required(http_handler_function):
	def inner(self):
		id_token = self.request.body
		try:
			idinfo = client.verify_id_token(id_token, credentials.client_id)
			if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
				raise crypt.AppIdentityError("Wrong issuer.")
		except crypt.AppIdentityError:
			self.response.write("Exception! Invalid token!")
			self.response.status = "401"
			return

		current_time = int(time.time())
		if not (int(idinfo["iat"]) < current_time and current_time < int(idinfo["exp"])):
			self.response.write("Expired token! Need me a new one!")
			self.response.status = "401"
			return

		userid = idinfo["sub"]
		return http_handler_function(self)

	return inner

class Testing(webapp2.RequestHandler):
	def get(self):
		given_string = self.request.get("test_string")
		self.response.write("Good golly gosh, you said \"" + given_string + "\"")

class Root(webapp2.RequestHandler):
	def get(self):
		self.response.write("This is a hardcoded string in python!")

class Login(webapp2.RequestHandler):
	@oauth_required
	def post(self):
		self.response.write("You've been authenticated!")
		return
		
		

app = webapp2.WSGIApplication([
	("/api/?", Root),
	("/api/testing/?", Testing),
	("/api/login/?", Login),
], debug=True)