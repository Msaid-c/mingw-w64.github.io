import math
from queue import Queue

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def reconstruct_path(prev, start, goal, graph):
    path = []
    current = goal
    while current != start:
        path.append(graph.coordinates(current))
        current = prev.get(current)
        if current is None:
            return []
    path.append(graph.coordinates(start))
    path.reverse()
    return path

def breadth_first(start, dest, graph):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    queue = Queue()
    visited = set()
    prev = {}

    queue.put(start)
    visited.add(start)

    while not queue.empty():
        current = queue.get()
        if current == dest:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = current
                queue.put(neighbor)

    return reconstruct_path(prev, start, dest, graph)

def depth_first(start, dest, graph):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    visited = set()
    prev = {}

    def dfs(node):
        if node == dest:
            return True
        visited.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                prev[neighbor] = node
                if dfs(neighbor):
                    return True
        return False

    dfs(start)
    return reconstruct_path(prev, start, dest, graph)
