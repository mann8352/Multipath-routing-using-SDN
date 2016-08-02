
import json
import httplib2
import traceback

class FlowRetrieval:
	"""Retrives all details of flow of each switch"""

	def __init__(self):
		pass

	def retrieveFlow(self, switch):
		"""retrieves flows"""

		h = httplib2.Http(".cache")
		h.add_credentials('admin', 'admin')

		base_url='http://localhost:8181/restconf/operational/opendaylight-inventory:nodes/node/'
		tail_url='/table/0/'
		url=base_url+switch+tail_url
		header={'Content-Type':'application/json', 'Accept': 'application/json'}
			
		try:
			resp, content = h.request(url, "GET")
			response=json.loads(content)
			flowlist=response['flow-node-inventory:table'][0]['flow']
		except:
			print ' No flow exists'
			print '-----------------------------------'
			return
		
		return flowlist


	def getFlowDetails(self, switch):
		"""gives the details of each flow of a switch"""

		flist=[]
		flowlist=self.retrieveFlow(switch)

		try:
			for f in flowlist:
				flowdict={'id':'', 'match':{}, 'instruction':{}}
				flowdict['id']=f['id']
				flowdict['match']=f['match']
				try:
					flowdict['instruction']=f['instructions']
				except:
					flist.append(flowdict)
					continue
				flist.append(flowdict)
		except:
			return
		
		return flist


	def getFlowIds(self, switch):
		"""returns flow-ids of all flows of a switch"""
		try:
			flowlist=self.getFlowDetails(switch)
			flowidlst=[]

			for flow in flowlist:
				flowidlst.append(str(flow['id']))
			return flowidlst
		except:
			return []


def main():
	print FlowRetrieval().getFlowIds('openflow:24')
	
if __name__ == '__main__':
	main()
		
