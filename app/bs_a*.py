#A star algorithm modified from https://www.redblobgames.com/pathfinding/a-star/implementation.html

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, end)
    path = PriorityQueue()
    path.put(start, 0)
    origin = {}
    current_cost = {}
    origin[start] = None
    current_cost[start] = 0
    
    while not path.empty():
        current = path.get()
        
        if current == end:
            break
            
        for next in graph.neighbors(current):
            new_cost = current_cost[current] + graph.cost(current, next)
            if next not in current_cost or new_cost < current_cost[next]:
                current_cost[next] = new_cost
                priority = new_cost + heuristic(end, next)
                path.put(next, priority)
                origin[next] = current
                
    return origin