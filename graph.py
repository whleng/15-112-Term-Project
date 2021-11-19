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
    '''
    ### testing graph ### 
    graph = Graph()
    graph.addEdge((0,0), (0,1))
    graph.addEdge((0,1), (1,1))
    graph.addEdge((1,1), (1,2))
    graph.addEdge((1,1), (2,1))
    graph.addEdge((2,1), (2,2))
    graph.addEdge((2,1), (2,0))
    print("start graph: ", graph)
    '''
    # solution = set()
    solution = dict()
    # startNode = (0,0)
    # targetNode = (5,5)
    solution = solve(startNode, targetNode, graph, visited, solution)
    solution = constructPath(solution, startNode, targetNode)
    return solution # a list of coordinates
    print("solution: ", solution)

def constructPath(solution, startNode, targetNode): 
    currNode = targetNode
    path = [currNode]
    while True:
        prevNode = solution[currNode] 
        path.append(prevNode)
        currNode = prevNode
        if currNode == startNode: break
    return path
    return list(reversed(path))

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

# draw graph works
def drawGraph(app, canvas, graph):
    # graph is an instance of the Graph class
    unvisitedCells = set()
    startNode = (0,0)
    unvisitedCells.add(startNode)
    visitedCells = set()
    while len(unvisitedCells) > 0:
        node = unvisitedCells.pop()
        visitedCells.add(node)
        _, neighbours = getNeighbours(app, app.rows, app.cols, 
                            node[0], node[1], visitedCells)
        #print(neighbours)
        for neighbour in neighbours:
            #print(neighbour)
            # if neighbour does not have a connected edge to the node
            if (node not in graph.table or 
                neighbour not in graph.getNeighbours(node)):
                drawWall(app, canvas, node, neighbour)
        unvisitedCells = set.union(neighbours, unvisitedCells)

# returns two coordinates to draw the walls
def drawWall(app, canvas, node, neighbour):
    # node and neighbour are going to be in the format of (row, col)
    nodeRow, nodeCol = node
    neighbourRow, neighbourCol = neighbour
    if nodeRow == neighbourRow:
        if nodeCol > neighbourCol: # node is on the right of the neighbour
            x0, y0, x1, y1 = getCellBounds(app, node)
        else:  
            x0, y0, x1, y1 = getCellBounds(app, neighbour) # neighbour on right
        line = x0, y0, x0, y0 + app.cellSize
    elif nodeCol == neighbourCol:
        if nodeRow > neighbourRow: # node is on bottom of neighbour
            x0, y0, x1, y1 = getCellBounds(app, node)
        else:  # neighbour at bottom
            x0, y0, x1, y1 = getCellBounds(app, neighbour)
        line = x0, y0, x0 + app.cellSize, y0
    canvas.create_line(line)

# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, node):
    row, col = node
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)
    
# def appStarted(app):
#     app.margin = 0
#     app.rows, app.cols = 20, 20
#     app.cellHeight, app.cellWidth = app.height / app.rows, app.width / app.cols
#     app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
#     app.graph = prim(app)
#     app.path = dfs(app.graph)
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
# loop through nodes in the graph 
#   check the neighbours of this node
#   if the node and the neighbour are not connected by an edge, draw a wall between them
# loop through neighbours of the graph and repeat the same thing

# ---------------------------------------------------------------

# nodes in graph are individual row, col cells
# need to write a function which draws the borders of the cell, based on their connection 
# if row == row, check which col greater then that is the direction, draw a wall there
# apply same rule for col == col
# walls can be represented (row,col),(row,col) aka wall connecting these two nodes together


####################################################
# Code that doesn't work
####################################################

from queue import PriorityQueue

# dijkstra does not really work
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


# bfs does not really work
def bfs(board):
    # conversion of board to graph
    nodes = set()
    edges = dict()
    visited = [ [False] * cols for _ in range(rows) ]

    # convert to nodes
    for row in range(len(rows)):
        for col in range(len(cols)):
            nodes.add( (row, col) )

    # convert connections to edges
    for startNode in nodes:
        for endNode in nodes:
            if (startNode != endNode and board(startNode) == "white"
                and board(endNode) == "white"):
                if len(edges[startNode]) == 0: 
                    edges[startNode] = set()
                edges.startNode.add(endNode)
    
    import queue

    goal = (row-1, col-1)
    reached = False
    currNode = (0,0)
    nodeNeighbours = list()
    while not reached:
        visited[currNode] = True
        neighbours = getNeighbours(currNode)
        nodeNeighbours.extend(neighbours)

        while len(nodeNeighbours) > 0:
            for neighbour in nodeNeighbours:
                neighbours = getNeighbours(neighbour)
                nodeNeighbours.extend(neighbours)
                if neighbour == goal: return True
        return None


# bfs
# for each starting node, find its neighbours, add it to a queue
# if the node has not been visited, visit it and find its neighbours
# keep searching the node for its neighbors, if reach end node return
# while checking, keep track of the shortest path to that point (using)
# 1. Add root node to the queue, and mark it as visited(already explored).
# 2. Loop on the queue as long as it's not empty.
#    1. Get and remove the node at the top of the queue(current).
#    2. For every non-visited child of the current node, do the following: 
#        1. Mark it as visited.
#        2. Check if it's the goal node, If so, then return it.
#        3. Otherwise, push it to the queue.
# 3. If queue is empty, then goal node was not found!

# dfs
# for each starting node, find its neighbours
# for the neighbours, add to the list the next level nodes to search
# go the the next level, then search the neighbours from there
# if one of the neighbours is the end position, backtrack to find the solution
