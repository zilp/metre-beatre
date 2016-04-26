'''
Created on Apr. 24, 2016

@author: shilpa
'''

#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import main

PORT_NUMBER = 8080

display_text = '''
	<html>
	  <header>
		  <title>METRE-BEATRE</title>
			 <style>
				  body {
					font-family: Helvetica;
					font-size: 16px;
					text-align: center;
				  }
				  h1 {
				  	font-weight: 100;
				  }
			</style>
	  </header>
		<body>
		  <h1>METRE-BEATRE <br/> <span style = "font-size: 20px"> guesses a poem's meter + tells you all sorts of other interesting things! </span> </h1>
			<form method="POST" action="/">
				<label>Insert URL of poem:</label> <br/>
				<input type="text" name="poem"/> <br/>
				<input type="submit" value="Send"/>
			</form>
			 facts about poem:<br/>%s
		</body>
	</html>
	'''

class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/server_form.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(display_text % "")
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		try:
			if self.path=="/":
				form = cgi.FieldStorage(
					fp=self.rfile,
					headers=self.headers,
					environ={'REQUEST_METHOD':'POST',
			                 'CONTENT_TYPE':self.headers['Content-Type'],
				})

				print "Poem: %s" % form["poem"].value
				poem = form["poem"].value
				self.send_response(200)
				self.end_headers()
				self.wfile.write(display_text % main.main(poem))
				return

		except KeyError:
			self.wfile.write(display_text % "Invalid input.")

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
