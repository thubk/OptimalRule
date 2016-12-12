import httplib
import json
 
class StaticEntryPusher(object):
 
    def __init__(self, server,path):
        self.server = server
 	self.path = path
    def get(self, data):
        ret = self.rest_call({}, 'GET',self.path)
        return json.loads(ret[2])
 
    def set(self, data):
        ret = self.rest_call(data, 'POST',self.path)
        return ret[0] == 200
 
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE',self.path)
        return ret[0] == 200
 
    def rest_call(self, data, action,path):
        #path = '/wm/staticentrypusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret
 
pusher = StaticEntryPusher('127.0.0.1',"/wm/staticentrypusher/json")
flow1 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow1",
    "cookie":"0",
    "priority":"1001",
    "ipv4_src":"192.168.1.105",
    "in_port":"1",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "active":"true",
    "actions":"output=flood"
    }
flow2 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow2",
    "cookie":"0",
    "priority":"1001",
    "ipv4_src":"192.168.1.102",
    "in_port":"1",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "active":"true",
    "actions":"output=flood"
    }
flow3 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"thu",
    "cookie":"0",
    "priority":"1001",
    "ipv4_src":"192.168.1.100",
    "in_port":"1",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "active":"true",
    "actions":"output=flood"
    }
 
flow4 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"nhat",
    "cookie":"0",
    "priority":"1001",
    "in_port":"1",
    "ipv4_src":"192.168.1.101",
    "eth_type":"0x0800",
    "ip_proto":"0x06",
    "active":"true",
    "actions":"output=flood"
    }
pusher.set(flow1)
pusher.set(flow2)
pusher.set(flow3)
pusher.set(flow4)



