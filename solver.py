from collections import deque

def solve_bfs(grid, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Reset visited
    for x in range(width):
        for y in range(height):
            grid[x][y].visited = False

    # Entrance at top-left; exit at bottom-right
    start = grid[0][0]
    end = grid[width - 1][height - 1]

    q = deque()
    q.append((start, [start]))
    start.visited = True

    # Continues until there are no more unvisited nodes within the queue
    while q:
        # Removes and returns the first item (FIFO)
        node, path = q.popleft()

        # If the current node is the exit, return the path taken to get there for rendering
        # Use (x,y) and not cell object for ease of access
        if node == end:
            return [(c.x, c.y) for c in path]

        # Checks neighbors in all 4 cardinal directions
        for dx, dy in directions:
            # Compute the neighboring cell by adding direction offsets
            nx, ny = node.x + dx, node.y + dy

            # Ensures the neighbor is within grid bounds
            if not (0 <= nx < width and 0 <= ny < height):
                continue

            neighbor = grid[nx][ny]

            # Wall checks; Cannot continue moving in a direction if there is a wall
            if dx == 1 and node.walls["right"]:
                continue
            if dx == -1 and node.walls["left"]:
                continue
            if dy == 1 and node.walls["bottom"]:
                continue
            if dy == -1 and node.walls["top"]:
                continue

            # Avoid cycles and redundency by skipping visited neighbors
            if neighbor.visited:
                continue

            # Mark before enqueing and updates path
            # TODO: inefficiency in creating new list in the queue
            neighbor.visited = True
            q.append((neighbor, path + [neighbor]))

    # If there is no valid solution
    return None