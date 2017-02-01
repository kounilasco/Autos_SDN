from entities.manager import *
from entities.slice import Slice,Flowspace
import ast

'''f=Flowspace()
f.setDpid(5)
f.setMatch(3)
f.setPriority(1)
f.setSlicePerm({'etudiant':'7'})
f.setName()'''
'''e={"name":"dsi","IpAddr":"127.0.0.1","port":"10003","mail":"test@neteam.ci","passwd":"test"}
s=Slice()
s.setName('dsi')
s.setIpAddr('127.0.0.1')
s.setPort('10010')
s.setPasswd('test')
s.setMail('test22h16@gmail.com')'''
m=Manager()
print m.getFlowSpaceBySliceName("dsi")
#m.createFlowSpace(f)
#a= m.getFlowSpace("etudiant")

#print(dpid)
#print(m.back["error"])
#print f.getSlicePerm().keys()
#print ast.literal_eval(a[0]).keys()
#for e in a:
#	print(e)
