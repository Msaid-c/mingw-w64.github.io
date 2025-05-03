import math
import heapq
from queue import Queue

import graph
from graph import MapGraph

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

def breadth_first(start, dest):
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

def depth_first(start, dest):
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

def bellman_ford(start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    dist = {v: float('inf') for v in graph.vertices()}
    prev = {}
    dist[start] = 0

    for _ in range(len(graph.vertices()) - 1):
        for u in graph.vertices():
            for v in graph.neighbors(u):
                weight = euclidean(graph.coordinates(u), graph.coordinates(v))
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u

    if dist[dest] == float('inf'):
        return []
    return reconstruct_path(prev, start, dest, graph)

def dijkstra(start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if node == dest:
            break
        for neighbor in graph.neighbors(node):
            weight = euclidean(graph.coordinates(node), graph.coordinates(neighbor))
            new_cost = cost + weight
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    return reconstruct_path(prev, start, dest, graph)

def astar(start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: euclidean(graph.coordinates(start), graph.coordinates(dest))}
    prev = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == dest:
            return reconstruct_path(prev, start, dest, graph)
        for neighbor in graph.neighbors(current):
            tentative_g = g_score[current] + euclidean(graph.coordinates(current), graph.coordinates(neighbor))
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                prev[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean(graph.coordinates(neighbor), graph.coordinates(dest))
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def min_spanning_tree(start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    visited = set()
    heap = [(0, start, None)]
    tree = {}

    while heap:
        weight, current, parent = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if parent is not None:
            tree[current] = parent
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                dist = euclidean(graph.coordinates(current), graph.coordinates(neighbor))
                heapq.heappush(heap, (dist, neighbor, current))

    prev = {}
    node = dest
    while node in tree:
        prev[node] = tree[node]
        node = tree[node]
    return reconstruct_path(prev, start, dest, graph)
