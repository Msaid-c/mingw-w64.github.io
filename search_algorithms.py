import math
import json
import heapq
from queue import Queue
from collections import defaultdict

graph = MapGraph('graph.json')
def euclidean_dist(a, b):
   return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
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
   visited = set()
   prev = {}
   g_score = {start_node: 0}
   f_score = {start_node: heuristic(start_node)}
   pq = [(f_score[start_node], start_node)]
   while pq:
       _, node = heapq.heappop(pq)
       if node == dest_node:
           break
       if node in visited:
           continue
       visited.add(node)
       for neighbor in graph.get_neighbors(node):
           tentative_g = g_score[node] + euclidean_dist(graph.get_position(node), graph.get_position(neighbor))
           if neighbor not in g_score or tentative_g < g_score[neighbor]:
               prev[neighbor] = node
               g_score[neighbor] = tentative_g
               f_score[neighbor] = tentative_g + heuristic(neighbor)
               heapq.heappush(pq, (f_score[neighbor], neighbor))
   return [graph.get_position(v) for v in reconstruct_path(prev, start_node, dest_node)]

def bellman_ford(start, dest):


def min_spanning_tree(start, dest):

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
