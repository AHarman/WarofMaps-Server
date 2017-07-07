import webapp2
from oauth2client import client, crypt
import logging
import credentials


class Testing(webapp2.RequestHandler):
	def get(self):
		given_string = self.request.get("test_string")
		self.response.write("Good golly gosh, you said \"" + given_string + "\"")

class Root(webapp2.RequestHandler):
	def get(self):
		self.response.write("This is a hardcoded string in python!")

class Login(webapp2.RequestHandler):
	def post(self):
		logging.debug("In the Login POST")

		id_token = self.request.body
		try:
			idinfo = client.verify_id_token(id_token, credentials.client_id)
			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise crypt.AppIdentityError("Wrong issuer.")
		except crypt.AppIdentityError:
			self.response.write("Exception! Invalid token! Wrong Issuer!")

		userid = idinfo['sub']
		self.response.write("User id: " + userid)


app = webapp2.WSGIApplication([
	("/api/?", Root),
	("/api/testing/?", Testing),
	("/api/login/?", Login),
], debug=True)