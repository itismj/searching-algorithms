from queue import PriorityQueue, Queue
import time
import pygame
from utilities import h, reconstruct_path

def uniform_cost_search(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # Start with cost 0
    came_from = {}
    cost_so_far = {spot: float('inf') for row in grid for spot in row}
    cost_so_far[start] = 0
    open_set_hash = {start}

    start_time = time.time()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        if current in open_set_hash:
            open_set_hash.remove(current)
        nodes_visited += 1

        if current == end:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Uniform Cost Search completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            path_length = reconstruct_path(came_from, end, draw)
            print(f"Path length is {path_length}")
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1  # Assuming uniform cost of 1 for each step. If not uniform, change this.

            if new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((new_cost, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                elif neighbor in open_set_hash and came_from.get(neighbor) is None:
                    came_from[neighbor] = current

        max_frontier = max(max_frontier, len(open_set_hash))
        draw()
        pygame.time.delay(10)
        if current != start:
            current.make_closed()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Uniform Cost Search completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False