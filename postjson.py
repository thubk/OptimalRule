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
