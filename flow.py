import sys
import json
import httplib2
import traceback
from loadbalancer import FlowStatistics
from flowretrieval import FlowRetrieval
#from driver import Driver

class FlowManagement:
	""" Adds, modifies and deletes flows from switch through Controller """
	def __init__(self):
		self.fr=FlowRetrieval()
		self.fs=FlowStatistics()
		#self.dj=Dijkstra()
		try:
			self.hostlist=self.fs.list_of_hosts()
			self.switchlist=self.fs.list_of_switches()
		except:
			traceback.print_exc()

	def addPathFlow(self, pathlist):
		""" Adds new path flows into the switch """
		try:
			edgesd=self.fs.edges_source_dest()
			edge=self.fs.edges()
		except:
			traceback.print_exc()
				
		'Finding edge-id of the edge connecting source and destn nodes'
		i=0
		edgeid=[]
		while i<(len(pathlist)-1):
			edgesource=pathlist[i]
			edgedest=pathlist[i+1]
			j=0
			while j<len(edgesd):
				if (edgesd[j]['source']==edgesource) and (edgesd[j]['destn']==edgedest):
						edge_id=edgesd[j]['id']
						edgeid.append(edge_id)
						break
				j += 1
			i += 1
		
		'Finding source and destination port number'
		x=0
		sourceport=[]
		destnport=[]
		while x<len(edgeid):
			y=0
			while y<len(edge):
				if edge[y]['id']==edgeid[x]:
					srcport=edge[y]['source-tp']
					desport=edge[y]['destn-tp']
					sourceport.append(srcport)
					destnport.append(desport)
					break
				y += 1
			x += 1
		
		print "--------------src port no-----------------------------"
		print sourceport
		print "--------------dest port no-----------------------------"
		print destnport
		print "-------------------------------------------------------"  
		
		'adding flows into the switches'
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/'
		header={'Content-Type':'application/json', 'Accept': 'application/json'}
		
		#findinfg source and destination host address
		srchost=pathlist[0][5:]
		desthost=pathlist[len(pathlist)-1][5:]
		
		m=1
		while m<(len(pathlist)-1):
			nodeid=pathlist[m]
			url=base_url+nodeid+tail_url

			#finding output port no.
			outport=sourceport[m].split(':')
			port=outport[len(outport)-1]
			
			try:
				data={'flow-node-inventory:table': [{'id':0, 'flow':[{'idle-timeout': 0, 'flags': '', 'hard-timeout': 0, 'priority': 10, 'cookie': 3026418949592973442, 'table_id': 0, 'id': '#manish', 'match': {'ethernet-match': {'ethernet-source': {'address': srchost}, 'ethernet-destination': {'address': desthost}}}, 'instructions': {'instruction': [{'order': 0, 'apply-actions': {'action': [{'output-action': {'max-length': 65535, 'output-node-connector': port}, 'order': 0}]}}]}}]}]}#, 'flow-hash-id-map':[{'flow-id': '#manish', 'hash': "Match [_ethernetMatch=EthernetMatch [_ethernetDestination=EthernetDestination [_address=MacAddress [_value=0A:3E:85:D2:3D:EF], augmentation=[]], _ethernetSource=EthernetSource [_address=MacAddress [_value=66:8F:00:F2:71:96], augmentation=[]], augmentation=[]], augmentation=[]]103026418949592973435"}]]}]}
				response, request=h.request(url, "PUT", json.dumps(data), headers=header)
				print "-----Response of putting flow in switch "+nodeid+"-----"
				print response
				print "====================="
			except:
				traceback.print_exc()
			m += 1
	

	def addFlow(self, flowdict):
		"""" Adds a flow to a switch """
				
		matchdict={}
		actdict={}
		switch=flowdict['switch']
		flowid=flowdict['flowid']
		idletimeout=flowdict['idle-timeout']
		hardtimeout=flowdict['hard-timeout']
		priority=flowdict['priority']
		action=flowdict['appaction']
		matchid=flowdict['match']['id']
		maxsize=flowdict['max-length']
		ethsrc=flowdict['match']['address']['source']
		ethdest=flowdict['match']['address']['destination']
		ipport=flowdict['match']['address']['ip-port']
		
		#authentication credentials
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/'
		header={'Content-Type':'application/json', 'Accept': 'application/json'}

		url=url=base_url+flowdict['switch']+tail_url

		if matchid==1:
			matchdict={'ethernet-match': {'ethernet-source': {'address': ethsrc}}}
			
		elif matchid==2:
			matchdict={'ethernet-match': {'ethernet-destination': {'address': ethdest}}}
		
		elif matchid==3:
			matchdict={'ethernet-match': {'ethernet-source': {'address': ethsrc}, 'ethernet-destination': {'address': ethdest}}}
		
		elif matchid==4:
			matchdict={'in-port': ipport}

		actdict={'max-length': maxsize, 'output-node-connector': action}
		
		try:
			data={'flow-node-inventory:table': [{'id':0, 'flow':[{'idle-timeout': idletimeout, 'flags': '', 'hard-timeout': hardtimeout, 'priority': priority, 'cookie':0 , 'table_id': 0, 'id': flowid, 'match': matchdict, 'instructions': {'instruction': [{'order': 0, 'apply-actions': {'action': [{'output-action': actdict, 'order': 0}]}}]}}]}]}
			response, request=h.request(url, "PUT", json.dumps(data), headers=header)
			print "-----Response of putting flow in switch "+nodeid+"-----"
			print response
			print "====================="
		except:
			traceback.print_exc()



	def deleteFlow(self, switch_id, flow_id):
		""" Deletes flow with id=flow_id from switch with id=switch_id """

		flow={}
		flowlist=[]
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		header={'Content-Type':'application/json', 'Accept': 'application/json'}
		base_del_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/'
		end_url='/table/0'
		
		try:
			flowlist=self.fr.retrieveFlow(switch_id)
		
			for f in flowlist:
				if f['id']==flow_id:
					flow=f
					break
			data=flow#json.loads(str(flow))
			print data

			print "Deletion status of "+switch_id
			print "-------------------------------------"
			del_url=base_del_url+'node/'+switch_id+end_url
			delresp, delreq=h.request(del_url,'PUT',json.dumps(data), headers=header)
			print delresp
			print "====================================" 
			
			delresp, delreq=h.request(del_url,'DELETE',json.dumps(data), headers=header)
			print delresp
			print "====================================" 
		except:
			traceback.print_exc()
			






	def deleteAnyFlow(self, switch_id):
		""" Deletes flow with id=flow_id from switch with id=switch_id """

		fs=FlowStatistics()
		switchlist=fs.list_of_switches()
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		header={'Content-Type':'application/json', 'Accept': 'application/json'}
		base_get_url='http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/'
		base_del_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/'
		end_url='/table/0'

		if (switch_id not in switchlist):
			print "Switch "+switch_id+" is not present in the topology"
			return
		
		try:
			res, req=h.request(base_del_url, "DELETE", headers=header)
		except:
			traceback.print_exc()
			
		i=0
		while i<len(switchlist):
			try:
				print "Deletion status of "+switch_id
				print "-------------------------------------"
				get_url=base_get_url+'node/'+switch_id+end_url
				del_url=base_del_url+'node/'+switch_id+end_url
				getresp, getreq=h.request(get_url, "GET")
				get_response=json.loads(getreq)

				"changes start"
				#print get_response

				"changes end "
				#print getresp
				#print "______________________________________"
					
				putresp, putreq=h.request(del_url, "PUT", json.dumps(get_response), headers=header)
				print putresp
				delresp, delreq=h.request(del_url,'DELETE',json.dumps(get_response), headers=header)
				print delresp
				print "===================================="
			except:
				traceback.print_exc()
			i += 1




	def deleteAllFlow(self):
		""" Deletes existing flows from all switches """
		fs=FlowStatistics()
		fm=FlowManagement()
		switchlist=fs.list_of_switches()

		i=0
		while i<len(switchlist):
			self.deleteAnyFlow(switchlist[i])
			i += 1

		

def main():
	#FlowManagement().deleteAnyFlow("openflow:24")
	FlowManagement().deleteAllFlow()

if __name__ == '__main__':
	main()

