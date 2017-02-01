#!/usr/bin/python
from slice import *
from subprocess import *
import shlex
import ast
"""
cette classe permet manipuler les slices et les flowspace
version 1.0
realise par N'ZI KOFFI YANNICK
TEL: 0769019553
MAIL : nykyko@gmail.com
DATE : 08/01/17

"""
SLICE = "M_slice"
FLOWSPACE = "M_flowspace"
MASTER = "master"
perm=""
class Manager:
	def __init__(self):
		self.fonction = ""
		self.back = {"out":"","error":""}

	def Manager(self,fct):
		self.fonction = fct
		self.back = {"out":[],"error":""}
	
	def setFonction(self,fct):
		self.fonction = fct

	def getFonction(self):
		return self.fonction
	####################################################################################################
    
	# dealing with slices
    
	def createSlice(self,s):
	   	global SLICE
		if self.fonction == SLICE:
			  if s.getName() and s.getIpAddr() and s.getPort() and s.getMail() and s.getPasswd():
				var="fvctl -f /dev/null add-slice %s tcp:%s:%s %s -p %s"%(s.getName(),s.getIpAddr(),s.getPort(),s.getMail(),s.getPasswd())
				param = shlex.split(var) 
				proc=Popen(param,stdout=PIPE,stderr=PIPE)
				self.back["out"] , self.back["error"] = proc.communicate()
			  else:
					self.back['error'] = "il faut renseiger toutes les informations du slice"
		else:
			self.back['error'] = "ce manager ne peut creer de slice : c'est un manager de flowspace"
	####################################################################################################
	def deleteSlice(self,s):
		if self.fonction == SLICE :
			if s.getName():
				param = "fvctl -f /dev/null remove-slice %s" % (s.getName())
				cmd = shlex.split(param)
				proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
				self.back["out"],self.back["error"] = proc.communicate()
			else:
				self.back["error"] = "renseigner le nom du slice a supprimer"


	####################################################################################################
	def getOneSliceStats(self,s) : 
		if self.fonction == SLICE :
			if s.getName():
				param = "fvctl -f /dev/null list-slice-stats %s" % (s.getName())
				cmd = shlex.split(param)
				proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
				self.back["out"],self.back["error"] = proc.communicate()
			else:
				self.back["error"] = "renseigner le nom du slice a selectionner"

	####################################################################################################
	def getSliceHealth(self,s) : 
		if self.fonction == SLICE :
			if s.getName():
				param = "fvctl -f /dev/null list-slice-health %s" % (s.getName())
				cmd = shlex.split(param)
				proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
				self.back["out"] , self.back["error"] = proc.communicate()
			else:
				self.back["error"] = "renseigner le nom du slice a selectionner"	
	####################################################################################################

	def getAllSlices(self):	
		if self.fonction == SLICE :
			param = "fvctl -f /dev/null list-slices"
			cmd = shlex.split(param)
			proc = Popen(cmd,stdout=PIPE,stderr=PIPE)

			self.back["out"] , self.back["error"] = proc.communicate()
	###################################################################################################

	def getSliceInfo(self,s): 
		if self.fonction == SLICE :
			if s.getName():
				param = "fvctl -f /dev/null list-slice-info %s" % (s.getName())
				cmd = shlex.split(param)
				proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
				self.back["out"] , self.back["error"] = proc.communicate()
			else:
				self.back["error"] = "renseigner le nom du slice a selectionner"

	#####################################################################################################

	def getSwitchsDpid(self):
		if self.fonction == MASTER:
			#param = "fvctl -f /dev/null  list-datapaths | tail -n +2 | cut -d : -f 2-|wc -l"
			param0 = "fvctl -f /dev/null  list-datapaths"
			param1 ="tail -n +2"
			param2 = "cut -d : -f 2-"
			#cmd = shlex.split(param)
			#print cmd
			p0 = Popen(shlex.split(param0),stdout=PIPE,stderr=PIPE)
			p1 = Popen(shlex.split(param1),stdin=p0.stdout,stdout=PIPE)
			p2 = Popen(shlex.split(param2),stdin=p1.stdout,stdout=PIPE)
			#p3 = Popen(shlex.split(param3),stdin=p2.stdout)
			out,self.back["error"]=p2.communicate()
			out = out.strip("\n").split("\n")
			i=1
			t={}
			for dpid in out :
				t["switch_0%s"%(i)]=int(dpid[-2:])
				i+=1
			self.back["out"]=t
		else:
			self.back["error"]="fonction du manager incorrecte"	

	######################################################################################		
			
	# dealing with flowspaces
	def controlPerm(self,perms):
	    global perm
	    if perms :
		if len(perms)==1:
		    perm=perms.keys()[0]+"="+str(perms[perms.keys()[0]])
		if len(perms) > 1:
		    for k,v in perms.items() :
			perm+= k+"="+str(v)+","
		perm=perm.strip(",")
		return 0
	    else:
		return 1

	########################################################################################################

	def is_exist_fs(self,fs):
		f= self.getFlowSpace()
		exist1=0
		exist2=0
		for e in f:
			if fs.getName() == e["name"]:
				exist1=1
				for a in e["slice-action"]:
					if a["slice-name"] in fs.getSlicePerm().keys():
						exist2=1
		return exist1,exist2

	#######################################################################################################				      			
	def createFlowSpace(self,f):
		global FLOWSPACE			    	
		if self.fonction == FLOWSPACE:
		    if f.getDpid() and f.getPriority() and f.getMatch() and f.getSlicePerm():
		          
		          if not self.controlPerm(f.getSlicePerm()) and not self.is_exist_fs(f)[0]:		        
		            	var="fvctl -f /dev/null add-flowspace %s %s %s in_port=%s %s"%(f.getName(),f.getDpid(),f.getPriority(),f.getMatch(),perm)
			        param = shlex.split(var) 
			        proc=Popen(param,stdout=PIPE,stderr=PIPE)
			        self.back["out"] , self.back["error"] = proc.communicate()
			  else:
				if self.controlPerm(f.getSlicePerm()):
					self.back['error'] = "il faut renseiger toutes les informations du slice"
				if self.is_exist_fs(f)[0] and not self.is_exist_fs(f)[1]:
					self.back['error'] ="Attention ce Flowspace existe"
				if self.is_exist_fs(f)[1]:
					self.back['error'] = "ce flowspace existe et est deja pris en compte pas le slice specifie"
		else:
			self.back['error'] = "ce manager ne peut creer de slice : c'est un manager"+self.getFonction()

	######################################################################################################################

	def getFlowSpace(self,*nom_slice):
		if len(nom_slice)>0:
			var="fvctl -n list-flowspace -s %s"%(nom_slice[0])
		else :
			var="fvctl -n list-flowspace"
		param0=shlex.split(var)
		param1=shlex.split("tail -n +2")
		p1=Popen(param0,stdout=PIPE,stderr=PIPE)
		p2=Popen(param1,stdin=p1.stdout,stdout=PIPE,stderr=PIPE)
		out , self.back["error"] = p2.communicate()
		l=[]
		for e in out.strip("\n").split("\n"):
			l.append(ast.literal_eval(e))
		return l
		#return out
			
		
	
	        
		                

	    
