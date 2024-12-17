from queue import PriorityQueue, Queue
import time
import pygame
from utilities import h, reconstruct_path

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