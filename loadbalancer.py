import json
import httplib2
import traceback

class FlowStatistics:
	"""Retrieves all data from controller using REST api"""
	
	def __init__(self):
		self.stat_node_list = self.statistics()
		response=self.get_topology()
		self.tpnodes=response['node']
		self.tplinks=response['link']

	def statistics(self):
		""" Get statisics of all nodes from the controller"""

		node_list=[]		#list to store each switch details
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
			
		try:
			resp, content = h.request('http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/', "GET")
			response=json.loads(content)
			response=response['nodes']['node']
		except:
			traceback.print_exc()
			return
		
		'no. of nodes'
		i=0
		while i<len(response):
			
			nodes={'node-id':'', 'node-connector':[]}		# dictionary to store nodes-id and corresponding interfaces' details
			
			nodes['node-id']=str(response[i]['id'])
			#print nodes['node-id']
			#print "========================================="
			res=response[i]['node-connector']
			
			j=0
			while j<len(res):
				
				#print res[j]
				#print "============================================"
				node_connector={'id':'', 'state':{'link-down':'', 'blocked':'', 'live':''}, 'port-number':'', 'status':'', 'packets-transmitted':'', 'packets-received':''}
				
				connector_id=str(res[j]['id']).split(':')
				if 'LOCAL' in connector_id:
					node_connector['id']=connector_id[0]+':'+connector_id[1]
				else:
					node_connector['id']=str(res[j]['id'])
				
				#print node_connector['id']
				#print "==============================" 
				
				connector_state=res[j]['flow-node-inventory:state']
				node_connector['state']['link-down']=str(connector_state['link-down'])
				node_connector['state']['blocked']=str(connector_state['blocked'])
				node_connector['state']['live']=str(connector_state['live'])
				
				#node_name=str(res[j]['flow-node-inventory:name'])
				#hw_address=str(res[j]['flow-node-inventory:hardware-address'])
				
				node_connector['port-number']=str(res[j]['flow-node-inventory:port-number'])
				
				packet=res[j]['opendaylight-port-statistics:flow-capable-node-connector-statistics']['packets']
				node_connector['packets-transmitted']=packet['transmitted']
				node_connector['packets-received']=packet['received']
				#print 'packets-transmitted', node_connector['packets-transmitted']
				#print 'packets-received', node_connector['packets-received']
					
				if 'stp-status-aware-node-connector:status' in res[j]:
					node_connector['status']=str(res[j]['stp-status-aware-node-connector:status'])
				
				nodes['node-connector'].append(node_connector)
				j += 1
				
				#print '=================================================================================' 
			
			node_list.append(nodes)
			i += 1
		
		return node_list


	#to retrieve link-down state of a particular node-connector
	def node_connector_state(self, nc_id):
		for i in self.stat_node_list:
			nc=i['node-connector']
			for j in nc:
				if j['id']==nc_id:
					return j['state']['link-down']


	#to retrieve node-connector-id corresponding to a node-id and port-number	
	def getNodeConnectors(self, node_id):#, port_no):
		nclist=[]
		for nc in self.stat_node_list:
			if nc['node-id']==node_id:
				for j in nc['node-connector']:
					if j['port-number']!= 'LOCAL':
						nclist.append(j['id'])
		return nclist#if j['port-number']==port_no:
						#return j['id']


	#to retrieve port-number corresponding to a node-connector-id	
	def port_number(self, nc_id):
		for nc in self.stat_node_list:
			for j in nc['node-connector']:
				if j['id']==nc_id:
						return j['port-number']


	#to get total no. of packets transmitted and retrieved at a node-connector
	def total_packets(self, nc_id):
		for i in self.stat_node_list:
			nc=i['node-connector']
			for j in nc:
				if j['id']==nc_id:
					return (j['packets-transmitted'])+(j['packets-received'])
		
		
	#authentication and request to get topology
	def get_topology(self):
			
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		try:
			resp, content = h.request('http://localhost:8181/restconf/operational/network-topology:network-topology/', "GET")
			response=json.loads(content)
			response=response['network-topology']['topology'][0]
			#print (response)
		except:
			traceback.print_exc()
			return
		
		return response			


	#to get list of node_id of all nodes
	def list_of_nodes(self):
		nodelist=[]
		
		j=0
		while j<len(self.tpnodes):
			nodelist.append(str(self.tpnodes[j]['node-id']))
			j += 1
		return nodelist		


	#to get list of node_id of all hosts
	def list_of_switches(self):	
		switchlist=[]
		nodelist=self.list_of_nodes()
		for node in nodelist:
			nlist=node.split(':') 			# host is a list of string
			if nlist[0]!='host':
				switchlist.append(node)
		return switchlist
	

	#to get list of node_id of all hosts
	def list_of_hosts(self):	
		hostlist=[]
		nodelist=self.list_of_nodes()
		#print nodelist
		for node in nodelist:
			nlist=node.split(':') 			# host is a list of string
			if nlist[0]=='host':
				hostlist.append(node)
		return hostlist


	#to get list of edge_id of all edges 
	def list_of_edges(self):
		edgelist=[]
				
		i=0
		while i<len(self.tplinks):
			edgelist.append(str(self.tplinks[i]['link-id']))
			i += 1
		return  edgelist

	
	#to get details of each edges i.e., sorce-node and destination-node of the edge
	def edges_source_dest(self):
		
		edgelist=[]
		#print len(edges)
		i=0
		while i<len(self.tplinks):
			edge_dict={'id':'', 'source':'', 'destn':''}
			edge_dict['id']=str(self.tplinks[i]['link-id'])
			edge_dict['source']=str(self.tplinks[i]['source']['source-node'])
			edge_dict['destn']=str(self.tplinks[i]['destination']['dest-node'])
			edgelist.append(edge_dict)
			i += 1
		#print len(edgelist)
		return edgelist	
		

	#to get details of each edges i.e., sorce-tp and destination-tp alongwith edge-id of the edge
	def edges(self):
		
		edgelist=[]
		
		i=0
		while i<len(self.tplinks):
			edge_dict={'id':'', 'source-tp':'', 'destn-tp':''}
			edge_dict['id']=str(self.tplinks[i]['link-id'])
			edge_dict['source-tp']=str(self.tplinks[i]['source']['source-tp'])
			edge_dict['destn-tp']=str(self.tplinks[i]['destination']['dest-tp'])
			edgelist.append(edge_dict)
			i += 1
		return edgelist	
		
		
	#to get details of each nodes i.e., id, tp-id, ap-id, mac, ip
	def nodes(self):
		
		nodelist=[]
		
		j=0
		while j<len(self.tpnodes):
			node_dict={'id':'', 'tp-id':[], 'ap-id':'', 'mac':'', 'ip':''} #ap=attachment point :only for hosts
			node_dict['id']=str(self.tpnodes[j]['node-id'])
			tp=self.tpnodes[j]['termination-point'] #tp=termination point
			
			#checking for hosts
			host=self.tpnodes[j]['node-id'].split(':') 			# host is a list of string
			if host[0]=='host':
				node_dict['ap-id']=str(self.tpnodes[j]['host-tracker-service:attachment-points'][0]['tp-id'])
				address=self.tpnodes[j]['host-tracker-service:addresses'][0]
				node_dict['mac']=str(address['mac'])
				node_dict['ip']=str(address['ip'])
				
			k=0
			while k<len(tp):
				node_dict['tp-id'].append(str(tp[k]['tp-id']))
				k += 1
			
			nodelist.append(node_dict)
			j += 1
		
		return nodelist


	#to get total no. of packets transmitted and retrieved at an edge by both its node connectors
	def edge_packets(self,edge_id):
		edge=self.edges()
		#print edge
		i=packets=0
		while i<len(edge):
			if edge[i]['id']==edge_id:
				try:
					source_packets=int(self.total_packets(edge[i]['source-tp']))
				except:
					source_packets=0
				try:
					dest_packets=int(self.total_packets(edge[i]['destn-tp']))
				except:
					dest_packets=0
				packets=source_packets+dest_packets
				return packets
			i +=1


	#to get state of source-tp and destination-tp of an edge
	def edge_state(self,edge_id):
		edgelist=self.edges()
		
		i=0
		while i<len(edgelist):
			if edgelist[i]['id']==edge_id:
				source_tp_state=self.node_connector_state(edgelist[i]['source-tp'])
				dest_tp_state=self.node_connector_state(edgelist[i]['destn-tp'])
				if source_tp_state=='True':
					return 0
				if dest_tp_state=='True':
					return 0
			
				return 1
			i += 1


def main():
	FlowStatistics().getNodeConnectors('openflow:22')
	#self.statistics()
	#topology()
	#dynamics()
	#FlowStatistics().edges_source_dest()
if __name__ == '__main__':
	main()


