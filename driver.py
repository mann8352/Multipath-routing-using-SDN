#Driver program to run the application
import sys
import datetime
import traceback
from dijkstra import Dijkstra
from flow import FlowManagement
from loadbalancer import FlowStatistics

class Driver:
	"""Run the application"""
	def __init__(self):
		self.fs=FlowStatistics()
		self.fm=FlowManagement()
		self.dj=Dijkstra()
		self.hostlist=self.fs.list_of_hosts()
		self.switchlist=self.fs.list_of_switches()

	
	def printHostDetails(self):
		pass


	def getAllHosts(self):
		"""Prints list of hosts"""
		print "-------------------------------------"
		print "=====       LIST OF HOSTS       ====="
		print "-------------------------------------"
		for i in range(1, len(self.hostlist)+1):
			print '  %2d.  %s' % (i, self.hostlist[i-1])
	
	def getAllSwitches(self):
		"""Prints list of switches"""
		print "-------------------------------------"
		print "=====     LIST OF SWITCHES      ====="
		print "-------------------------------------"
		for i in range(1, len(self.switchlist)+1):
			print '  %2d.  %s' % (i, self.switchlist[i-1])

	
	def getAllPaths(self):
		print "---------------------------------------"
		print "Seq No.	:  		Host Id"
		print "---------------------------------------"
		for i in range(1,len(self.hostlist)+1):
			print '  %2d.  %s' % (i, self.hostlist[i-1])
		print "---------------------------------------"

		source=raw_input("  Input Source sequence no. : ")
		target=raw_input("  Input Target sequence no. : ")
		#dj.getAllPaths(source, target)

	
	def getAnyShortestPath(self):
		print "---------------------------------------"
		print "Seq No.	:  		Host Id"
		print "---------------------------------------"
		for i in range(1,len(self.hostlist)+1):
			print str(i)+"	:	"+self.hostlist[i-1]
		print "---------------------------------------"

		try:
			source=int(raw_input("  Input Source sequence no. : "))
			target=int(raw_input("  Input Target sequence no. : "))
			
			if source and target in range(1,len(self.hostlist)+1):
				path=self.dj.anyShortestPath(self.hostlist[target-1], self.hostlist[source-1])
				print "Shortest Path between "+self.hostlist[source-1]+" and "+self.hostlist[target-1]+" is :"
				print ' ---> '.join(path)
				ch=raw_input('Want to push the path into controller ? (Y/N)')
				if((ch=='y') or (ch=='Y')):
					pass#self.fm.addFlow(path)
			else:
				print "~~~~INVALID CHOICE~~~~"
		except:
			traceback.print_exc()
			return

	
	def getAllShortestPath(self):
		self.dj.allShortestPath()

	
	def addSwitchFlow(self):
		self.getAllSwitches()
		
		ncdict={}
		flowdict={}
		switchdict={}
		macdict={}
		ipdict={}
		appaction=''
		ethsrc=''
		ethdest=''
		ipport=''
		
		# getting mac and ip of hosts
		count=1
		nodelist=self.fs.nodes()
		for i in range(1, len(nodelist)+1):
			nlist=nodelist[i-1]['id'].split(':') 			# host is a list of string
			if nlist[0]=='host':
				macdict[count]=nodelist[i-1]['mac']
				ipdict[count]=nodelist[i-1]['ip']
				count +=1


		actdict={1: 'Send to controller', 2: 'Send to some output port', 3: 'Discard'}	
		matchdict={1: 'Ethernet Source Address', 
					2: 'Ethernet Destination Address',
					3: 'Ethernet Source and Destination Address',
					4: 'Input Node Connector'}

		for i in range(1, len(self.switchlist)+1):
			switchdict[i]=self.switchlist[i-1]
		try:
			print '-----------------------------------'
			switch=int(raw_input("  Enter switch no. : "))
			print '  You have selected '+switchdict[switch]+' to add a flow.'
			print '-----------------------------------'
			flowid=raw_input(' Enter flow id : ')
			idletimeout=int(raw_input(' Enter idle-timeout : '))
			hardtimeout=int(raw_input(' Enter hard-timeout : '))
			priority=int(raw_input(' Enter priority(0-10) : '))
			maxsize=int(raw_input(' Enter maximum packet size : '))

			#getting all node-connectors for the switch
			nclist=self.fs.getNodeConnectors(switchdict[switch])
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
					continue

			if matchid==1:
				print '%s   %s   %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				print '-----------------------------------'
				ethsrc=int(raw_input(' Enter ethernet source address : '))
				print '-----------------------------------'
			
			elif matchid==2:
				print '%s   %s   %s' % ('s.no.', 'mac-id', 'ip')
				print '-----------------------------------'
				for i in range(1, len(macdict)+1):
					print '  %d.  %s  %s' % (i, macdict[i], ipdict[i])
				ethdest=int(raw_input(' Enter ethernet destination address : '))
				print '-----------------------------------'
			
			elif matchid==3:
				print '%s   %s   %s' % ('s.no.', 'mac-id', 'ip')
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
						print '  Please choose different ource and destination.'
						continue
					else:
						break


			elif matchid==4:
				print '-----------------------------------'
				print "  Available ports of "+switchdict[switch]+' are : '
				
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
			
			print '-----------------------------------'
			print '       Applied Action '
			print '-----------------------------------'
			for i in range(1, len(actdict)+1):
				print '  %d.  %s' % (i, actdict[i])
			print '-----------------------------------'
			action=int(raw_input("  Enter action to be applied : "))
			print '-----------------------------------'
		
			if action==1:
				appaction='CONTROLLER'
			elif action==2:
				appaction=raw_input(' Enter output port no. : ')
			elif action==3:
				appaction='DISCARD'
			
			flowdict={'switch': switchdict[switch],
						 'flowid': flowid, 
						 'idle-timeout': idletimeout, 
						 'hard-timeout': hardtimeout, 
						 'priority': priority, 
						 'max-length': maxsize,
						 'match': {'id': matchid, 'address':{'source': macdict[ethsrc], 'destination': macdict[ethdest], 'ip-port':ncdict[ipport]}}, 
						 'action': appaction}
			print flowdict
			#fm.addFlow

		except:
			print "INVALID CHOICE"


	def getSwitchFlow(self):
		pass

	def modifySwitchFlow(self):
		"""   """

	def deleteSwitchFlow(self):
		"""  """

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
				print 'wrong choice'
				traceback.print_exc()
				#return
			

			

def main():
	Driver().testRun()

if __name__ == '__main__':
	main()

  

	    