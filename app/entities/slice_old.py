#!/usr/bin/python

class Slice:
	def __init__(self):
		self.name = ""
		self.IpAddr = ""
		self.port = ""
		self.mail = ""
		self.passwd = ""
		#self.retour = {"out":"","error":""}

	def Slice(self,element):
		self.name = element['name']
		self.IpAddr = element['IpAddr']
		self.port = element['port']
		self.mail = element['mail']
		if not element['passwd']:
			self.passwd = element['name']
		else:
			self.passwd = element['passwd']
		#self.retour = {"out":"","error":""}

	
	def getName(self):
		return self.name

	def getAdr(self):
		return self.adr

	def getPort(self):
		return self.port

	def getMail(self):
		return self.mail
	
	def setName(self,nom):
		self.nom = nom
	def setIpAddr(self,IpAddr):
		self.IpAddr = IpAddr
	def setPort(self,port):
		self.port = port
	def setMail(self,mail):
		self.mail = mail
	def setPasswd(self,pwd):
		self.passwd = pwd
		
class Flowspace:
    
    def __init__(self):
        self.nom = ""
        self.dpid = ""
        self.priority = 1
        self.match = ""
        self.slice_perm = []
        
    def Flowspace(self,option):
        self.nom = ""
        self.dpid = option["dpid"]
        self.priority = option["priority"]
        self.match = option["match"] #in_port
        self.slice_perm = option["slice_perm"]
        
    # def of getters    
    def getName(self):
        return self.name
        
    def getDpid(self):
        return self.dpid
    
    def getPriority(self):
        return self.priority
        
    def getMatch(self):
        return self.match
    
    def getSlicePerm(self):
        return self.slice_perm
        
    # def of setters    
    def setName(self):
	if self.getDpid() and self.getMatch():
        	self.name = "dpid%s_port%s"%(self.getDpid(),self.getMatch())
         # setting flowspace name look like "dpid1_port1" to make it more sens
	else :
		print "renseigner le dpid et le port"

    def setDpid(self,dpid):
        self.dpid = dpid

    def setPriority(self, prior):
        self.priority = prior
        
    def setMatch(self,match):
        self.match = match
        
    def setSlicePerm(self, perm):
        self.slice_perm = perm
        

