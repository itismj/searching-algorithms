import random

def generate_maze(grid):
    # Helper function to get neighbors for maze generation
    def get_neighbors(spot, grid):
        neighbors = []
        row, col = spot.row, spot.col
        # Check for valid neighbors in the grid
        if row > 1 and grid[row - 2][col].is_barrier():  # Up
            neighbors.append((grid[row - 2][col], grid[row - 1][col]))
        if row < len(grid) - 2 and grid[row + 2][col].is_barrier():  # Down
            neighbors.append((grid[row + 2][col], grid[row + 1][col]))
        if col > 1 and grid[row][col - 2].is_barrier():  # Left
            neighbors.append((grid[row][col - 2], grid[row][col - 1]))
        if col < len(grid[0]) - 2 and grid[row][col + 2].is_barrier():  # Right
            neighbors.append((grid[row][col + 2], grid[row][col + 1]))
        return neighbors

    # Helper function to check if a cell is a dead end
    def is_dead_end(spot, grid):
        row, col = spot.row, spot.col
        open_neighbors = 0
        # Count the number of open neighbors
        if row > 0 and not grid[row - 1][col].is_barrier():
            open_neighbors += 1
        if row < len(grid) - 1 and not grid[row + 1][col].is_barrier():
            open_neighbors += 1
        if col > 0 and not grid[row][col - 1].is_barrier():
            open_neighbors += 1
        if col < len(grid[0]) - 1 and not grid[row][col + 1].is_barrier():
            open_neighbors += 1
        return open_neighbors == 1  # Dead end if only one open neighbor

    # Initialize the maze with barriers everywhere
    for row in grid:
        for spot in row:
            spot.make_barrier()

    # Randomly pick a starting cell
    start_row = random.randrange(1, len(grid) - 1, 2)
    start_col = random.randrange(1, len(grid[0]) - 1, 2)
    stack = [grid[start_row][start_col]]
    grid[start_row][start_col].reset()  # Open starting point

    # Maze generation using recursive backtracking
    while stack:
        current = stack[-1]
        neighbors = get_neighbors(current, grid)

        if neighbors:  # If there are unvisited neighbors
            next_cell, wall_between = random.choice(neighbors)
            next_cell.reset()  # Open the neighbor cell
            wall_between.reset()  # Remove the wall between
            stack.append(next_cell)  # Visit the neighbor
        else:
            stack.pop()  # Backtrack if no unvisited neighbors

    # Ensure the edges are covered with walls
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        grid[i][0].make_barrier()    # Leftmost column
        grid[i][-1].make_barrier()   # Rightmost column
    for j in range(cols):
        grid[0][j].make_barrier()    # Top row
        grid[-1][j].make_barrier()   # Bottom row

    # Remove dead ends by connecting them to other paths, avoiding edge cells
    for row in grid[1:-1]:  # Skip the top and bottom edge rows
        for spot in row[1:-1]:  # Skip the leftmost and rightmost edge columns
            if is_dead_end(spot, grid):  # If the cell is a dead end
                r, c = spot.row, spot.col
                neighbors = []
                # Check all valid neighbors
                if r > 1 and grid[r - 1][c].is_barrier():  # Up
                    neighbors.append(grid[r - 1][c])
                if r < rows - 2 and grid[r + 1][c].is_barrier():  # Down
                    neighbors.append(grid[r + 1][c])
                if c > 1 and grid[r][c - 1].is_barrier():  # Left
                    neighbors.append(grid[r][c - 1])
                if c < cols - 2 and grid[r][c + 1].is_barrier():  # Right
                    neighbors.append(grid[r][c + 1])

                # Randomly open a barrier to connect the dead end
                if neighbors:
                    random.choice(neighbors).reset()