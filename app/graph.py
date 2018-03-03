class graph(object):
    no_go_zones = []
    width = -1
    height = -1
    
    def init(self, width, height):
        self.width = width
        self.height = height
        
    def refresh(self, board_stats):
        self.no_go_zones = []
        other_snakes = board_stats['other_snakes']
        
        for snake in other_snakes:
            nodes = snake['nodes']
            for node in range(len(nodes) - 1):
                xy_pos = nodes[node]
                x_pos = node[0]
                y_pos = node[1]
                self.no_go_zones.append((x_pos, y_pos))
                
    def neighbors(self, node):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]
        n_up = (node[0] + up[0], node[1] + up[1])
        n_down = (node[0] + down[0], node[1] + down[1])
        n_left = (node[0] + left[0], node[1] + left[1])
        n_right = (node[0] + right[0], node[1] + right[1])
        n_temp = [n_up, n_down, n_left, n_right]
        neighbors = []
        for neighbor in n_temp:
            if self.check_bounds(neighbor) and neighbor not in self.no_go_zones:
                neighbors.append(neighbor)
        return neighbors
            
    def check_bounds(self, node):
        if node[0] < 0 or node[0] >= self.width:
            return False
        if node[1] < 0 or node[1] >= self.height:
            return False
        return True
    
    def cost(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

