from queue import PriorityQueue
import time
import pygame
from utilities import h, reconstruct_path
from eda import record_metrics




def astar_algorithm(draw, grid, start, end):
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
            record_metrics("A*", True, elapsed_time)  # Record success
            path_length = reconstruct_path(came_from, end, draw)
            print(f"Path length is {path_length}")
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
            # pygame.time.delay(100) # To slow down the search


    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"A* Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    record_metrics("A*", False, elapsed_time)  # Record failure
    return False

