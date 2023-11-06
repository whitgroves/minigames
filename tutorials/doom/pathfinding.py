from collections import deque

class Pathfinding:
    def __init__(self, game) -> None:
        self.game = game
        self.map = game.map.mini_map
        # all possible vectors of movement from this block to the adjacent ones
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.build_graph()
        
    def get_path(self, start, goal):
        self.visited = self.breadcrumbs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)
        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]
        
    def breadcrumbs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}
        while queue:
            cur_block = queue.popleft()
            if cur_block == goal:
                break
            next_blocks = graph[cur_block]
            for block in next_blocks:
                if block not in visited and block not in self.game.object_manager.npc_locs:
                    queue.append(block)
                    visited[block] = cur_block
        return visited
        
    def get_adjacent_blocks(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]
        
    def build_graph(self):
        for y, row in enumerate(self.map):
            for x, val in enumerate(row):
                if not val:  # i.e., an empty cell
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_adjacent_blocks(x, y)