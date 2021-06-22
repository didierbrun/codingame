import sys
import math
import heapq

#
# Read datas
#
xs, ys = [int(i) for i in input().split()]
xd, yd = [int(i) for i in input().split()]
clouds = []
n = int(input())
for i in range(n):
    xi, yi, wi, hi = [int(j) for j in input().split()]
    clouds.append((xi, yi, wi, hi))

#
# Cell class 
#
class Cell:
    def __init__(self, index, x, y):
        self.exit = False
        self.start = False
        self.index = index
        self.corner = False
        self.x = x
        self.y = y
        self.v = []
        self.h = []
        self.links = set()
        self.visited = False
        self.distance = math.inf
    
    def intersect(self, other):
        if other.y >= self.v[0] and other.y <= self.v[1]:
            if self.x >= other.h[0] and self.x <= other.h[1]:
                return (self.x, other.y)
        if other.x >= self.h[0] and other.x <= self.h[1]:
            if self.y >= other.v[0] and self.y <= other.v[1]:
                return (other.x, self.y)
        return None
    
    def distance_to(self, other):
        dx = abs(other.x - self.x)
        dy = abs(other.y - self.y)
        return dx + dy
    
    @classmethod
    def cornerCell(self, index, x, y):
        cell = Cell(index, x, y)
        cell.corner = True
        return cell

    @classmethod
    def startCell(self, index, x, y):
        cell = Cell(index, x, y)
        cell.start = True
        return cell
    
    @classmethod
    def exitCell(self, index, x, y):
        cell = Cell(index, x, y)
        cell.exit = True
        return cell

    @classmethod
    def hashPosition(self, x, y):
        return "{}_{}".format(x, y)

def dijkstra(nodes):
    openList = []
    heapq.heapify(openList)
    heapq.heappush(openList, (0, 0))
    while len(openList) > 0:
        cost, n = heapq.heappop(openList)
        for l in nodes[n].links:
            if not nodes[l].visited:
                ncost = cost + nodes[l].distance_to(nodes[n])
                if ncost < nodes[l].distance:
                    nodes[l].distance = ncost
                    heapq.heappush(openList, (ncost, nodes[l].index))
        nodes[n].visited = True

#
# Resolve 
# 
zone = [math.inf, math.inf, -math.inf, -math.inf]
map = {}
nodes = []
map[Cell.hashPosition(xd, yd)] = Cell.startCell(0, xd, yd)
nodes.append(map[Cell.hashPosition(xd, yd)])
map[Cell.hashPosition(xs, ys)] = Cell.exitCell(1, xs, ys)
nodes.append(map[Cell.hashPosition(xs, ys)])

for xi, yi, wi, hi in clouds:
    for x, y in [(xi - 1, yi -1), (xi + wi, yi - 1), (xi + wi, yi + hi), (xi - 1, yi + hi)]:
        inWall = False
        for xi, yi, wi, hi in clouds:
            if x in range(xi, xi + wi) and y in range(yi, yi + hi):
                inWall = True
        if not inWall and Cell.hashPosition(x, y) not in map:
            map[Cell.hashPosition(x, y)] = Cell.cornerCell(len(nodes), x, y)
            nodes.append(map[Cell.hashPosition(x, y)])

for n in nodes:
    if n.x < zone[0]: zone[0] = n.x
    if n.x > zone[2]: zone[2] = n.x
    if n.y < zone[1]: zone[1] = n.y
    if n.y > zone[3]: zone[3] = n.y

for i in range(len(nodes)):
    node = nodes[i]
    h = [zone[0], zone[2]]
    v = [zone[1], zone[3]]
    for xi, yi, wi, hi in clouds:
        if yi <= node.y and yi + hi > node.y and xi <= node.x and xi + wi > node.x:
            if node.x + 1 >= xi and node.x + 1 < xi + wi:
                h[1] = node.x
            if node.x - 1 >= xi and node.x - 1 < xi + wi:
                h[0] = node.x
            if node.y + 1 >= yi and node.y + 1 < yi + hi:
                v[1] = node.y
            if node.y - 1 >= yi and node.y - 1 < yi + hi:
                v[0] = node.y
         
        if yi <= node.y and yi + hi > node.y:
            if xi > node.x and h[1] != node.x:
                h[1] = min(h[1], xi - 1)
            elif xi < node.x and h[0] != node.x:
                h[0] = max(h[0], xi + wi)
        if xi <= node.x and xi + wi > node.x:
            if yi > node.y and v[1] != node.y:
                v[1] = min(v[1], yi - 1)
            elif yi < node.y and v[0] != node.y:
                v[0] = max(v[0], yi + hi)
        
    for n in nodes:
        if n.index != i:
            if n.x == node.x:
                if n.y in range(v[0], v[1] + 1):
                    if n.y < node.y:
                        v[0] = max(v[0], n.y)
                    else :
                        v[1] = min(v[1], n.y)
            if n.y == node.y:
                if n.x in range(h[0], h[1] + 1):
                    if n.x < node.x:
                        h[0] = max(h[0], n.x)
                    else:
                        h[1] = min(h[1], n.x)
    node.v = v
    node.h = h

for i in range(len(nodes)):
    na = nodes[i]
    for j in range(len(nodes)):
        if i != j:
            nb = nodes[j]
            if na.index != nb.index:
                if na.intersect(nb) != None:
                    na.links.add(nb.index)
                    nb.links.add(na.index)

dijkstra(nodes)
print(nodes[1].distance)