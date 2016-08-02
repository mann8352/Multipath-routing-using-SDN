import sys
import json
import httplib2
import traceback
from vertex import Vertex
from loadbalancer import FlowStatistics

class Graph(object):
  
    _instance = None
        
    def __new__(self):
        if not self._instance:
            self._instance = super(Graph, self).__new__(self)
            self._instance.vert_dict = {}
            self._instance.num_vertices = 0
            self._instance.createGraph()
        return self._instance

        

    def createGraph(self):
        """creates a graph from the topology"""  
        #print 'creating graph'
        fs = FlowStatistics()
        nodelist=fs.list_of_nodes()
        for node in nodelist:
            self.add_vertex(node)

        edge=fs.edges()
        edgelist=fs.edges_source_dest()

        #print "Toplogy started: "+str(datetime.datetime.now())
        i=0
        while i<len(edgelist):
            edge_weight=fs.edge_packets(edgelist[i]['id'])
            edge_state=fs.edge_state(edgelist[i]['id'])
            if edge_state==1:
                self.add_edge(edgelist[i]['source'], edgelist[i]['destn'], edge_weight)
            i += 1

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        """adds a vertex to the graph"""
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, ver_id):
        """used to retrive vertex uusing its id(i.e. key or name)"""
        if ver_id in self.vert_dict:
            return self.vert_dict[ver_id]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        """adds an edge to the graph"""
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        """returns all keys of vert_dict, which is nothing but vertex names"""
        return self.vert_dict.keys()    #returns list

    def set_previous(self, current):
        """sets the current node to the previous node """                       
        self.previous = current

    def get_previous(self, current):
        """returns the previous node while traversing"""
        return self.previous


