import math
import time
from toiuurule import *
from postjson import *
prevent_flow = {}
name = 0
time

allow_flow ={}
allow_flow["switch"] = "00:00:00:00:00:00:00:01"
allow_flow["name"] = "" 
allow_flow["cookie"] = "0"
allow_flow["priority"] = "2000"
allow_flow["in_port"] = "1"
allow_flow["ipv4_src"] = ""
allow_flow["eth_type"] = "0x0800"
allow_flow["active"] = "true"
allow_flow["actions"] = "output=3"

prevent_flow["switch"] = "00:00:00:00:00:00:00:01"
prevent_flow["name"] = "" 
prevent_flow["cookie"] = "0"
prevent_flow["priority"] = "1500"
prevent_flow["in_port"] = "1"
prevent_flow["ipv4_src"] = ""
prevent_flow["eth_type"] = "0x0800"
prevent_flow["active"] = "true"
prevent_flow["actions"] = ""

delete_flow = {}
delete_flow["switch"] = "00:00:00:00:00:00:00:01"
delete_flow["name"] = ""
flow3 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow_mod_1",
    "cookie":"0",
    "priority":"1001",
    "ipv4_src":"192.168.1.100",
    "in_port":"1",
    "eth_type":"0x0800",
    "active":"true",
    "actions":"output=flood"
    }
 
flow4 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"nhat",
    "cookie":"0",
    "priority":"1001",
    "in_port":"1",
    "ipv4_src":"192.168.1.1",
    "eth_type":"0x0800",
    "active":"true",
    "actions":"output=flood"
    }
class Node:
    """Class Node"""
    def __init__(self, data,counter,wildcard,listIP,subnet):
	    self.left = None
	    self.data = data
	    self.counter = counter
	    self.listIP = listIP
	    self.wildcard = wildcard
	    self.subnet = subnet
	    self.right = None


