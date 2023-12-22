# Day 21: Step Counter


## Part One


64 = 3746
65 = 3889
100 = 6829
101 = 6865

total



def bfs(matrix, start, step_count):
    visited = set()
    queue = deque([(start, 0)])
    while queue:
        (row, col), steps = queue.popleft()
        if steps > step_count:
            continue
        for dr, dc in DIRECTIONS:
            new_row, new_col = row + dr, col + dc
            if matrix[new_row][new_col] != ROCK and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append(((new_row, new_col), steps + 1))
    return len(
        [(row, col) for row, col in visited if (row + col) % 2 == step_count % 2]
    )

def main():
    with open(FILENAME) as input_file:
        matrix = input_file.read().split("\n")
    start = len(matrix) // 2, len(matrix) // 2
    visited = bfs(matrix, start, 64)
    print(visited)

    expanded = expand_matrix(matrix, 7)
    start = len(expanded) // 2, len(expanded) // 2
    y_values = [bfs(expanded, start, step_count) for step_count in [65, 196, 327]]
    # 65, 65 + 131, 65 + 131 * 2
    x_values = np.array([0, 1, 2])

    target = (26501365 - 65) // 131
    coefficients = np.polyfit(x_values, y_values, 2)
    result = np.polyval(coefficients, target)
    print(np.round(result, 0))