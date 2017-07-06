import webapp2

class Testing(webapp2.RequestHandler):
	def get(self):
		given_string = self.request.get("test_string")
		self.response.write("Good golly gosh, you said \"" + given_string + "\"")

class Root(webapp2.RequestHandler):
	def get(self):
		self.response.write("This is a hardcoded string in python!")

app = webapp2.WSGIApplication([
	("/api", Root),
    ("/api/testing", Testing),
], debug=True)