#!/usr/bin/python
from mininet.topo import Topo
class Neteam(Topo):
	def __init__(self):
		# Initialize topology
		Topo.__init__(self)
		# Create template host, switch, and link
		hconfig = {'inNamespace':True}
		http_link_config = {'bw': 10}
		wan_link_config = {'bw': 50}
		host_link_config = {}
		# Create switch nodes
		for i in range(6):
			sconfig = {'dpid': "%016x" % (i+1)}
			self.addSwitch('s%d' % (i+1), **sconfig)
		# Create host nodes
		for i in range(6):
			self.addHost('h%d' % (i+1), **hconfig)
		# Add switch links
		self.addLink('s1', 's3', **http_link_config)
		self.addLink('s1', 's2', **wan_link_config)
		self.addLink('s3', 's4', **http_link_config)
		self.addLink('s3', 's5', **http_link_config)
		self.addLink('s2', 's6', **http_link_config)
		# Add host links
		self.addLink('h1', 's4', **host_link_config)
		self.addLink('h2', 's4', **host_link_config)
		self.addLink('h3', 's5', **host_link_config)
		self.addLink('h4', 's5', **host_link_config)
		self.addLink('h5', 's6', **host_link_config)
		self.addLink('h6', 's6', **host_link_config)

topos = { 'neteam': ( lambda: Neteam() ) }
