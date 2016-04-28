'''
Created on Apr. 24, 2016

consulted PyMOTW tutorial
'''

# !/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
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
          <h1>METRE-BEATRE <br/>
          <span style = "font-size: 20px">
          guesses a poem's meter + rhyme scheme!
          </span> </h1>
            <form method="POST" action="/">
                <label>
                    Insert URL of poem (on Poets.org or Poetry Foundation):
                </label> <br/>
                <input type="text" name="poem"/> <br/>
                <input type="submit" value="Send"/>
            </form>
            <pre>
             %s
            </pre>
        </body>
    </html>
    '''


class myHandler(BaseHTTPRequestHandler):

    # get request handler
    def do_GET(self):
        if self.path == "/":
            self.path = "/server_form.html"

        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if sendReply is True:
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(display_text % "")
                f.close()
            return

        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    # handles post requests
    def do_POST(self):
        try:
            if self.path == "/":
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
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
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER
    server.serve_forever()

except KeyboardInterrupt:
    print 'Shutting down server...'
    server.socket.close()
