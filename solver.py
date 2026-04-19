from collections import deque

def solve(grid, width, height):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # reset visited
    for x in range(width):
        for y in range(height):
            grid[x][y].visited = False

    start = grid[0][0]
    end = grid[width - 1][height - 1]

    q = deque()
    q.append((start, [start]))
    start.visited = True

    while q:
        node, path = q.popleft()

        if node == end:
            return [(c.x, c.y) for c in path]

        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            neighbor = grid[nx][ny]

            # wall checks
            if dx == 1 and node.walls["right"]:
                continue
            if dx == -1 and node.walls["left"]:
                continue
            if dy == 1 and node.walls["bottom"]:
                continue
            if dy == -1 and node.walls["top"]:
                continue

            if neighbor.visited:
                continue

            neighbor.visited = True
            q.append((neighbor, path + [neighbor]))

    return None