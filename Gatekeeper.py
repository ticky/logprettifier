# Gatekeeper.py
# CGI wrapper allowing buffering output and setting headers and content independently

class Gatekeeper:

    def __init__(self):
        self.Headers = {}
        self.Body    = []
        self.Headers["X-Powered-By"] = "Python, Gatekeeper.py"
        self.Headers["Content-Type"] = "text/html"

    def addHeader(self, name, value):
        self.Headers[name] = value

    def addBody(self, value):
        self.Body.append(value)

    def flush(self):
        for name in self.Headers:
            print(name+": "+self.Headers[name])

        print ""

        for value in self.Body:
            print(value)

    def __del__(self):
        self.flush()