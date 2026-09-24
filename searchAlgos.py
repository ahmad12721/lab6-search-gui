import math
import heapq


# ---------------------------------------------------------------------------
# Hospital coordinates and weighted graph (same as Task 3 in the lab notebook)
# ---------------------------------------------------------------------------

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}


# ---------------------------------------------------------------------------
# Euclidean heuristic
# ---------------------------------------------------------------------------

def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# ---------------------------------------------------------------------------
# Greedy Best-First Search : f(n) = h(n)
# ---------------------------------------------------------------------------

def gbfs(graph, start, goal):

    frontier = [(heuristic(start, goal), start)]
    visited = set()
    parent = {start: None}
    expansion_order = []

    while frontier:

        _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        # Goal test when node is removed from the priority queue
        if current == goal:
            break

        for neighbor in graph[current]:
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    if goal not in parent:
        return None, None, expansion_order

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    # Actual path cost (GBFS ignores cost while searching, but we still report it)
    total_cost = sum(graph[a][b] for a, b in zip(path, path[1:]))

    return path, total_cost, expansion_order


# ---------------------------------------------------------------------------
# A* Search : f(n) = g(n) + h(n)
# ---------------------------------------------------------------------------

def a_star(graph, start, goal):

    g_cost = {start: 0}
    came_from = {start: None}
    frontier = [(heuristic(start, goal), start)]
    visited = set()
    expansion_order = []

    while frontier:

        _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        # Goal test when node is removed from the priority queue
        if current == goal:
            break

        for neighbor, cost in graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                f_n = new_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_n, neighbor))

    if goal not in came_from:
        return None, None, expansion_order

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()

    return path, g_cost[goal], expansion_order
