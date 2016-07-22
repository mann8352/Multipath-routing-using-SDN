
#Dijkstra's shortest path algorithm
import sys
import heapq
import datetime
from graph import Graph
from vertex import Vertex
from loadbalancer import FlowStatistics
from flow import FlowManagement


class Dijkstra:
	"""Applies Dijkstra's shortest path algorithm on the graph created from the topology"""
	def __init__(self):
		self.fst=FlowStatistics()
		self.fmt=FlowManagement()
		
			
	def shortest(self, v, path):
		''' make shortest path from v.previous'''
		#print "count: "+str(self.count)+", Time: "+str(datetime.datetime.now())
		if v.previous:
		    path.append(v.previous.get_id())
		    self.shortest(v.previous, path)
		return


	def dijkstra(self, aGraph, start, target):
	   	# print '''Dijkstra's shortest path'''
	    # Set the distance for the start node to zero 
	    start.set_distance(0)

	    # Put tuple pair into the priority queue
	    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
	    heapq.heapify(unvisited_queue)

	    while len(unvisited_queue):
	        # Pops a vertex with the smallest distance 
	        uv = heapq.heappop(unvisited_queue)
	        current = uv[1]
	        current.set_visited()

	        #for next in v.adjacent:
	        for next in current.adjacent:
	            # if visited, skip
	            if next.visited:
	                continue
	            new_dist = current.get_distance() + current.get_weight(next)
	            
	            if new_dist < next.get_distance():
	                next.set_distance(new_dist)
	                next.set_previous(current)
	               # print 'updated : current = %s next = %s new_dist = %s' \
	                       # %(current.get_id(), next.get_id(), next.get_distance())
	           # else:
	                #print 'not updated : current = %s next = %s new_dist = %s' \
	                      #  %(current.get_id(), next.get_id(), next.get_distance())

	        # Rebuild heap
	        # 1. Pop every item
	        while len(unvisited_queue):
	            heapq.heappop(unvisited_queue)
	        # 2. Put all vertices not visited into the queue
	        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
	        heapq.heapify(unvisited_queue)


	def shortest_path(self, sourcehost, destnhost):
		"""Finds the shortest path, given the source and destination node"""
		#print "shortest_path starts: "+str(datetime.datetime.now())
		g = Graph()
		fs = self.fst#FlowStatistics()
		nodelist=fs.list_of_nodes()
		for node in nodelist:
			g.add_vertex(node)

		edge=fs.edges()
		edgelist=fs.edges_source_dest()

		#print "Toplogy started: "+str(datetime.datetime.now())
		i=0
		while i<len(edgelist):
			edge_weight=fs.edge_packets(edgelist[i]['id'])
			edge_state=fs.edge_state(edgelist[i]['id'])
			if edge_state==1:
				g.add_edge(edgelist[i]['source'], edgelist[i]['destn'], edge_weight)
			i += 1
		#print "Toplogy End: "+str(datetime.datetime.now())
		#print "Graph start: "+str(datetime.datetime.now())
		#print 'Graph data:'
		for v in g:
			for w in v.get_connections():
				vid = v.get_id()
				wid = w.get_id()
				#print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))	
		#print "Graph End: "+str(datetime.datetime.now())
		self.dijkstra(g, g.get_vertex(sourcehost), g.get_vertex(destnhost))
		target = g.get_vertex(destnhost)
		path = [target.get_id()]
		#print "Dijkstra End: "+str(datetime.datetime.now())
		self.shortest(target, path)
		#print 'The shortest path : %s' %(path[::-1])

		return path


	def anyShortestPath(self, source_host, dest_host):
		"""returns the shortest path between a source and a destination host"""
		path=self.shortest_path(source_host, dest_host)
		return path
	
	
	def allShortestPath(self):
		#print "path starts: "+str(datetime.datetime.now())
		"""returns the shortest path for each host source-destination pair"""
		fs=self.fst#FlowStatistics()
		fm=self.fmt#FlowManagement()
		hostlist=fs.list_of_hosts()
		#print "path End: "+str(datetime.datetime.now())
		#print hostlist
		#print hostlist[0], hostlist[len(hostlist)-1]
		i=0
		while i<len(hostlist):
			j=0
			#path=[]
			while j<len(hostlist):
				if hostlist[i] != hostlist[j]:
					path=self.shortest_path(hostlist[j], hostlist[i])
					print "path between "+hostlist[i]+" and "+hostlist[j]+" is: "
					print ' ---> '.join(path)
					print "_________________________________________________________________________"
					fm.addPathFlow(path)
				j += 1
			i += 1
		
			

def main():
	#print "starts: "+str(datetime.datetime.now())
	start=datetime.datetime.now()
	print "starts: "+str(datetime.datetime.now())
		
	Dijkstra().allShortestPath()
	print "End: "+str(datetime.datetime.now())
	end=datetime.datetime.now()
	time=end-start
	print "Execution time: "+str(time)
	#print "ends: "+str(datetime.datetime.now())
	
    
if __name__ == '__main__':
	main()

  
