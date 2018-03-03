#A star algorithm modified from https://www.redblobgames.com/pathfinding/a-star/implementation.html

from Queue import PriorityQueue

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, end):
    path = PriorityQueue()
    path.put((0, start))
    origin = {}
    current_cost = {}
    origin[start] = None
    current_cost[start] = 0
    
    while not path.empty():
        current = path.get()[1]
        
        if current == end:
            break
            
        for next_node in graph.neighbors(current):
            new_cost = current_cost[current] + 1#graph.cost(current, next_node)
            if next_node not in current_cost or new_cost < current_cost[next_node]:
                current_cost[next_node] = new_cost
                priority = new_cost + heuristic(end, next_node)
                path.put((priority, next_node))
                origin[next_node] = current
                
    return origin