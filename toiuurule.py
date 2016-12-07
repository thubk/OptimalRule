import httplib
import json
import ast
class StaticEntryPusher(object):
 
    def __init__(self, server):
        self.server = server
 
    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
 
    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200
 
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
 
    def rest_call(self, data, action):
        path = '/wm/staticentrypusher/list/00:00:00:00:00:00:00:01/json'
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
 
pusher = StaticEntryPusher('127.0.0.1')
def getip():
	file1 = open("IP.txt", "w")
	file2 = open("ID.txt", "w")
	data = None	
	data = pusher.get(data)
	print 
	print
	number = len(data["00:00:00:00:00:00:00:01"])
	exdata = data["00:00:00:00:00:00:00:01"]
	for i in exdata:
		for key in i:
			if int(i[key]["priority"]) == int(1001):
				file1.writelines(i[key]["match"]["ipv4_src"]+"\n")
				file2.writelines(key+"\n")

	file1.close()

getip()
		

