import sys
import math


points = []

count, n = [int(i) for i in input().split()]
lpts = []
for i in range(count):
    lpts.append(input().split())

class Point:
    def __init__(self, datas):
        self.letter = datas[0]
        self.coords = list(map(float, datas[1:]))
        self.visited = False
    
    def distance_to(self, coords):
        count = 0
        for i in range(len(self.coords)):
            count += math.pow((coords[i] - self.coords[i]), 2)
        return count
    
    def orthant_with(self, coords):
        for i in range(len(self.coords)):
            if abs(coords[i]) != 0.0 and abs(self.coords[i]) != 0.0:
                if math.copysign(1.0, coords[i]) != math.copysign(1.0, self.coords[i]):
                    return True
        return False

def nearest_point(origin, points):
    min_distance = math.inf
    found = None
    for p in points:
        if not p.visited:
            dis = p.distance_to(origin)
            if dis < min_distance:
                min_distance = dis
                found = p
    return found

#
# Resolve
#
points = []
for l in lpts:
    points.append(Point(l))

origin = [0.0] * n
visited = 0
solution = []

current = nearest_point(origin, points)
current.visited = True
solution.append(current.letter)
visited += 1
orthant = current.orthant_with(origin)
if orthant: solution.append(' ')

while visited < count:
    npoint = nearest_point(current.coords, points)
    if npoint != None:
        orthant = npoint.orthant_with(current.coords)
        if orthant: solution.append(' ')
        npoint.visited = True
        solution.append(npoint.letter)
        visited += 1
        current = npoint

print("".join(solution))