import heapq
import math
from queue import Queue

def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def reconstruct_path(prev, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = prev.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path

def breadth_first(graph, start, dest):
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

    return reconstruct_path(prev, start, dest)

def depth_first(graph, start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    visited = set()
    prev = {}

    def dfs(current):
        if current == dest:
            return True
        visited.add(current)
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                prev[neighbor] = current
                if dfs(neighbor):
                    return True
        return False

    if dfs(start):
        return reconstruct_path(prev, start, dest)
    return []

def dijkstra(graph, start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    dist = {start: 0}
    prev = {}
    visited = set()
    heap = [(0, start)]

    while heap:
        current_dist, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if current == dest:
            break
        for neighbor in graph.neighbors(current):
            weight = euclidean(graph.coordinates(current), graph.coordinates(neighbor))
            new_dist = dist[current] + weight
            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    return reconstruct_path(prev, start, dest)

def astar(graph, start, dest):
    start = graph.find_closest_vertex(start)
    dest = graph.find_closest_vertex(dest)
    open_set = [(0, start)]
    g_score = {start: 0}
    f_score = {start: euclidean(graph.coordinates(start), graph.coordinates(dest))}
    prev = {}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == dest:
            return reconstruct_path(prev, start, dest)

        for neighbor in graph.neighbors(current):
            tentative_g = g_score[current] + euclidean(graph.coordinates(current), graph.coordinates(neighbor))
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                prev[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + euclidean(graph.coordinates(neighbor), graph.coordinates(dest))
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def bellman_ford(graph, start, dest):
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

    return reconstruct_path(prev, start, dest) if dist[dest] != float('inf') else []

def min_spanning_tree(graph, start, dest):
    start = graph.find_closest_vertex(start)
    parent = {start: None}
    visited = set()
    heap = [(0, start, None)]
    tree_edges = []

    while heap:
        weight, current, p = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        if p is not None:
            tree_edges.append((p, current))
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                dist = euclidean(graph.coordinates(current), graph.coordinates(neighbor))
                heapq.heappush(heap, (dist, neighbor, current))

    prev = {v: u for u, v in tree_edges}
    return reconstruct_path(prev, start, graph.find_closest_vertex(dest))
