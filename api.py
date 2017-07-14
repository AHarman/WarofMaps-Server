import webapp2
from oauth2client import client, crypt
import logging
import credentials
import time

def oauth_failed(requestHandler):
	requestHandler.response.write("Invalid token")
	requestHandler.response.status = 401
	logging.debug("Request authentication failed")
	return

def oauth_required(http_handler_function):
	def inner(requestHandler):
		headers = requestHandler.request.headers
		if "Authorization" in headers and headers["Authorization"].split()[0] == "Bearer:":
			id_token = headers["Authorization"].split()[1]
		else:
			oauth_failed(requestHandler)
			return
		try:
			idinfo = client.verify_id_token(id_token, credentials.client_id)
			if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
				raise crypt.AppIdentityError("Wrong issuer.")
		except crypt.AppIdentityError:
			oauth_failed(requestHandler)
			return

		current_time = int(time.time())
		if not (int(idinfo["iat"]) < current_time and current_time < int(idinfo["exp"])):
			oauth_failed(requestHandler)
			return

		userid = idinfo["sub"]

		logging.debug("Request authentication success")
		return http_handler_function(requestHandler)

	return inner

class Login(webapp2.RequestHandler):
	@oauth_required
	def post(self):
		self.response.write("You've been authenticated!")
		return

app = webapp2.WSGIApplication([
	("/api/login/?", Login),
], debug=True)