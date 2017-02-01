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
NOT_RUNNING_MESSAGE="FlowVisor is not runnning"
NOT_A_SLICE_ERROR="NOT A SLICE"
NOT_A_FLOWSPACE_ERROR="NOT A FLOWSPACE"
PWD="projet\n"
CREATE_SLICE_OK_MESSAGE = "Slice %s was successfully created"
DELETE_SLICE_OK_MESSAGE = "Slice %s has been deleted"
NO_SUCH_SLICE_ERROR = "NO SUCH SLICE "
GENERAL_ERROR = "Please check that FlowVisor is running and try again."
UPDATE_SLICE_RETURN = "Slice %s has been successfully updated"
NO_SWITCH_CONNECTED_ERROR = "No switches connected"
PASSWORD_UPDATE_RETURN ="Slice password for %s has been updated."
DELETE_FLOWSPACE_OK_MESSAGE = "Flowspace entries have been removed."

class Manager:
	def __init__(self):
		#self.fonction = ""
		self.back = {"out":"","error":""}

	def isSlice(self,s):
		try:
			s.getIpAddr()
		except AttributeError:
			return 0
		return 1

	def isFlowspace(self,f):
		try:
			f.getDpid()
		except AttributeError:
			return 0
		return 1

	def is_running_fv(self):
		var ="sudo -S service flowvisor status"
		param=shlex.split(var)
		proc=Popen(param,stdin=PIPE,stdout=PIPE,stderr=PIPE)
		r,e=proc.communicate(PWD)
		if r.strip("\n")== NOT_RUNNING_MESSAGE:
			return 0
		else:
			return 1

	def turnFvOn(self):
		var ="sudo -S service flowvisor start"
		param=shlex.split(var)
		proc=Popen(param,stdout=PIPE,stderr=PIPE)
		r=proc.communicate(PWD)
		if not r :
			return 0
		else :
			return 1

	def turnFvOff(self):
		var ="sudo -S service flowvisor stop"
		param=shlex.split(var)
		proc=Popen(param,stdout=PIPE,stderr=PIPE)
		r,e=proc.communicate(PWD)
		if e :
			return 0
		else :
			return 1

	def restartFv(self):
		if self.is_running_fv():
			var ="sudo -S service flowvisor restart"
			param=shlex.split(var)
			proc=Popen(param,stdout=PIPE,stderr=PIPE)
			r,e=proc.communicate(PWD)
			if e :
				return 0
			else :
				return 1
		else:
			return NOT_RUNNING_MESSAGE

	######################################################################################################

	def is_slice_exit(self,nom):
		s= self.getAllSlices()
		trouve=False
		for a in s:
			if a[0] == nom:
				trouve =True
			
		return trouve

	####################################################################################################

	# dealing with slices

	def createSlice(self,s):
		global SLICE
		r=""
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE
		if not self.isSlice(s):
			return NOT_A_SLICE_ERROR
		if s.getName() and s.getIpAddr() and s.getPort() and s.getMail() and s.getPasswd():
			var="fvctl -n add-slice %s tcp:%s:%s %s -p %s"%(s.getName(),s.getIpAddr(),s.getPort(),s.getMail(),s.getPasswd())
			param = shlex.split(var) 
			proc=Popen(param,stdout=PIPE,stderr=PIPE)
			r , self.back["error"] = proc.communicate()
			
		if r.strip("\n") == CREATE_SLICE_OK_MESSAGE % (s.getName()):
			return 1
		else:
			return 0

	####################################################################################################

	def deleteSlice(self,s):
		r=""
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE
		if not self.isSlice(s):
			return NOT_A_SLICE_ERROR

		if s.getName():
			param = "fvctl -n remove-slice %s" % (s.getName())
			cmd = shlex.split(param)
			proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
			r,self.back["error"] = proc.communicate()
		if r.strip('\n') == DELETE_SLICE_OK_MESSAGE % (s.getName()):
			return 1
		else:
			return 0
	#####################################################################################################
	#												    #
	# 		cette partie concerne la mise a jour d'un slice					    #
	#												    #
	#####################################################################################################

	def enableSlice(self,option):
		try:
			var="fvctl -n update-slice --%s %s"%(option["etat"],option["nom"])
			param=shlex.split(var)
			proc = Popen(param,stdout=PIPE,stderr=PIPE)
			res,err=proc.communicate()
		except KeyError:
			return 0
		if res.strip("\n") == UPDATE_SLICE_RETURN % (option["nom"]):
			return 1
		else:
			return 0


	def updatePort(sels,option):
		try:
			var="fvctl -n update-slice --controller-port=%s %s"%(option["port"],option["nom"])
			param=shlex.split(var)
			proc = Popen(param,stdout=PIPE,stderr=PIPE)
			res,err=proc.communicate()
		except KeyError:
			return 0
		if res.strip("\n") == UPDATE_SLICE_RETURN % (option["nom"]):
			return 1
		else:
			return 0

	def updateSliceHost(self,option):
		try:
			var="fvctl -n update-slice --controller-hostname=%s %s"%(option["hostname"],option["nom"])
			param=shlex.split(var)
			proc = Popen(param,stdout=PIPE,stderr=PIPE)
			res,err=proc.communicate()
		except KeyError:
			return 0
		if res.strip("\n") == UPDATE_SLICE_RETURN % (option["nom"]):
			return 1
		else:
			return 0

	def updateAdminContact(self,option):
		try:
			var="fvctl -n update-slice --admin-contact=%s %s"%(option["contact"],option["nom"])
			param=shlex.split(var)
			proc = Popen(param,stdout=PIPE,stderr=PIPE)
			res,err=proc.communFormicate()
		except KeyError:
			return 0
		if res.strip("\n") == UPDATE_SLICE_RETURN % (option["nom"]):
			return 1
		else:
			return 0

	def updateSlice(self,s):
		if self.isSlice(s):
			req1="fvctl -n update-slice --controller-hostname=%s --controller-port=%s --admin-contact=%s %s"%(s.getIpAddr(),s.getPort(),s.getMail(),s.getName())
			req2="fvctl -n update-slice-password -p %s %s"%(s.getPasswd(),s.getName())
			proc = Popen(shlex.split(req1),stdout=PIPE,stderr=PIPE)
			res1,err1 = proc.communicate()
			proc = Popen(shlex.split(req2),stdout=PIPE,stderr=PIPE)
			res2,err2 = proc.communicate()
			if res1.strip('\n')==UPDATE_SLICE_RETURN %(s.getName()) and res2.strip('\n')==PASSWORD_UPDATE_RETURN %(s.getName()):
				return 1
			else:
				return res1,res2
		else :
			return 0
	####################################################################################################
	def getOneSliceStats(self,s) :
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isSlice(s):
			return NOT_A_SLICE_ERROR

		if s.getName():
			param = "fvctl -n list-slice-stats %s" % (s.getName())
			cmd = shlex.split(param)
			proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
			s,error = proc.communicate()
			return s
		else:
			self.back["error"] = "renseigner le nom du slice a selectionner"

	####################################################################################################
	def getSliceHealth(self,s) : 
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isSlice(s):
			return NOT_A_SLICE_ERROR
		if s.getName():
			param = "fvctl -n list-slice-health %s" % (s.getName())
			cmd = shlex.split(param)
			proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
			self.back["out"] , self.back["error"] = proc.communicate()
		else:
			self.back["error"] = "renseigner le nom du slice a selectionner"	
	####################################################################################################

	def getAllSlices(self):	
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		param = "fvctl -n list-slices"
		param1 = " tail -n +2"
		#param2 = "cut -d --> -f 1:"
		cmd = shlex.split(param)
		proc1 = Popen(cmd,stdout=PIPE,stderr=PIPE)
		p2 = Popen(shlex.split(param1),stdin=proc1.stdout,stdout=PIPE,stderr=PIPE)

		s , self.back["error"] = p2.communicate()
		s=s.strip('\n').replace(' ','').split('\n')
		o=[]
		for e in s:
			o.append(e.split("-->"))
		return o

	###################################################################################################

	def getSliceInfo(self,s):
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isSlice(s):
			return NOT_A_SLICE_ERROR
		if not self.is_slice_exit(s.getName()):
			return NO_SUCH_SLICE_ERROR
		if s.getName():
			param = "fvctl -n list-slice-info %s" % (s.getName())
			cmd = shlex.split(param)
			proc = Popen(cmd,stdout=PIPE,stderr=PIPE)
			r , self.back["error"] = proc.communicate()
			r=r.replace('\n','').replace('false','False').replace('true','True')
			if r == NO_SWITCH_CONNECTED_ERROR or r ==NOT_RUNNING_MESSAGE :
				return NO_SWITCH_CONNECTED_ERROR + NOT_RUNNING_MESSAGE 			
			else:
				try:
					r=ast.literal_eval(r)
					return r
				except SyntaxError:
						return ast.literal_eval(r[55:])
		else:
			self.back["error"] = "renseigner le nom du slice a selectionner"

	#####################################################################################################

	def getSwitchsDpid(self):
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE
		param0 = "fvctl -n  list-datapaths"
		param1 ="tail -n +2"
		param2 = "cut -d : -f 2-"
		p0 = Popen(shlex.split(param0),stdout=PIPE,stderr=PIPE)
		p1 = Popen(shlex.split(param1),stdin=p0.stdout,stdout=PIPE)
		p2 = Popen(shlex.split(param2),stdin=p1.stdout,stdout=PIPE)
		out,self.back["error"]=p2.communicate()
		out = out.strip("\n").split("\n")
		i=1
		t={}
		for dpid in out :
			print dpid
			try:
				t["switch_0%s"%(i)]=int(dpid[-2:])
				i+=1
			except ValueError:
				if not out:# fv is not running
					return out
				else:#fv is runnig but no connected switch
					return NO_SWITCH_CONNECTED_ERROR
				break			
		return t	


	######################################################################################		
			
	# dealing with flowspaces
	def controlPerm(self,perms):#perm est un dict
		global perm
		if perms :
			if len(perms)==1:
				perm=perms.keys()[0]+"="+str(perms[perms.keys()[0]])
				return 0
			elif len(perms) > 1:
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
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isFlowspace(f):
				return NOT_A_FLOWSPACE_ERROR			    	
		if f.getDpid() and f.getPriority() and f.getMatch() and f.getSlicePerm():
				
			if not self.controlPerm(f.getSlicePerm()) and not self.is_exist_fs(f)[1]:		        
				var="fvctl -n add-flowspace %s %s %s in_port=%s %s"%(f.getName(),f.getDpid(),f.getPriority(),f.getMatch(),perm)
				param = shlex.split(var) 
				proc=Popen(param,stdout=PIPE,stderr=PIPE)
				return 1
			else:
				return 0
		else :
				return 0
	######################################################################################################################

	def getFlowSpace(self,*nom_slice):
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
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
			try:
				l.append(ast.literal_eval(e))
			except SyntaxError:
				return GENERAL_ERROR
				break
		return l
		#return out
			
		######################################################################################################################
	def deleteFlowspace(self,f):
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isFlowspace(f):
			return NOT_A_FLOWSPACE_ERROR
		var = 'fvctl -n remove-flowspace %s'%(f.getName())
		param=shlex.split(var)
		p=Popen(param,stdout=PIPE,stderr=PIPE)
		resultats=p.communicate()[0]
		if resultats.strip('\n')==DELETE_FLOWSPACE_OK_MESSAGE:
			return 1
		else:
			return 0

		######################################################################################################################
	def showFlowSpace(self,f):
		if not self.is_running_fv():
			return NOT_RUNNING_MESSAGE 
		if not self.isFlowspace(f):
				return NOT_A_FLOWSPACE_ERROR
		var="fvctl -n list-flowspace"
		var1="grep %s"%(f.getName())
		param0=shlex.split(var)
		param1=shlex.split(var1)
		p=Popen(param0,stdout=PIPE,stderr=PIPE)
		p1=Popen(param1,stdin=p.stdout,stdout=PIPE,stderr=PIPE)
		resultats = p1.communicate()[0]
		
		try:
			resutats=ast.literal_eval(resultats)
			return resutats
		except SyntaxError:
			resutats=""
			return resultats
		

