import pygame
import math
from queue import PriorityQueue, Queue
import time
import random
from maze_generator import generate_maze
from astar import astar_algorithm
from bfs import bfs_algorithm
from dfs import dfs_algorithm
from dijkstra import dijkstra
from uniform_cost import uniform_cost_search
from utilities import draw, get_clicked_pos, make_grid

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

					astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

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
							
				if event.key == pygame.K_j and start and end: # G for Djikstra Search
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)
					dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
					
				if event.key == pygame.K_u and start and end: # u for Uniform Cost Search
					for row in grid:
						for spot in row:
							if spot.is_open() or spot.is_closed() or spot.is_path():  # If the spot was previously closed
								spot.reset()
							spot.update_neighbors(grid)
					uniform_cost_search(lambda: draw(win, grid, ROWS, width), grid, start, end)
				if event.key == pygame.K_m:  # Generate maze
					start = None
					end = None
					generate_maze(grid)
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)