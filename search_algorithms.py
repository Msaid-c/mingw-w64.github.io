from queue import Queue

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

def breadth_first(graph, start, goal):
    start = graph.find_closest_vertex(start)
    goal = graph.find_closest_vertex(goal)
    queue = Queue()
    visited = set()
    prev = {}

    queue.put(start)
    visited.add(start)

    while not queue.empty():
        current = queue.get()
        if current == goal:
            break
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                prev[neighbor] = current
                queue.put(neighbor)

    return reconstruct_path(prev, start, goal)

def depth_first(graph, start, goal):
    start = graph.find_closest_vertex(start)
    goal = graph.find_closest_vertex(goal)
    stack = [(start, [start])]
    visited = set()

    while stack:
        current, path = stack.pop()
        if current == goal:
            return path
        if current not in visited:
            visited.add(current)
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    return []
