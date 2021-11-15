

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

def dfs():
    visited = set()
    graph = Graph()
    graph.addEdge((0,0), (0,1))
    graph.addEdge((0,1), (1,1))
    graph.addEdge((1,1), (1,2))
    graph.addEdge((1,1), (2,1))
    graph.addEdge((1,2), (2,2))
    graph.addEdge((2,1), (2,2))
    graph.addEdge((2,1), (2,0))
    print("start graph: ", graph)
    solution = set()
    startNode = (0,0)
    targetNode = (2,0)
    solution = solve(startNode, targetNode, graph, visited, solution)
    print("solution: ", solution)

def solve(startNode, targetNode, graph, visited, solution):
    if startNode == targetNode:
        return solution
    visited.add(startNode)
    for neighbour in graph.getNeighbours(startNode):
        if neighbour not in visited:
            solution.add(neighbour)
            solution = solve(neighbour, targetNode, graph, visited, solution)
            print(solution)
            if solution != None: return solution
            solution.pop(neighbour)
    return None

dfs()

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

# obtaining 4 cells connected to it 
def getNeighbours(board, row, col):
    rows, cols = len(board), len(board[0])
    neighbours = set()
    for dir in app.directions:
        drow, dcol = dir
        row, col = row+drow, col+dcol
        if (0 <= row < rows and 
            0 <= col < cols):
            neighbours.add( (row, col) )
        else: 
            row, col = row-drow, row-dcol
    return neighbours


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
