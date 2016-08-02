#Driver program to run the application
import sys
import time
import traceback
from graph import Graph
from vertex import Vertex
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
		self.g=Graph()
		#self.fm.deleteAllFlow()
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

	
	def getAnyShortestPath(self):
		"Gives the shortest path between any two hosts"

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
					#print path1
					#print path2
					if len(path1)>1:
						print "Shortest Path between "+self.hostdict[source]+" and "+self.hostdict[target]+" is :"
						print ' ---> '.join(path1)
						ch=raw_input('Want to push the path into controller? (Y/N)')
						if ((ch=='y') or (ch=='Y')):
							self.fm.addPathFlow(path1)
							#choice=raw_input('Want to add path in reverse direction? (Y/N)')
							#if ((choice=='y') or (choice=='Y')): 
							time.sleep(5)
								#path1.reverse()
							self.fm.addPathFlow(path2)
						return
						
					else:
						print " No path exists betweeen "+self.hostdict[source]+" and "+self.hostdict[target]
						return
				else:
					print "~~Source and destination can't be the same~~~"
					choice=raw_input('Want to retry ? (Y/N)')
					if ((choice=='y') or (choice=='Y')): 
						continue
					else:
						return
					print "-------------------------------------"
			except:
				#traceback.print_exc()
				print '	~~~~~INVALID CHOICE~~~~~'
				print "-------------------------------------"
				return

	
	def clearFlows(self):
		"""  Returns shortest path between each pair of hosts"""
		self.fm.deleteAllFLow()

	
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

			#checking swith status
			vertex_node = self.g.get_vertex(self.switchdict[switch])
			if vertex_node.get_status()==False:
				print self.switchdict[switch]+' is DOWN at the moment.'
				print 'Please first make it UP and then try adding flows.'
				print '----------------------------------------------------------'
				return
			
			print '  You have selected '+self.switchdict[switch]+' to add a flow.'
			print '-----------------------------------'
			
			idletimeout=int(raw_input(' Enter idle-timeout : '))
			hardtimeout=int(raw_input(' Enter hard-timeout : '))
			priority=int(raw_input(' Enter priority : '))
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
			else:
				print '		~~~~~Invalid Action~~~~~'
				return
						
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
			#traceback.print_exc()
			return



	def getSwitchFlow(self):
		""" Returns the details of all flows of the switch """
		flowlist=[]
		self.getAllSwitches()
		try:
			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '-----------------------------------'
			flowlist=self.fr.getFlowDetails(self.switchdict[switch])
			if flowlist==None:
				return
			print ' ------------------------------------------------------------------- '
			print ' 		Flows of '+self.switchdict[switch]+' : '
			print ' ------------------------------------------------------------------- '
			print '%8s      %10s              %10s' % ('Flow-ID', 'Source', 'Destination')
			print ' ------------------------------------------------------------------- '
			for flow in flowlist:
				try:
					print '%5s    %20s   %20s' %(flow['id'], str(flow['match']['ethernet-match']['ethernet-source']['address']), str(flow['match']['ethernet-match']['ethernet-destination']['address']))#+str(flow['instruction'])
				except:
					print '%5s   %18s %23s' %(flow['id'], str(flow['match']['ipv4-source']), str(flow['match']['ipv4-destination']))
			print ' ------------------------------------------------------------------- '
		except:
			print '         ~~~~~~Invalid choice~~~~~~'
			#traceback.print_exc()
			return
	
	def deleteSwitchFlow(self):
		"""  Deletes a flow from the switch """
		flowlist=[]
		flowdict={}
		self.getAllSwitches()
		try:
			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '-----------------------------------'

			#checking switch status
			vertex_node = self.g.get_vertex(self.switchdict[switch])
			if vertex_node.get_status()==False:
				print self.switchdict[switch]+' is DOWN at the moment.'
				print 'Please first make it UP and then try deleting flows.'
				print '----------------------------------------------------------'
				return

			flowlist=self.fr.getFlowDetails(self.switchdict[switch])
			if flowlist==None:
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
				self.fm.deleteAnyFlow(self.switchdict[switch])
			
			#Deleting a paricular flow of a switch using its flow_id
			elif choice==2:			
				print ' ------------------------------------------------------------------- '
				print '   		Flows of '+self.switchdict[switch]+' : '
				print ' ------------------------------------------------------------------- '
				print '%6s %7s %13s %27s' % (' S.No.', 'Flow-ID', 'source', 'Destination')
				print ' ------------------------------------------------------------------- '
				count=1
				for flow in flowlist:
					try:
						print '%3d   %5s %22s  %22s' % (count, flow['id'], str(flow['match']['ethernet-match']['ethernet-source']['address']), str(flow['match']['ethernet-match']['ethernet-destination']['address']))
					except:
						print '%3d   %5s %18s  %23s' % (count, flow['id'], str(flow['match']['ipv4-source']), str(flow['match']['ipv4-destination']))
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

	
	def switchDown(self):
		"""Brings down a switch"""
		
		ver_dict={}
		print "-------------------------------------"
		print "=====     LIST OF SWITCHES(which are up)      ====="
		print "-------------------------------------"
		count=1
		try:
			#getting list of all vertices' keys(i.e. name of vertices)
			verlist=self.g.get_vertices()
			for vertex in verlist:
				vertex_node = self.g.get_vertex(vertex)
				if vertex_node.get_status() and ('host' not in vertex):		#only switches are considered, but not the host
					print '   %d.   %s ' % (count, str(vertex))
					ver_dict[count]=vertex
					count += 1
			if ver_dict=={}:
				print 'No more active switches are present'
				return
			while 1:
				print "-------------------------------------"
				ver_no=int(raw_input(' Enter S.No. : '))
				#to check for invalid inputs. Gives traceback for invalid inputs
				ver_dict[ver_no]
				self.g.get_vertex(ver_dict[ver_no]).set_status(False)
				
				choice=raw_input(" Want to bring down another switch ? (Y/N)")
				if ((choice=='y') or (choice=='Y')): 
					self.switchDown()
				return
				print "-------------------------------------"
		except:
			traceback.print_exc()



	def switchUp(self):
		"""Brings up a switch"""
		
		ver_dict={}
		print "-------------------------------------"
		print "=====     LIST OF SWITCHES(which are down)      ====="
		print "-------------------------------------"
		count=1
		try:
			#getting list of all vertices' keys(i.e. name of vertices)
			verlist=self.g.get_vertices()
			for vertex in verlist:
				vertex_node = self.g.get_vertex(vertex)
				if (vertex_node.get_status()==False) and ('host' not in vertex):		#only switches are considered, but not the host
					print '   %d.   %s ' % (count, str(vertex))
					ver_dict[count]=vertex
					count += 1
			if ver_dict=={}:
				print 'No more inactive switches are present'
				return
			while 1:
				print "-------------------------------------"
				ver_no=int(raw_input(' Enter S.No. : '))
				#to check for invalid inputs. Gives traceback for invalid inputs
				ver_dict[ver_no]
				self.g.get_vertex(ver_dict[ver_no]).set_status(True)
				
				choice=raw_input(" Want to bring up another switch ? (Y/N)")
				if ((choice=='y') or (choice=='Y')): 
					self.switchUp()
				return
				print "-------------------------------------"
		except:
			traceback.print_exc()


	def exit(self):
		self.exit()
	
	def testRun(self):
		" Program to test the application "
		
		while 1:
			print '============================================='
			print '    MULTIPATH ROUTING OF VIDEOS USING SDN    '
			print '============================================='
			print ' 1. Get all Hosts'
			print ' 2. Get all Switches'
			print ' 3. Get Shortest Path between any pair of hosts'
			print ' 4. Clear all flows from each switch'
			print ' 5. Add a flow to a particular Switch'
			print ' 6. Get flow from a particular Switch'
			print ' 7. Delete a flow from the Switch'
			print ' 8. Bring a switch down'
			print ' 9. Bring a switch up'
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
							 3 : self.getAnyShortestPath,
							 4 : self.clearFlows,
							 5 : self.addSwitchFlow,
							 6 : self.getSwitchFlow,
							 7 : self.deleteSwitchFlow,
							 8: self.switchDown,
							 9 : self.switchUp,
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

  

	    