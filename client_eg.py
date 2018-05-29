import socket

from coapthon.client.coap import CoAP
from coapthon.client.helperclient import HelperClient
from coapthon.messages.message import Message
from coapthon.utils import parse_uri


class CoAPclient(CoAP):
    def __init__(self, host, port, message):
        CoAP.__init__(self, server=(host, port), starting_mid=None, callback=None)
        try:
            self.send_message(message)
        except Exception as e:
            print "Exception: ", str(e)
            self.close()


def main():
    global client
    host, port, path = parse_uri("coap://[::1]:5683/lights")
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
        print "Host:", tmp
    except socket.gaierror:
        print ("Exception")
        pass
    msg = Message()
    # msg.source = (host, port)
    # msg.destination = ('192.168.103.137', 5683)
    # msg.type = defines.Types['CON']
    msg.payload = '{"message": "Hello"}'
    # msg.code = 2
    # print msg.pretty_print()

    try:
        client = HelperClient(server=(host, port))
        response = client.get(path)
        print response.pretty_print()
        response = client.post(path, msg.payload, timeout=10)
        print response.pretty_print()
        response = client.delete(path)
        print response.pretty_print()
        client.close()
        # client = CoAPclient(host, port, msg)
    except Exception as e:
        print "Exception: ", str(e)
        client.close()


if __name__ == "__main__":
    main()
