from grandalf.graphs import Vertex,Edge,Graph
from grandalf.layouts import SugiyamaLayout
import math
from grandalf.routing import route_with_rounded_corners

"""
A GeneralGraph contains two dictionaries: nodes and edges

nodes are added to the GeneralGraph by calling add_node(node) on the GeneralGraph

a node has to be a dictionary and contain an "_id" which must be hashable
a shadow integer identifier _assignedItemId is derived from the item_count in the GeneralGraph

an edge is a directional join of two nodes
an edge can have 'meaning' which is some text that defines the meaning of the join (edge_meaning=)
an edge can have 'data' which can be any (dictionary) object (edge_data=)

To do:
 remove nodes and edges
 change node and edge values

??? should data aggregate on edges or edges in their entirety
"""


class GeneralGraph:
    item_count = 0

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        pass

    def add_node(self, node: dict):  # node has to have id
        if node.get("_id"):
            self.nodes[node["_id"]] = {
                "_id": node["_id"],
                "_assignedItemId": GeneralGraph.item_count,
                "_node": node,
            }
            GeneralGraph.item_count = GeneralGraph.item_count + 2  # to cover the label
        else: raise TypeError("Node must have ._id")
        return self

    def add_edge(self, from_node: dict, to_node: dict, edge_data=None, edge_meaning: str=None):
        if from_node.get("_id") and to_node.get("_id"):
            if not self.nodes.get(from_node["_id"]):
                self.add_node(from_node)
            if not self.nodes.get(to_node["_id"]):
                self.add_node(to_node)
            edge_id = "{}-[{}]->{}".format(from_node["_id"], edge_meaning, to_node["_id"]) if edge_meaning else\
                "{}-->{}".format(from_node["_id"], to_node["_id"])
            edge = {
                    "_id": edge_id,
                    "_assignedItemId": GeneralGraph.item_count,
                    "_fromNode": self.nodes[from_node["_id"]],
                    "_edgeMeaning": edge_meaning,
                    "_toNode": self.nodes[to_node["_id"]],
                    "_edgeData": edge_data
                }
            # SHOULD allow for multiple edges with the same _id
            if not self.edges.get(edge_id):
                self.edges[edge_id] = edge
                self.edges[edge_id]["_edgeData"] = [self.edges[edge_id]["_edgeData"],]  #embed edgeData in a list
            else:
                self.edges[edge_id]["_edgeData"].append(edge["_edgeData"])
            GeneralGraph.item_count = GeneralGraph.item_count + 2  # to cover the label
        else: raise TypeError("from_node and to_node must have ['_id']")
        return self

    def layout_using_grandalf(self):
        # ??? Are "_grandalf_vertices" needed - can they be local???
        """
        :return:
        """
        X_OFFSET = 25
        MAX_COMPONENT_SIZE = 150  # ??? need an algorithmic way of finding this plus some gutter

        class size(object):
            def __init__(self, w, h):
                self.w = w
                self.h = h

        # create grandalf vertices
        for node in self.nodes.values():
            v = Vertex(node["_id"])
            v.view = size(node["_gliff"].gliph["width"], node["_gliff"].gliph["height"])
            node["_grandalf_vertex"] = v
        V = [node["_grandalf_vertex"] for node in self.nodes.values()]
        E = [Edge(edge["_fromNode"]["_grandalf_vertex"], edge["_toNode"]["_grandalf_vertex"]) for edge in self.edges.values()]
        g = Graph(V, E)
        for component in g.C:  # Each component
            sug = SugiyamaLayout(component)
            sug.init_all()
            sug.draw(5)  # allows negative x's
            # Layout components and adjust for gliffy sizes
            min_x = min(v.view.xy[0] for v in component.sV)
            min_y = min(v.view.xy[1] for v in component.sV)
            max_x = max(v.view.xy[0] for v in component.sV)
            # ??? Reset _gliff positions rather than grandalf positions
            Y_OFFSET = 100
            layer = 0
            layer_pos = min_y
            for v in component.sV:
                if not math.isclose(layer_pos, v.view.xy[1]):
                    layer = layer + 1
                    layer_pos = v.view.xy[1]
                v.view.new_x = v.view.xy[0] - min_x + X_OFFSET
                v.view.new_y = v.view.xy[1] + layer * Y_OFFSET
                # ??? need to know that "_gliff" has been created
                self.nodes[v.data]["_gliff"].gliph["x"] = v.view.new_x
                self.nodes[v.data]["_gliff"].gliph["y"] = v.view.new_y
                print("%s %s: (%d,%d)" % (component, v.data, v.view.new_x, v.view.xy[1]))
            print("=====End Component=======")
            X_OFFSET = MAX_COMPONENT_SIZE + X_OFFSET + max_x - min_x
        return self