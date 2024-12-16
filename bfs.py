from collections import deque

def bfs_algorithm(grid, start, end):
    # BFS Implementation
    rows, cols = len(grid), len(grid[0])
    queue = deque([start])
    visited = set()
    parent = {}

    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    return []

def get_neighbors(node, grid):
    row, col = node
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 0:
            neighbors.append((r, c))
    return neighbors
