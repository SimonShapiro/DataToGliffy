from GeneralGraph import GeneralGraph as gg
from Gliffs import gliffs as gliffs
import json
import csv


def build_from_edges_in_csv(filename, from_id, to_id):
    g = gg.GeneralGraph()
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            g.add_edge({"_id": row[from_id], "data": {}}, {"_id": row[to_id], "data": {}})
    return g
####
## Some tests
#g = gg.GeneralGraph()
#n1 = {"_id": "first node"}
#n2 = {"_id": "quick node three", "data":[]}
#n3 = {"_id": "quick node four", "data":["a", "b", "c"]}
#n4 = {"_id": "quick sink"}
#n0 = {"_id": "two", "data":[]}
#g.add_node(n1).add_node(n0)
#g.add_edge({"_id": "quick node 1"},{"_id": "quick node two", "data":[]}, edge_data={})\
#    .add_edge(n1, n2, edge_meaning="WORKS WITH", edge_data={})\
#    .add_edge(n1, n2, edge_meaning="WORKS WITH", edge_data={"some": "data"})\
#    .add_edge(n1, n3, edge_meaning="LIKES")\
#    .add_edge(n3, n4)\
#    .add_edge(n0, n4)
#
g = build_from_edges_in_csv("/Users/simonshapiro/DataToGliffy/data/test.csv", "FROM", "TO")
#Attach gliffs based on some data on node and edge
for node in g.nodes.values():
    gnode = gliffs.GNode(node["_assignedItemId"], description=node["_id"], shape=gliffs.GLIFFY_SHAPES.COMPONENT)
    node["_gliff"] = gnode
for edge in g.edges.values():
    gline = gliffs.GLine(edge["_assignedItemId"], edge["_fromNode"]["_assignedItemId"], edge["_toNode"]["_assignedItemId"], edge["_edgeMeaning"])
    edge["_gliff"] = gline
###
#Layout the diagram
diagram = gliffs.GliffyDiagram()
g = g.layout_using_grandalf()
gliph_list = [node["_gliff"].gliph for node in g.nodes.values()] + [edge["_gliff"].gliph for edge in g.edges.values()]
diagram.diagram["stage"]["objects"] = gliph_list
print(json.dumps(diagram.diagram))
pass