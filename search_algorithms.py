import math
import heapq
from queue import Queue


def breadth_first(start_point, end_point):
    graph = MapGraph('graph.json')
    source = graph.find_closest_vertex(start_point)
    target = graph.find_closest_vertex(end_point)

    q = Queue()
    q.put((source, [source]))
    visited = {source}

    while not q.empty():
        node, path = q.get()
        if node == target:
            return [graph.get_position(n) for n in path]

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                q.put((neighbor, path + [neighbor]))

    return []


def depth_first(start_point, end_point):
    graph = MapGraph('graph.json')
    start = graph.find_closest_vertex(start_point)
    goal = graph.find_closest_vertex(end_point)

    stack = [(start, [start])]
    seen = set()

    while stack:
        node, path = stack.pop()
        if node == goal:
            return [graph.get_position(n) for n in path]

        if node not in seen:
            seen.add(node)
            for neighbor in graph.get_neighbors(node):
                if neighbor not in seen:
                    stack.append((neighbor, path + [neighbor]))

    return []


def dijkstra(start_point, end_point):
    graph = MapGraph('graph.json')
    start = graph.find_closest_vertex(start_point)
    end = graph.find_closest_vertex(end_point)

    dist = {v: float('inf') for v in graph.get_vertices()}
    prev = {}
    dist[start] = 0

    heap = [(0, start)]

    while heap:
        curr_dist, curr = heapq.heappop(heap)

        if curr == end:
            break

        for neighbor in graph.get_neighbors(curr):
            weight = euclidean_dist(graph.get_position(curr), graph.get_position(neighbor))
            alt = curr_dist + weight

            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = curr
                heapq.heappush(heap, (alt, neighbor))

    path = []
    node = end
    while node in prev:
        path.insert(0, node)
        node = prev[node]
    if node == start:
        path.insert(0, start)
        return [graph.get_position(n) for n in path]

    return []


def bellman_ford(start_point, end_point):
    graph = MapGraph('graph.json')
    source = graph.find_closest_vertex(start_point)
    target = graph.find_closest_vertex(end_point)

    vertices = graph.get_vertices()
    dist = {v: float('inf') for v in vertices}
    prev = {}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        for u in vertices:
            for v in graph.get_neighbors(u):
                w = euclidean_dist(graph.get_position(u), graph.get_position(v))
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u

    path = []
    node = target
    while node in prev:
        path.insert(0, node)
        node = prev[node]
    if node == source:
        path.insert(0, source)
        return [graph.get_position(n) for n in path]

    return []


def breadth_first_hub(start, dest):
    return []

def bellman_ford_negative(start, dest):
    return []
