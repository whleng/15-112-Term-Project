from cmu_112_graphics import *
# referenced from TA lecture: Graph Algorithm
# generic graph object
class Graph(object):
    def __init__(self):
        self.table = dict() # dict storing the nodes and edges

    # add an edge between two nodes in the graph
    def addEdge(self, nodeA, nodeB, weight=1):
        if nodeA not in self.table:
            self.table[nodeA] = dict()
        if nodeB not in self.table:
            self.table[nodeB] = dict()
        self.table[nodeA][nodeB] = weight
        self.table[nodeB][nodeA] = weight

    # return weight of an edge between two nodes
    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]

    # return list of all nodes in the graph
    def getNodes(self):
        return list(self.table)

    def getNeighbours(self, node):
        return set(self.table[node])

# have yet to integrate the node as an object inside 
class Node(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

# dfs works, for pathfinding, 
# but only finds one path, not the shortest path yet
# referenced from TA lecture: Graph Algorithm
def dfs(graph, startNode, targetNode):
    visited = set()
    solution = dict()
    solution = solve(startNode, targetNode, graph, visited, solution)
    solution = constructPath(solution, startNode, targetNode)
    print("sol:", solution)
    return solution # a list of coordinates

def constructPath(solution, startNode, targetNode): 
    currNode = targetNode
    path = [currNode]
    while True:
        if currNode == startNode: break
        prevNode = solution[currNode] 
        path.append(prevNode)
        currNode = prevNode
    return path

def solve(startNode, targetNode, graph, visited, solution):
    if startNode == targetNode:
        return solution
    visited.add(startNode)
    for neighbour in graph.getNeighbours(startNode):
        if neighbour not in visited:
            solution[neighbour] = startNode
            # solution.add(neighbour)
            # print(startNode, neighbour, solution)
            tempsol = solve(neighbour, targetNode, graph, visited, solution)
            if tempsol != None: return tempsol
            # solution.remove(neighbour)
            solution[neighbour] = None
    return None

# dfs() # uncomment to test dfs

from queue import *

# referenced from TA lecture: Graph Algorithm
def bfs(graph, startNode, targetNode):
    visited = set()
    solution = dict()
    q = Queue() # to be visited
    q.put(startNode) 
    currNode = startNode
    while currNode != targetNode:
        # print(currNode)
        currNode = q.get()
        visited.add(currNode)
        for neighbour in graph.getNeighbours(currNode):
            if neighbour not in visited:
                solution[neighbour] = currNode
                q.put(neighbour)
                visited.add(neighbour)
    solution = constructPath(solution, startNode, targetNode)
    # print(solution)
    return solution

# bfs() # uncomment to test dfs

import random 

# prim's algo for maze generation, works
# can be used (within a room + whole map)
# referenced from 
# https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
# and https://hurna.io/academy/algorithms/maze_generator/prim_s.html
def prim(app):
    startNode = (0,0)
    cells = set() # set of cells
    visited = set()
    cells.add(startNode)
    graph = Graph()
    while len(cells) > 0:
        # cell = cells.pop() # get a random cell
        cell = random.choice(list(cells))
        cells.remove(cell)
        visited.add(cell) # mark cell as visited
        row, col = cell
        visitedNeighbours, unvisitedNeighbours = getNeighbours(app, app.rows, app.cols, row, col, visited) 
        # return visited neighbours
        if len(visitedNeighbours) > 0:
            neighbour = visitedNeighbours.pop()
            graph.addEdge(neighbour, cell) 
            # randomly connect the cell to a neighbour which has been visited
        cells = set.union(cells, unvisitedNeighbours) # add unvisited neighbour to the set
    # to create more paths, randomly add in some edges
    # however, adding this will cause the dfs to not work
    # for i in range(100):
    #     cell = random.randint(0, app.rows), random.randint(0, app.cols)
    #     (drow, dcol) = random.choice(app.directions)
    #     neighbour = cell[0] + drow, cell[1] + dcol
    #     graph.addEdge(neighbour, cell)
    return graph

# obtaining 4 cells connected to it 
def getNeighbours(app, rows, cols, row, col, visited):
    # rows, cols = len(board), len(board[0])
    visitedNeighbours = set()
    unvisitedNeighbours = set()
    for dir in app.directions:
        drow, dcol = dir
        newRow, newCol = row+drow, col+dcol
        if (0 <= newRow < rows and 
            0 <= newCol < cols):
            if ((newRow,newCol) not in visited):
                unvisitedNeighbours.add( (newRow, newCol) )
            else: 
                visitedNeighbours.add( (newRow, newCol))
    return visitedNeighbours, unvisitedNeighbours


#################################################
# Test Code
#################################################
# def appStarted(app):
#     app.margin = 0
#     app.rows, app.cols = 20, 20
#     app.cellHeight, app.cellWidth = app.height / app.rows, app.width / app.cols
#     app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
#     app.graph = prim(app)
#     app.path = bfsNew(app.graph)
#     # app.graph = Graph()
#     # app.graph.addEdge((0,0), (0,1))
#     # app.graph.addEdge((0,1), (1,1))


# def drawCell(app, canvas, row, col, cellColor):
#     x = app.margin + col * app.cellWidth
#     y = app.margin + row * app.cellHeight
#     canvas.create_oval(x, y, x + app.cellWidth, y + app.cellHeight,
#                             fill=cellColor)

# def redrawAll(app, canvas):
#     drawGraph(app, canvas, app.graph)
#     for (row, col) in app.path:
#         drawCell(app, canvas, row, col, "red")

# runApp(width=400, height=400)

####################################################
# Code that doesn't work
####################################################

from queue import PriorityQueue

# referenced from TA lecture: Graph Algorithm
def dijksrta():
    allNodes = {(0,0), (0,1), (1,1), (1,2), (2,0), (2,1), (2,2)}
    graph = Graph()
    graph.addEdge((0,0), (0,1))
    graph.addEdge((0,1), (1,1))
    graph.addEdge((1,1), (1,2))
    graph.addEdge((1,1), (2,1))
    graph.addEdge((2,1), (2,2))
    graph.addEdge((2,1), (2,0))
    startNode = (0,0)
    targetNode = (10,0)
    visited = set()
    distance = dict() 
    solution = dict()
    for node in allNodes:
        distance[node] = 99999
    distance[startNode] = 0
    pq = PriorityQueue() # to be visited
    pq.put(startNode, distance[startNode]) 
    # how to ensure that priority queue sorts by second element
    currNode = startNode
    while currNode != targetNode:
    # while not visited.empty():
        currNode = pq.get()
        for neighbour in graph.getNeighbours(currNode):
            if neighbour not in visited:
                edge = graph.getEdge(currNode, neighbour)
                if distance[currNode] + edge < distance[neighbour]:
                    distance[neighbour] = distance[currNode] + edge
                    if neighbour in pq: 
                        pq.pop(neighbour)
                    pq.put(neighbour, distance[neighbour])
                    solution[neighbour] = currNode
                visited.add(neighbour)
        pq.pop(currNode)
    print("done")
    #print(solution)

# dijksrta()

