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
		""" Adds a path flow to the switch """
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
		"""
		print "--------------src port no-----------------------------"
		print sourceport
		print "--------------dest port no-----------------------------"
		print destnport
		print "-------------------------------------------------------"  """
		
		'adding flows into the switches'
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/flow/'
		#header={'Content-Type':'application/json', 'Accept': 'application/json'}
		header={'Content-Type':'application/xml', 'Accept': 'application/xml'}
		end_url=''
		#findinfg source and destination host address
		srchost=pathlist[0][5:]
		desthost=pathlist[len(pathlist)-1][5:]
		
		m=1
		while m<(len(pathlist)-1):
			nodeid=pathlist[m]
			idlist=self.fr.getFlowIds(nodeid)
			try:
				if idlist==[]:
					end_url='0'
				elif int(idlist[len(idlist)-1])==0:
					end_url=int(idlist[len(idlist)-1])+1
				elif int(idlist[len(idlist)-1]):
					end_url=int(idlist[len(idlist)-1])+1
			except:
				end_url='0'
			#print end_url

			url=base_url+nodeid+tail_url+str(end_url)
			#print url

			#finding output port no.
			outport=sourceport[m].split(':')
			port=outport[len(outport)-1]
			
			try:
				#data={'flow-node-inventory:table': [{'id':0, 'flow':[{'idle-timeout': 300, 'flags': '', 'hard-timeout': 300, 'priority': 10, 'cookie': 3026418949592973442, 'table_id': 0, 'id': '#'+srchost+'-'+desthost, 'match': {'ethernet-match': {'ethernet-source': {'address': srchost}, 'ethernet-destination': {'address': desthost}}}, 'instructions': {'instruction': [{'order': 0, 'apply-actions': {'action': [{'output-action': {'max-length': 65535, 'output-node-connector': port}, 'order': 0}]}}]}}]}]}#, 'flow-hash-id-map':[{'flow-id': '#manish', 'hash': "Match [_ethernetMatch=EthernetMatch [_ethernetDestination=EthernetDestination [_address=MacAddress [_value=0A:3E:85:D2:3D:EF], augmentation=[]], _ethernetSource=EthernetSource [_address=MacAddress [_value=66:8F:00:F2:71:96], augmentation=[]], augmentation=[]], augmentation=[]]103026418949592973435"}]]}]}
				#response, request=h.request(url, "PUT", json.dumps(data), headers=header)
				data="<?xml version='1.0' encoding='UTF-8' standalone='no'?> <flow xmlns='urn:opendaylight:flow:inventory'> <priority>10</priority> <flow-name>manish</flow-name><id>"+str(end_url)+"</id><hard-timeout>0</hard-timeout> <table_id>0</table_id><match> <ethernet-match><ethernet-source><address>"+srchost+"</address></ethernet-source> <ethernet-destination><address>"+desthost+"</address></ethernet-destination></ethernet-match></match><instructions> <instruction> <order>0</order> <apply-actions> <action> <order>0</order> <output-action> <max-length>65535</max-length><output-node-connector>"+port+"</output-node-connector></output-action> </action> </apply-actions> </instruction> </instructions><cookie>3026418949592973326</cookie><idle-timeout>0</idle-timeout> </flow>"
				response, request=h.request(url, "PUT", data, headers=header)
				print "-----Response of putting flow in switch "+nodeid+"-----"
				print response
				print "===================================================================="
			except:
				traceback.print_exc()
			m += 1
		return
	

	def addFlow(self, flowdict):
		"""" Adds a flow to a switch """
				
		matchcriteria=''
		actdict={}
		switch=flowdict['switch']
		#flowid=flowdict['flowid']
		idletimeout=flowdict['idle-timeout']
		hardtimeout=flowdict['hard-timeout']
		priority=flowdict['priority']
		action=flowdict['action']
		matchid=flowdict['match']['id']
		#maxsize=flowdict['max-length']
		#ethsrc=flowdict['match']['address']['ethernet']['source']
		#ethdest=flowdict['match']['address']['ethernet']['destination']
		srcaddress=flowdict['match']['address']['source']
		destaddress=flowdict['match']['address']['destination']
		ipport=flowdict['match']['ip-port']
		
		#authentication credentials
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/flow/'
		#header={'Content-Type':'application/json', 'Accept': 'application/json'}
		header={'Content-Type':'application/xml', 'Accept': 'application/xml'}

		'getting flow-ids of all flows installed on the switch'
		idlist=self.fr.getFlowIds(switch)
		try:
			if idlist==[]:
				end_url='0'
			elif int(idlist[len(idlist)-1])==0:
				end_url=int(idlist[len(idlist)-1])+1
			elif int(idlist[len(idlist)-1]):
				end_url=int(idlist[len(idlist)-1])+1
		except:
			end_url='0'
		print end_url

		url=base_url+switch+tail_url+str(end_url)
		print url

		#url=base_url+flowdict['switch']+tail_url

		if matchid==1:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type><ethernet-source><address>"+srcaddress+"</address></ethernet-source> </ethernet-match>"
			#matchdict={'ethernet-match': {'ethernet-source': {'address': ethsrc}}}
			
		elif matchid==2:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type<ethernet-destination><address>"+destaddress+"</address></ethernet-destination></ethernet-match>"
			#matchdict={'ethernet-match': {'ethernet-destination': {'address': ethdest}}}
		
		elif matchid==3:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type<ethernet-source><address>"+srcaddress+"</address></ethernet-source> <ethernet-destination><address>"+destaddress+"</address></ethernet-destination> </ethernet-match>"
			#matchdict={'ethernet-match': {'ethernet-source': {'address': ethsrc}, 'ethernet-destination': {'address': ethdest}}}
		
		elif matchid==4:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type> </ethernet-match><ipv4-source>"+srcaddress+"/32</ipv4-source>"
			#matchdict={'in-port': ipport}

		elif matchid==5:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type> </ethernet-match><ipv4-destination>"+destaddress+"/32</ipv4-destination>"

		elif matchid==6:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type> </ethernet-match><ipv4-source>"+srcaddress+"/32</ipv4-source><ipv4-destination>"+destaddress+"/32</ipv4-destination>"

		elif matchid==7:
			matchcriteria="<ethernet-match> <ethernet-type> <type>2048</type> </ethernet-type> </ethernet-match><in-port>"+ipport+"</in-port>"

		#actdict={'max-length': maxsize, 'output-node-connector': action}
		
		try:
			#data={'flow-node-inventory:table': [{'id':0, 'flow':[{'idle-timeout': idletimeout, 'flags': '', 'hard-timeout': hardtimeout, 'priority': priority, 'cookie':0 , 'table_id': 0, 'id': flowid, 'match': matchdict, 'instructions': {'instruction': [{'order': 0, 'apply-actions': {'action': [{'output-action': actdict, 'order': 0}]}}]}}]}]}
			#response, request=h.request(url, "PUT", json.dumps(data), headers=header)
			data="<?xml version='1.0' encoding='UTF-8' standalone='no'?> <flow xmlns='urn:opendaylight:flow:inventory'> <priority>"+str(priority)+"</priority> <flow-name>manish</flow-name> <match>"+matchcriteria+"</match> <id>"+str(end_url)+"</id> <table_id>0</table_id> <hard-timeout>"+str(hardtimeout)+"</hard-timeout> <idle-timeout>"+str(idletimeout)+"</idle-timeout> <instructions> <instruction> <order>0</order> <apply-actions> <action> <order>0</order> <output-action> <output-node-connector>"+action+"</output-node-connector> </output-action> </action> </apply-actions> </instruction> </instructions> </flow>"
			response, request=h.request(url, "PUT", data, headers=header)
			print "-----Response of putting flow in switch "+switch+"-----"
			print response
			print "======================================================"
		except:
			traceback.print_exc()


	
	def deleteFlow(self, switch_id, *flow_id):
		""" Deletes flow with id=flow_id from switch with id=switch_id """
		length=len(flow_id)
		
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		header={'Content-Type':'application/json', 'Accept': 'application/json'}
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		end_url='/table/0/flow/'

		try:
			if length==1:
				url=base_url+switch_id+end_url+str(flow_id[0])
				print ' Deletion status of flow-id '+str(flow_id[0])+' in '+switch_id
			elif length==0:
				url=base_url+switch_id
				print ' Deletion status of flows of '+switch_id
			#print url
			
			print "-------------------------------------"	
			res, req=h.request(url, "DELETE", headers=header)
			print res
			print "--------------------------------------"
			
		except:
			traceback.print_exc()
			return
			

	def deleteAnyFlow(self, switch_id):
		""" Deletes all flows from a switch """

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
				print ' Deletion status of flows of '+switch_id
				print '-------------------------------------'
				get_url=base_get_url+'node/'+switch_id+end_url
				del_url=base_del_url+'node/'+switch_id+end_url
				getresp, getreq=h.request(get_url, "GET")
				get_response=json.loads(getreq)

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
	#FlowManagement().deleteFlow("openflow:11")

if __name__ == '__main__':
	main()