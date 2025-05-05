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


graph = MapGraph('graph.json')

def euclidean_dist(a, b):
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

def breadth_first_search(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
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
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def breadth_first_hub(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)

    hubs = [v for v in graph.get_vertices() if len(graph.get_neighbors(v)) >= 5]
    hubs.sort(key=lambda h: euclidean_dist(graph.get_position(h), graph.get_position(dest_node)), reverse=True)

    path = []
    current = start_node
    for hub in hubs[:3]:
        sub_path = breadth_first_search(graph.get_position(current), graph.get_position(hub))
        if not sub_path:
            continue
        path.extend(sub_path[:-1])
        current = hub

    final_leg = breadth_first_search(graph.get_position(current), graph.get_position(dest_node))
    if final_leg:
        path.extend(final_leg)
    else:
        return []

    return path

def depth_first_search(start, dest):
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
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

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
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def dijkstra(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    visited = set()
    prev = {}
    cost = {start_node: 0}
    pq = [(0, start_node)]
    while pq:
        current_cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if node == dest_node:
            break
        for neighbor in graph.get_neighbors(node):
            weight = euclidean_dist(graph.get_position(node), graph.get_position(neighbor))
            total = current_cost + weight
            if neighbor not in cost or total < cost[neighbor]:
                cost[neighbor] = total
                prev[neighbor] = node
                heapq.heappush(pq, (total, neighbor))
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def astar(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)

    def heuristic(node):
        return euclidean_dist(graph.get_position(node), graph.get_position(dest_node))

    open_set = [(heuristic(start_node), start_node)]
    g_score = {start_node: 0}
    parent = {}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == dest_node:
            break
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph.get_neighbors(current):
            tentative_g = g_score[current] + euclidean_dist(graph.get_position(current), graph.get_position(neighbor))
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, neighbor))

    return [graph.get_position(v) for v in reconstruct_path(parent, start_node, dest_node)]

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
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def bellman_ford_negative(start, dest):
    start_node = graph.find_closest_vertex(start)
    dest_node = graph.find_closest_vertex(dest)
    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {}
    dist[start_node] = 0
    for _ in range(len(graph.get_vertices()) - 1):
        for u in graph.get_vertices():
            for v in graph.get_neighbors(u):
                weight = euclidean_dist(graph.get_position(u), graph.get_position(v))
                if v.endswith("0"):
                    weight *= -1
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u
    return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def min_spanning_tree(start, dest):
    parent = {}
    visited = set()
    pq = []
    start_node = graph.find_closest_vertex(start)
    heapq.heappush(pq, (0, start_node, None))

    while pq:
        weight, node, prev_node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        if prev_node is not None:
            parent[node] = prev_node
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                edge_weight = euclidean_dist(graph.get_position(node), graph.get_position(neighbor))
                heapq.heappush(pq, (edge_weight, neighbor, node))

    dest_node = graph.find_closest_vertex(dest)
    return [graph.get_position(v) for v in reconstruct_path(parent, start_node, dest_node)]

def search(algorithm, start, dest):
    if algorithm == 'p2p':
        return point_to_point(start, dest)
    elif algorithm == 'fly':
        return fly(start, dest)
    elif algorithm == 'random':
        return random_graph(start, dest)
    elif algorithm == 'bfs':
        return breadth_first_search(start, dest)
    elif algorithm == 'bfsh':
        return breadth_first_hub(start, dest)
    elif algorithm == 'dfs':
        return depth_first_search(start, dest)
    elif algorithm == 'dfsb':
        return depth_first_best(start, dest)
    elif algorithm == 'bf':
        return bellman_ford(start, dest)
    elif algorithm == 'bfn':
        return bellman_ford_negative(start, dest)
    elif algorithm == 'dijkstra':
        return dijkstra(start, dest)
    elif algorithm == 'astar':
        return astar(start, dest)
    elif algorithm == 'mst':
        return min_spanning_tree(start, dest)
    return []
