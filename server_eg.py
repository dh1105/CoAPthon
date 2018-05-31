import datetime
import json

from pymongo import MongoClient

from coapthon.resources.resource import Resource
from coapthon.server.coap import CoAP


class res(Resource):
    def __init__(self, name="Res", coap_server=None):
        super(res, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        global client
        client = MongoClient()

    def render_GET(self, request):
        print request.payload
        d = json.loads(request.payload)
        ip = d['IPv6']
        val = client.payload_storage.posts.find(ip)
        arr = []
        for documents in val:
            temp = documents['payload']
            arr.append(temp)
        self.payload = arr
        return self

    def render_POST(self, request):
        mes = json.loads(request.payload)
        print "Payload received: ", mes
        print "Source: ", request.source
        db = client.network_members.members
        if not self.check_member(db, mes['ID']):
            print "Member not found adding"
            self.add_member(db, request, mes)
        else:
            print "Member found"
            if not self.check_ip(db, request.source):
                print "IP different"
                self.update_ip(db, request, mes)
            else:
                print "Same IP"

        id_sensor = mes['ID']
        post = {"Date": datetime.datetime.utcnow(),
                "Message": mes['Message']}
        print post
        insert = db[id_sensor].insert_one(post).inserted_id
        cursor = db[id_sensor].find()
        for docs in cursor:
            print docs
        print insert
        # db = client.payload_storage
        # temp = []
        # post = {"payload": mes['payload'],
        #         "date": datetime.datetime.utcnow()}
        # temp.append(post)
        # print post
        # ip = mes["IPv6"]
        # post_id = client.payload_storage.posts.insert_one({ip: temp})
        # cursor = client.payload_storage.posts.find()
        # for documents in cursor:
        #     print documents
        # print post_id
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

    @staticmethod
    def check_member(db, payload):
        val = db.find_one({"ID": payload})
        print val
        if val is None:
            return False
        else:
            return True

    @staticmethod
    def add_member(db, request, d):
        val = {"ID": d['ID'],
               "Date": datetime.datetime.utcnow(),
               "IP": request.source}
        db.insert_one(val)
        print "Member added"

    @staticmethod
    def check_ip(db, source):
        val = db.find({"IP": source})
        if val is None:
            return False
        else:
            return True

    @staticmethod
    def update_ip(db, request, d):
        db.update_one({"ID": d['ID']}, {"$set": {"IP": request.source}})
        print "IP updated"


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
