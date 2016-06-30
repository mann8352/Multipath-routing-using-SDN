import sys
import json
import httplib2
import traceback
from loadbalancer import FlowStatistics

class FlowManagement:
	""" Adds, modifies and deletes flows from switch through Controller """

	def addFlow(self, pathlist):
		""" Adds new flows into the switch """

		fs=FlowStatistics()
		edgesd=fs.edges_source_dest()
		edge=fs.edges()
		#dk=Dijkstra()
		'''print "============================================="
		print str(edgesd)
		print str(edge)
		print "=============================================="'''
		#pathlist=dk.shortest_path()
		#pathlist=['host:8e:1c:95:f1:6c:1d', 'openflow:22', 'openflow:23', 'openflow:24', 'host:aa:09:ee:96:2e:8f']
		
		#print pathlist
		#print edgesd
		#print edge
		
		'Finding edge-id of the edge connecting source and destn nodes'
		i=0
		edgeid=[]
		#print "Edgesd"+str(edgesd)
		while i<(len(pathlist)-1):
			edgesource=pathlist[i]
			edgedest=pathlist[i+1]
			#print "Source: "+str(edgesource)+", Dest:"+str(edgedest)
			j=0
			while j<len(edgesd):
				#print "source : "+edgesource+", dest: "+edgedest
				#print "source : "+edgesd[j]['source']+", dest: "+edgesd[j]['destn']
				#print "=================================================="
				if (edgesd[j]['source']==edgesource) and (edgesd[j]['destn']==edgedest):
						edge_id=edgesd[j]['id']
						edgeid.append(edge_id)
						break
				j += 1
			i += 1
		
		"""print "--------------PATH LIST-----------------------------"
		print pathlist
		print "--------------edge id-----------------------------"
		print edgeid"""

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
		fm=FlowManagement()
		#fm.deleteAllFlow()
		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')
		base_url='http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/'
		header={'Content-Type':'application/json', 'Accept': 'application/json'}

		m=1
		n=0
		
		while m<(len(pathlist)-1):
			nodeid=pathlist[m]
			url=base_url+nodeid+tail_url

			#data={"flow-node-inventory:table":[{"id":0, "flow":[{"id":"0","hard-timeout":0,"table_id":0,"match":{"in-port":destnport[m-1]},"instructions":{"instruction":{"order":0,"apply-actions":{"action":[{"order":0,"output-action":{"max-length":65535,"output-node-connector":sourceport[m]}}]}}}},{"id":"1","hard-timeout":0,"table_id":0,"match":{"ethernet-match":{"ethernet-type":{"type":35020}}},"instructions":{"instruction":{"order":0,"apply-actions":{"action":[{"order":0,"output-action":{"max-length":65535,"output-node-connector":"CONTROLLER"}}]}}}}]}]}
			data={'flow-node-inventory:table': [{'id':0, 'flow':[{'idle-timeout': 0, 'flags': '', 'hard-timeout': 0, 'priority': 10, 'cookie': 3026418949592973442, 'table_id': 0, 'id': '#manish', 'match': {'ethernet-match': {'ethernet-source': {'address': '0a:03:5c:70:f8:bd'}, 'ethernet-destination': {'address': 'aa:f0:65:42:1b:d1'}}}, 'instructions': {'instruction': [{'order': 0, 'apply-actions': {'action': [{'output-action': {'max-length': 65535, 'output-node-connector': '2'}, 'order': 0}]}}]}}]}]}#, 'flow-hash-id-map':[{'flow-id': '#manish', 'hash': "Match [_ethernetMatch=EthernetMatch [_ethernetDestination=EthernetDestination [_address=MacAddress [_value=0A:3E:85:D2:3D:EF], augmentation=[]], _ethernetSource=EthernetSource [_address=MacAddress [_value=66:8F:00:F2:71:96], augmentation=[]], augmentation=[]], augmentation=[]]103026418949592973435"}]]}]}
			response, request=h.request(url, "PUT", json.dumps(data), headers=header)
			print "-----Response of putting flow in switch "+nodeid+"-----"
			print response
			print "====================="
			m += 1
		

	def deleteAnyFlow(self, switch_id):
		""" Deletes existing flows from a paricular switch """

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
		#res, req=h.request(base_del_url, "GET")
		#data=json.loads(req)
		try:
			res, req=h.request(base_del_url, "DELETE", headers=header)
			#print res
			#print "++++++++++++++++++++++++++++++++++++++++++"
		except:
			traceback.print_exc()
			
		i=0
		while i<len(switchlist):
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
	FlowManagement().addFlow(['host:d2:5d:e6:48:88:f3', 'openflow:14', 'openflow:11', 'openflow:12', 'host:6a:50:9b:47:53:b9'])

if __name__ == '__main__':
	main()

