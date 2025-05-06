import math
import json
import heapq
from queue import Queue

class MapGraph:
    def __init__(self, json_file):
        with open(json_file) as f:
            self.graph = json.load(f)

    def get_vertices(self):
        return list(self.graph['E'].keys())

    def get_neighbors(self, v):
        return self.graph['E'][v]

    def get_position(self, v):
        return self.graph['V'][v]['position']

    def find_closest_vertex(self, point):
        closest = None
        min_dist = float('inf')
        for vertex in self.get_vertices():
            dist = euclidean_dist(point, self.get_position(vertex))
            if dist < min_dist:
                min_dist = dist
                closest = vertex
        return closest

def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def reconstruct_path(prev, start, goal):
    path = []
    current = goal
    while current != start:
        if current not in prev:
            return []
        path.append(current)
        current = prev[current]
    path.append(start)
    path.reverse()
    return [graph.get_position(v) for v in path]

graph = MapGraph('graph.json')

def bfs_ids(start_node, dest_node):
    visited = set()
    prev = {}
    queue = Queue()
    queue.put(start_node)
    visited.add(start_node)
    while not queue.empty():
        node = queue.get()
        if node == dest_node:
            break
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = node
                queue.put(neighbor)
    return prev, start_node, dest_node

def breadth_first(start, dest):
    prev, start_node, dest_node = bfs_ids(graph.find_closest_vertex(start), graph.find_closest_vertex(dest))
    return reconstruct_path(prev, start_node, dest_node)

def breadth_first_hub(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    hubs = [v for v in graph.get_vertices() if len(graph.get_neighbors(v)) >= 5]
    hubs.sort(key=lambda h: euclidean_dist(graph.get_position(h), graph.get_position(dest_node)), reverse=True)

    path = []
    current = start_node
    for hub in hubs[:3]:
        prev, sn, dn = bfs_ids(current, hub)
        sub_path = reconstruct_path(prev, sn, dn)
        if sub_path:
            path.extend(sub_path[:-1])
            current = hub
    prev, sn, dn = bfs_ids(current, dest_node)
    final_leg = reconstruct_path(prev, sn, dn)
    if final_leg:
        path.extend(final_leg)
    return path

def depth_first(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    visited = set()
    prev = {}
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node == dest_node:
            break
        if node not in visited:
            visited.add(node)
            for neighbor in reversed(graph.get_neighbors(node)):
                if neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in prev:
                        prev[neighbor] = node
    return reconstruct_path(prev, start_node, dest_node)

def depth_first_best(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    visited = set()
    prev = {}
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node == dest_node:
            break
        if node not in visited:
            visited.add(node)
            neighbors = graph.get_neighbors(node)
            neighbors.sort(key=lambda n: euclidean_dist(graph.get_position(n), graph.get_position(dest_node)), reverse=True)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    if neighbor not in prev:
                        prev[neighbor] = node
    return reconstruct_path(prev, start_node, dest_node)

def dijkstra(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    prev = {}
    cost = {start_node: 0}
    pq = [(0, start_node)]
    while pq:
        current_cost, node = heapq.heappop(pq)
        if node == dest_node:
            break
        if current_cost > cost.get(node, float('inf')):
            continue
        for neighbor in graph.get_neighbors(node):
            weight = euclidean_dist(graph.get_position(node), graph.get_position(neighbor))
            total = current_cost + weight
            if total < cost.get(neighbor, float('inf')):
                cost[neighbor] = total
                prev[neighbor] = node
                heapq.heappush(pq, (total, neighbor))
    return reconstruct_path(prev, start_node, dest_node)

def astar(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    def heuristic(n):
        return euclidean_dist(graph.get_position(n), graph.get_position(dest_node))
    open_set = [(heuristic(start_node), start_node)]
    g_score = {start_node: 0}
    prev = {}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == dest_node:
            break
        for neighbor in graph.get_neighbors(current):
            temp_g = g_score[current] + euclidean_dist(graph.get_position(current), graph.get_position(neighbor))
            if temp_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = temp_g
                prev[neighbor] = current
                heapq.heappush(open_set, (temp_g + heuristic(neighbor), neighbor))
    return reconstruct_path(prev, start_node, dest_node)

def bellman_ford(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {}
    dist[start_node] = 0
    for _ in range(len(graph.get_vertices()) - 1):
        for u in graph.get_vertices():
            for v in graph.get_neighbors(u):
                weight = euclidean_dist(graph.get_position(u), graph.get_position(v))
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
  
    for u in graph.get_vertices():
        for v in graph.get_neighbors(u):
            weight = euclidean_dist(graph.get_position(u), graph.get_position(v))
            if dist[u] + weight < dist[v]:
                return []
    return reconstruct_path(prev, start_node, dest_node)

def bellman_ford_negative(start, dest):
    return bellman_ford(start, dest)

def min_spanning_tree(start, dest):
    parent = {}
    visited = set()
    pq = [(0, graph.find_closest_vertex(start), None)]
    while pq:
        weight, node, prev_node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if prev_node:
            parent[node] = prev_node
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                edge_weight = euclidean_dist(graph.get_position(node), graph.get_position(neighbor))
                heapq.heappush(pq, (edge_weight, neighbor, node))
    return reconstruct_path(parent, graph.find_closest_vertex(start), graph.find_closest_vertex(dest))

def search(algorithm, start, dest):
    funcs = {
        'bfs': breadth_first,
        'bfsh': breadth_first_hub,
        'dfs': depth_first,
        'dfsb': depth_first_best,
        'bf': bellman_ford,
        'bfn': bellman_ford_negative,
        'dijkstra': dijkstra,
        'astar': astar,
        'mst': min_spanning_tree
    }
    return funcs.get(algorithm, lambda s, d: [])(start, dest)
