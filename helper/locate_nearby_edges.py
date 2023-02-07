# https://sumo.dlr.de/docs/Tools/Sumolib.html#locate_nearby_edges_based_on_the_geo-coordinate
# https://sumo.dlr.de/pydoc/sumolib.html

import sumolib

# parse the net
net = sumolib.net.readNet('./cologne_scenario/cologne.net.xml')

edge = net.getEdge('-132409814#4')
fromId = edge.getFromNode()
toId = edge.getToNode()
fromCoord = fromId.getCoord()
toCoord = toId.getCoord()
lon, lat = net.convertXY2LonLat(fromCoord[0], fromCoord[1])

print(edge)
print(fromId, toId)
print(fromCoord, toCoord)
print(lat, ",", lon)


# locate nearby edges based on the geo-coordinate
# This requires the module pyproj to be installed. For larger networks rtree is also strongly recommended.
radius = 0.12
x, y = net.convertLonLat2XY(7.013019057413672, 50.94135355923195)
edges = net.getNeighboringEdges(x, y, radius)


closest = (float('inf'),  None)
for edge, distance in edges:
    print(edge, distance)
    if distance < closest[0]:
        closest = (distance, edge)

print(closest)

# # pick the closest edge
# if len(edges) > 0:
#     distancesAndEdges = sorted([(dist, edge) for edge, dist in edges])
#     dist, closestEdge = distancesAndEdges[0]
# #
# #     print(dist, closestEdge)
