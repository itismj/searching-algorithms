import pygame
import math
from queue import PriorityQueue, Queue
import time

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE
	def is_path(self):
		return self.color == PURPLE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()



def algorithm(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0  # Correct frontier tracking
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    start_time = time.time()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_visited += 1

        if current == end:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"A* Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        max_frontier = max(max_frontier, len(open_set_hash)) # Correct frontier tracking
        draw()
        if current != start:
            current.make_closed()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"A* Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False

def bfs_algorithm(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0  # Correct frontier tracking
    q = Queue()
    q.put(start)
    visited = {start}
    came_from = {}

    start_time = time.time()
    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = q.get()
        nodes_visited += 1

        if current == end:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"BFS Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                q.put(neighbor)
                neighbor.make_open()

        max_frontier = max(max_frontier, q.qsize()) # Correct frontier tracking
        draw()
        if current != start:
            current.make_closed()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"BFS Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False


def dfs_algorithm(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0  # Correct frontier tracking
    stack = [start]
    visited = {start}
    came_from = {}

    start_time = time.time()
    while stack:
        for event in pygame.event.get():  # Keep event handling here for responsiveness
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = stack.pop()
        nodes_visited += 1
        
        if current == end:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"DFS Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        max_frontier = max(max_frontier, len(stack)) # Update max frontier
        draw()
        if current != start:
            current.make_closed()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"DFS Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False


def greedy_best_first_search(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # Start with a heuristic of 0
    came_from = {}
    open_set_hash = {start}

    start_time = time.time()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_visited += 1

        if current == end:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Greedy Best-First Search completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in open_set_hash and not neighbor.is_barrier():  # Check if not in open set or is barrier
                count += 1
                heuristic = h(neighbor.get_pos(), end.get_pos())  # Calculate heuristic
                open_set.put((heuristic, count, neighbor))
                open_set_hash.add(neighbor)
                came_from[neighbor] = current
                neighbor.make_open()

        # Update max frontier size based on open_set.queue
        max_frontier = max(max_frontier, len(open_set.queue))

        draw()
        pygame.time.delay(10)  # Add a small delay to prevent the UI from freezing
        if current != start:
            current.make_closed()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Greedy Best-First Search completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False

def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_a and start and end: # A for A_star
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_b and start and end: # B for BFS
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)

					bfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_d and start and end: # D for DFS
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)

					dfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_g and start and end: # G for Greedy Search
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)

					greedy_best_first_search(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)