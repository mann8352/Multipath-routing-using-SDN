#Driver program to run the application
import sys
import datetime
import traceback
from dijkstra import Dijkstra
from flow import FlowManagement
from loadbalancer import FlowStatistics
from flowretrieval import FlowRetrieval

class Driver:
	"""Runs the application"""
	def __init__(self):
		self.fr=FlowRetrieval()
		self.fs=FlowStatistics()
		self.fm=FlowManagement()
		self.dj=Dijkstra()
		try:
			self.hostlist=self.fs.list_of_hosts()
			self.switchlist=self.fs.list_of_switches()
		except:
			traceback.print_exc()

		self.hostdict={}
		for i in range (1, len(self.hostlist)+1):
			self.hostdict[i]=self.hostlist[i-1]
		
		self.switchdict={}
		for i in range (1, len(self.switchlist)+1):
			self.switchdict[i]=self.switchlist[i-1]


	def getAllHosts(self):
		"""Prints list of hosts"""
		
		print "-------------------------------------"
		print "=====       LIST OF HOSTS       ====="
		print "-------------------------------------"
		for i in range(1, len(self.hostdict)+1):
			print '  %2d.  %s' % (i, self.hostdict[i])
	
	
	def getAllSwitches(self):
		"""Prints list of switches"""
		
		print "-------------------------------------"
		print "=====     LIST OF SWITCHES      ====="
		print "-------------------------------------"
		for i in range(1, len(self.switchdict)+1):
			print '  %2d.  %s' % (i, self.switchdict[i])

	
	def getAllPaths(self):
		"""Gets different paths between two hosts"""

		self.getAllHosts()
		try:
			print "-------------------------------------"
			source=int (raw_input("  Input Source sequence no. : "))
			target=int (raw_input("  Input Target sequence no. : "))
			print "-------------------------------------"
			
			if source==target:
				print "~~Source and destination can't be the same~~~"
				print "-------------------------------------"
		except :
			print '~~~Invalid Choice~~~'
			print "-------------------------------------"
		

	
	def getAnyShortestPath(self):
		"Gets the shortest path between any two hosts"

		self.getAllHosts()

		while 1:
			try:
				print "-------------------------------------"
				source=int (raw_input("  Input Source sequence no. : "))
				target=int (raw_input("  Input Target sequence no. : "))
				print "-------------------------------------"
				
				if source!=target:						
					path1=self.dj.anyShortestPath(self.hostdict[target], self.hostdict[source])
					path2=self.dj.anyShortestPath(self.hostdict[source], self.hostdict[target])
					print "Shortest Path between "+self.hostdict[source]+" and "+self.hostdict[target]+" is :"
					print ' ---> '.join(path1)
					ch=raw_input('Want to push the path into controller ? (Y/N)')
					if ((ch=='y') or (ch=='Y')):
						self.fm.addPathFlow(path1)
						choice=raw_input('Want to retry ? (Y/N)')
						if ((choice=='y') or (choice=='Y')): 
							self.fm.addPathFlow(path2)
					break
				else:
					print "~~Source and destination can't be the same~~~"
					choice=raw_input('Want to retry ? (Y/N)')
					if ((choice=='y') or (choice=='Y')): 
						continue
					else:
						break
					print "-------------------------------------"
			except:
				traceback.print_exc()
				print "-------------------------------------"
				return

	
	def getAllShortestPath(self):
		"""  Returns shortest path between each pair of hosts"""
		self.dj.allShortestPath()

	
	def addSwitchFlow(self):
		""" Adds flow to a switch"""
		self.getAllSwitches()
		
		ncdict={}
		flowdict={}
		macdict={}
		ipdict={}
		appaction=''
		ethsrc=''
		ethdest=''
		ipsrc=''
		ipdest=''
		ipport=''
		
		actdict={1: 'Send to controller', 2: 'Send to some output port', 3: 'Discard'}	
		matchdict={1: 'Ethernet Source Address', 
					2: 'Ethernet Destination Address',
					3: 'Ethernet Source and Destination Address',
					4: 'IPV4 Source Address',
					5: 'IPV4 Destination Address',
					6: 'IPV4 Source and Destination Address',
					7: 'Input Node Connector'}

		try:
			# getting mac and ip of hosts
			count=1
			nodelist=self.fs.nodes()
			for i in range(1, len(nodelist)+1):
				nlist=nodelist[i-1]['id'].split(':') 			# host is a list of string
				if nlist[0]=='host':
					macdict[count]=nodelist[i-1]['mac']
					ipdict[count]=nodelist[i-1]['ip']
					count += 1

			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '  You have selected '+self.switchdict[switch]+' to add a flow.'
			print '-----------------------------------'
			
			"""while 1:
				count=0
				print '  Entered Id is prefixed by # automatically. Enter only flow-id. '
				flowid=raw_input(' Enter flow id : ')
				flowidlist=self.fr.getFlowIds(self.switchdict[switch])
				if ('#'+flowid) in flowidlist:
					print '-----------------------------------'
					print 'flowid '+flowid+' already exists in '+self.switchdict[switch]
					if count==0:
						print ' Already present IDs are : '
						for ids in flowidlist:
							print ids
						print '-----------------------------------'
					continue
				else:
					break"""
			
			idletimeout=int(raw_input(' Enter idle-timeout : '))
			hardtimeout=int(raw_input(' Enter hard-timeout : '))
			priority=int(raw_input(' Enter priority(0-10) : '))
			#maxsize=int(raw_input(' Enter maximum packet size : '))

			#getting all node-connectors for the switch
			nclist=self.fs.getNodeConnectors(self.switchdict[switch])
			for i in range(1, len(nclist)+1):
				ncdict[i]=nclist[i-1]

			print '-----------------------------------'
			print '      Matching Criteria '
			print '-----------------------------------'
			for i in range(1, len(matchdict)+1):
				print '  %d.  %s' % (i, matchdict[i])
			while 1:
				print '-----------------------------------'
				matchid=int(raw_input("  Enter matching criteria : "))
				print '-----------------------------------'
				if matchid in range(1, len(matchdict)+1):
					break
				else:
					print '~~~~~Wrong Entry~~~~~'
					print '-----------------------------------'
					continue

			if matchid==1:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				
				while 1:
					print '-----------------------------------'
					ethsrc=int(raw_input(' Enter ethernet source address : '))
					print '-----------------------------------'
					if ethsrc in range(1, len(macdict)+1):
						break
					else:
						print '~~~~~Wrong Entry~~~~~'
						print '-----------------------------------'
						continue
			
			elif matchid==2:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				while 1:
					print '-----------------------------------'
					ethdest=int(raw_input(' Enter ethernet destination address : '))
					print '-----------------------------------'
					if ethdest in range(1, len(macdict)+1):
						break
					else:
						print '~~~~~Wrong Entry~~~~~'
						print '-----------------------------------'
						continue
			
			elif matchid==3:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				
				while 1:
					print '-----------------------------------'
					ethsrc=int(raw_input(' Enter ethernet source address : '))
					ethdest=int(raw_input(' Enter ethernet destination address : '))
					print '-----------------------------------'
					if macdict[ethsrc]==macdict[ethdest]:
						print '  Source and destination cannot be the same.'
						print '  Please choose different source and destination.'
						print '-----------------------------------'
						continue
					else:
						break

			if matchid==4:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				
				while 1:
					print '-----------------------------------'
					ipsrc=int(raw_input(' Enter IPV4 source address : '))
					print '-----------------------------------'
					if ipsrc in range(1, len(ipdict)+1):
						break
					else:
						print '~~~~~Wrong Entry~~~~~'
						print '-----------------------------------'
						continue
			
			elif matchid==5:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				while 1:
					print '-----------------------------------'
					ipdest=int(raw_input(' Enter IPV4 destination address : '))
					print '-----------------------------------'
					if ipdest in range(1, len(ipdict)+1):
						break
					else:
						print '~~~~~Wrong Entry~~~~~'
						print '-----------------------------------'
						continue
			
			elif matchid==6:
				print '%s      %s  	    %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				
				while 1:
					print '-----------------------------------'
					ipsrc=int(raw_input(' Enter IPV4 source address : '))
					ipdest=int(raw_input(' Enter IPV4 destination address : '))
					print '-----------------------------------'
					if ipdict[ipsrc]==ipdict[ipdest]:
						print '  Source and destination cannot be the same.'
						print '  Please choose different source and destination.'
						print '-----------------------------------'
						continue
					else:
						break


			elif matchid==7:
				print '-----------------------------------'
				print "  Available ports of "+self.switchdict[switch]+' are : '
				
				for i in range(1, len(ncdict)+1):
					print '  %2d.  %s' % (i, ncdict[i])

				while 1:
					print '-----------------------------------'
					ipport=int(raw_input(' Enter input port no. : '))
					print '-----------------------------------'
					if ipport in range(1, len(ncdict)+1):
						break
					else:
						print '~~~~~Port not available~~~~~'
						continue
			
			mdict={}
			if matchid==1:
				mdict={'id': matchid, 'address': {'source': macdict[ethsrc], 'destination': ''}, 'ip-port': ''}
			elif matchid==2:
				mdict={'id': matchid, 'address': {'source': '', 'destination': macdict[ethdest]}, 'ip-port': ''}
			elif matchid==3:
				mdict={'id': matchid, 'address': {'source': macdict[ethsrc], 'destination': macdict[ethdest]}, 'ip-port': ''}
			elif matchid==4:
				mdict={'id': matchid, 'address': {'source': ipdict[ipsrc], 'destination': ''}, 'ip-port': ''}
			elif matchid==5:
				mdict={'id': matchid, 'address': {'source': '', 'destination': ipdict[ipdest]}, 'ip-port': ''}
			elif matchid==6:
				mdict={'id': matchid, 'address': {'source': ipdict[ipsrc], 'destination': ipdict[ipdest]}, 'ip-port': ''}
			elif matchid==7:
				mdict={'id': matchid, 'address': {'source': '', 'destination': ''}, 'ip-port': ipport}


			print '-----------------------------------'
			print '       Applied Action '
			print '-----------------------------------'
			for i in range(1, len(actdict)+1):
				print '  %d.  %s' % (i, actdict[i])
			print '-----------------------------------'
			action=int(raw_input("  Enter action to be applied :"))
			print '-----------------------------------'
		
			if action==1:
				appaction='CONTROLLER'
			elif action==2:
				print '-----------------------------------'
				print "  Available ports of "+self.switchdict[switch]+' are : '
				for i in range(1, len(ncdict)+1):
					print '  %2d.  %s' % (i, ncdict[i])
				while 1:
					print '-----------------------------------'
					appaction=int(raw_input(' Enter output port no. : '))
					if appaction in range(1, len(ncdict)+1):
							break
					else:
						print '~~~~~Port not available~~~~~'
						continue
		
			elif action==3:
				appaction='DISCARD'
						
			flowdict={'switch': self.switchdict[switch], 
						'idle-timeout': idletimeout, 
						'hard-timeout': hardtimeout, 
						'priority': priority, 
						'match': mdict,
						'action': appaction}
			
			print flowdict
			self.fm.addFlow(flowdict)

		except:
			print "=====Invalid Input======"
			traceback.print_exc()



	def getSwitchFlow(self):
		""" Returns the details of all flows of the switch """

		flowlist=[]
		self.getAllSwitches()
		try:
			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '-----------------------------------'
			flowlist=self.fr.getFlowDetails(self.switchdict[switch])

			print '-----------------------------------'
			print ' Flows of switch '+self.switchdict[switch]+' are: '
			print '-----------------------------------'
			print '%s      %s         %s' % ('Flow-ID', 'Matching Criteria', 'Instructions')
			print '-----------------------------------'
			for flow in flowlist:
				print flow['id']+'		'+str(flow['match'])+'		'#+str(flow['instruction'])

		except:
			print '      Invalid choice  '
			traceback.print_exc()
			
	
	def modifySwitchFlow(self):
		"""   """
		pass

	def deleteSwitchFlow(self):
		"""  Deletes a flow from the switch """

		flowlist=[]
		flowdict={}
		self.getAllSwitches()
		try:
			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '-----------------------------------'
			
			#creating dictionary of flow details
			flowlist=self.fr.getFlowDetails(self.switchdict[switch])
			if flowlist==[]:
				print 'Nothing to delete'
				return
			for i in range (1, len(flowlist)+1):
				flowdict[i]=flowlist[i-1]
			
			print '-------------------------------------'
			print ' 1. Delete all flows of '+self.switchdict[switch]
			print ' 2. Delete flow using flow-id'
			print '-------------------------------------'
			choice = int(raw_input(' Enter your choice: '))
			print '-------------------------------------'
			
			#Deleting all flows of a switch
			if choice==1:
				self.fm.deleteFlow(self.switchdict[switch])
			
			#Deleting a paricular flow of a switch using its flow_id
			elif choice==2:			
				print '-----------------------------------'
				print ' Flows of switch '+self.switchdict[switch]+' are: '
				print '-----------------------------------'
				print '%5s %5c %12s %30s         %50s' % ('S.No.', ' ', 'Flow-ID', 'Matching Criteria', 'Instructions')
				print '-----------------------------------'
				count=1
				for flow in flowlist:
					print '%3d   %5s %-20s    %s' % (count, ' ', flow['id'], str(flow['match']))#+str(flow['instruction'])
					count += 1

				while 1:
					print ' ------------------------------------------------------------------- '
					flowseq=int(raw_input(' Enter S.No. : '))
					flowdict[flowseq]
					
					choice=raw_input(" Want to delete flowid no. "+flowlist[flowseq-1]['id']+" ? (Y/N)")
					if ((choice=='y') or (choice=='Y')): 
						self.fm.deleteFlow(self.switchdict[switch], flowlist[flowseq-1]['id'])
						break
					else:
						break
					print "-------------------------------------"

		except:
			traceback.print_exc()
			return

	
	def exit(self):
		self.exit()
	
	def testRun(self):
		" Program to test the application "
		
		while 1:
			print '-------------------------------------'
			print '     MULTIPATH ROUTING USING SDN     '
			print '-------------------------------------'
			print ' 1. Get all Hosts'
			print ' 2. Get all Switches'
			print ' 3. Get all possible paths between any pair of hosts'
			print ' 4. Get Shortest Path between any pair of hosts'
			print ' 5. Get Shortest Path between every pair of hosts'
			print ' 6. Add a flow to a particular Switch'
			print ' 7. Get flow from a particular Switch'
			print ' 8. Modify flow of a Switch'
			print ' 9. Delete a flow from the Switch'
			print '10. Exit'
			print '-------------------------------------'

			try:
				option = int(raw_input('  Enter option needed: '))
				print '-------------------------------------'
				if option==10:
					print "~~~~~~~Thanks For Visiting... See You Again~~~~~~~"
					print '--------------------------------------------------'
					break
					self.exit()
						
				choice = { 1 : self.getAllHosts,
							 2 : self.getAllSwitches,
							 3 : self.getAllPaths,
							 4 : self.getAnyShortestPath,
							 5 : self.getAllShortestPath,
							 6 : self.addSwitchFlow,
							 7 : self.getSwitchFlow,
							 8 : self.modifySwitchFlow,
							 9 : self.deleteSwitchFlow,
							 10 : self.exit }
				
				choice[option]()
			except:
				print '    ### wrong choice ###'
				traceback.print_exc()
				#return
			

			

def main():
	Driver().testRun()

if __name__ == '__main__':
	main()

  

	    