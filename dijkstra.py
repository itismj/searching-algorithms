from queue import PriorityQueue
import time
import pygame
from utilities import h, reconstruct_path


def dijkstra(draw, grid, start, end):
    nodes_visited = 0
    max_frontier = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # Start with a distance of 0
    came_from = {}
    distance = {spot: float("inf") for row in grid for spot in row}
    distance[start] = 0
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
            print(f"Dijkstra's Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_distance = distance[current] + 1  # Assuming each edge has a weight of 1

            if temp_distance < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = temp_distance
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((temp_distance, count, neighbor))
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
    print(f"Dijkstra's Algorithm completed in {elapsed_time:.4f} seconds with {nodes_visited} nodes visited and {max_frontier} max frontier size.")
    return False