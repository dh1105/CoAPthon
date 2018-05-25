from coapthon.server.coap import CoAP
from exampleresources import BasicResource

class CoAPServer(CoAP):
    def __init__(self, host, port):
        print("Server starting")
        CoAP.__init__(self, (host, port))
        self.add_resource('basic/', BasicResource())
        print("Server on, host IP: %s" % host)

def main():
    server = CoAPServer("127.0.0.1", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print "Server Shutdown"
        server.close()
        print "Exiting..."

if __name__ == '__main__':
    main()