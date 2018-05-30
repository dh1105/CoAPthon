import json

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP
from pymongo import MongoClient
import datetime
import pprint


class res(Resource):
    def __init__(self, name="Res", coap_server=None):
        super(res, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        with open("/home/riot/temperature.json", 'r') as f:
            value = json.load(f)
        print(value['e'])
        self.payload = value['e']
        self.resource_type = "temperature"
        self.content_type = "application/json"
        self.interface_type = "if1"

    def render_GET(self, request):
        # print json.dumps({"e": 23.5})
        # self.payload = (
        #     defines.Content_types["application/json"],
        #     json.dumps({"e": [{"n": "temperature", "v": 23.5, "u": "degC"}]}))
        f = open("put_messages.txt", "r")
        self.payload = f.readlines()
        return self

    def render_POST(self, request):
        # d = json.loads(request.payload)
        # print d["message"]
        print "Payload received: ", request.payload
        # f = open("put_messages.txt", "a")
        # f.write(request.payload + "\n")
        # f.close()
        client = MongoClient()
        db = client.payload_storage
        post = {"payload": request.payload,
                "date": datetime.datetime.utcnow()}
        print post
        posts = db.posts
        post_id = posts.insert_one(post).inserted_id
        pprint.pprint(posts.find_one())
        return self

    def render_DELETE(self, request):
        return True

    def render_PUT(self, request):
        print("Payload: %s" % self.payload)
        f = open("clientmes.json", "w")
        data = {"e": self.payload}
        f.write(json.dumps(data))
        f.close()
        return self


class CoAPServer(CoAP):
    def __init__(self, host, port, multicast=False):
        CoAP.__init__(self, (host, port), multicast)
        self.add_resource('lights/', res())
        print "CoAP server started on {}:{}".format(str(host), str(port))
        print self.root.dump()


def main():
    ip = "::1"
    port = 5683
    multicast = False
    server = CoAPServer(ip, port, multicast)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        server.close()


if __name__ == "__main__":
    main()