class Tree:

    def createNode(self, data,counter,wildcard,listip,subnet):
        return Node(data,counter,wildcard,listip,subnet)

    def insert(self, node , data,counter,wildcard,listip,subnet):
        #if tree is empty , return a root node
        if node is None:
            return self.createNode(data,counter,wildcard,listip,subnet)
        # if data is smaller than parent , insert it into left side
        if data is 0:
            node.left = self.insert(node.left, data, counter,wildcard,listip,subnet)
        else:
            node.right = self.insert(node.right, data , counter,wildcard,listip,subnet)
        return node


    def search(self, node, data):
        # if root is None or root is the search data.
        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)



    def deleteNode(self,node,data):

        # Check if tree is empty.
        if node is None:
            return None

        # searching key into BST.
        if data < node.data:
            node.left = self.deleteNode(node.left, data)
        elif data > node.data:
            node.right = self.deleteNode(node.right, data)
        else: # reach to the node that need to delete from BST.
            if node.left is None and node.right is None:
                del node
            if node.left == None:
                temp = node.right
                del node
                return  temp
            elif node.right == None:
                temp = node.left
                del node
                return temp

        return node

    def traversePostorder(self, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
	    if root.wildcard == 1:
		
		if root.counter == 32:
			prevent_flow["ipv4_src"] = adresstostring(root.listIP[0])
			prevent_flow["name"] = adresstostring(root.listIP[0])
			pusher.set(prevent_flow)
		else:
			prevent_flow["ipv4_src"] = adresstostring(root.listIP[0])+"/"+str(root.counter)
			prevent_flow["name"] = adresstostring(root.listIP[0])
			pusher.set(prevent_flow)
	    self.traversePostorder(root.left)
            self.traversePostorder(root.right)

def recursive(tree,node,data,counter,listip,text_allow):
	number = math.pow( 2, 32-counter + 1)-1
	size = len(listip)
	per = size/number
	#if counter is 32:
	#	return tree.insert(node,data,counter,1,listip)
	if per >= 0.4:
		if counter == 32:
			return tree.insert(node,data,counter,1,listip,"")
		else:
			bo = 0
			subnet = listip[0][0:counter]
			size = 0
			ip = ""
			size = len(str(subnet))
			total = 32 - size
			maxnumber = 0
			maxnumber = math.pow( 2, total)-1
			number = 0
			if size != 32:
				for i in range(0,int(maxnumber+1)):
					ip = subnet + str(bin(number)[2:].zfill(total))
					bo = 0
					for j in listip:
						if ip == j:
							bo = 1
							break
					if bo == 0:
						print ip
						text_allow.writelines(ip+"\n")
						time.sleep(10)
					number = number +1
			return tree.insert(node,data,counter,1,listip,subnet)
	else:
		new0_listip = [];
		new1_listip = [];
		counter0=0;
		counter1=0;
		for i in xrange(0,len(listip)):
			ip = listip[i]
			if int(ip[counter]) == 0:
				new0_listip.insert(counter0,ip)
				counter0 = counter0+1
			else:
				new1_listip.insert(counter1,ip)
				counter1 = counter1+1
		if(node is None):
			if len(new0_listip) is not 0:
				tree.insert(node,0,counter+1,0,new0_listip,"")
				recursive(tree,node,0,counter+1,new0_listip,text_allow)
			if len(new1_listip) is not 0: 
				tree.insert(node,1,counter+1,0,new1_listip,"")
				recursive(tree,node,1,counter+1,new1_listip,text_allow)
		else:
			if len(new0_listip) is not 0:
				tree.insert(node,0,counter0,0,new0_listip,"")
				recursive(tree,node.left,0,counter+1,new0_listip,text_allow)
			if len(new1_listip) is not 0: 
				tree.insert(node,1,counter1,0,new1_listip,"")
				recursive(tree,node.right,1,counter+1,new1_listip,text_allow)
		
	
def adresstostring(adress):
	bit = 0
	temp1 = 0
	temp2 = 0
	temp3 = 0
	temp4 = 0
	for i in range(0,8):
		if (len(adress)-1) >= i:
			if adress[i] is "1":
				bit = 1
			else:
				bit = 0
		else:
			bit =0
		if bit == 1:
			if i == 7:
				temp1 = temp1 + 1
			else:
				temp1 = temp1 + math.pow( 2, (7-i))
	for i in range(8,16):
		if (len(adress)-1) >= i:
			if adress[i] is "1":
				bit = 1
			else:
				bit = 0
		else:
			bit =0
		if bit == 1:
			if i == 15:
				temp2 = temp2 + 1
			else:
				temp2 = temp2 + math.pow( 2, (15-i))
	for i in range(16,24):
		if (len(adress)-1) >= i:
			if adress[i] is "1":
				bit = 1
			else:
				bit = 0
		else:
			bit =0
		if bit == 1:
			if i == 23:
				temp3 = temp3 + 1
			else:
				temp3 = temp3 + math.pow( 2, (23-i))
	for i in range(24,32):
		if (len(adress)-1) >= i:
			if adress[i] is "1":
				bit = 1
			else:
				bit = 0
		else:
			bit =0
		if bit == 1:
			if i == 31:
				temp4 = temp4 + 1
			else:
				temp4 = temp4 + math.pow( 2, (31-i))
	return str(int(temp1)) + "."+ str(int(temp2)) + "." + str(int(temp3)) + "." + str(int(temp4))
subnet = ""
def deleteContent(pfile):

    pfile.seek(0)
    pfile.truncate()
    pfile.seek(0) # I believe this seek is redundant

    return pfile
def run():
    root = None
    tree = Tree()
    getip()
    text_ip = open("IP.txt", "r")
    text_id = open("ID.txt", "r")
    text_allow = open("IP_ALLOW.txt", "w")
    listip = text_ip.readlines()
    listid = text_id.readlines()
    iplist = listip
    if listip is not None:
	    for i in xrange(0,len(listip)):
		ip = '.'.join([bin(int(x)+256)[3:] for x in listip[i].split('.')])
		ip = ip[0:8]+ip[9:17]+ip[18:26]+ip[27:]
		iplist[i] = ip
	    root = tree.insert(root, 0,0,0,listip,[])
	    recursive(tree,root,1,8,iplist,text_allow)
	    tree.traversePostorder(root)
	    for j in listid:
		j = j[0:len(j)-1]
		delete_flow["name"] = j
		pusher.remove("00:00:00:00:00:00:00:01",delete_flow)
    text_allow.close()
    text_allow = open("IP_ALLOW.txt", "r")
    listip_allow = text_allow.readlines()
    print listip_allow
    for j in listip_allow:
	j = j[0:len(j)-1]
	allow_flow["name"] = adresstostring(j)
	allow_flow["ipv4_src"] = adresstostring(j)
	print allow_flow
	pusher.set(allow_flow)
    text_allow.close()
    text_allow = open("IP_ALLOW.txt", "w")
    deleteContent(text_allow)
    text_allow.close()
def main():
	while(1):
		run()
		time.sleep(10)
if __name__ == "__main__":
    main()


