from copy import deepcopy

# Constants for cell states
UNFILLED = -2  # Unfilled cell
WATER = -1  # Black cell (sea)
ISLAND = 0  # Regular island cell
NUMBERED = lambda x: x > 0  # Function to check if a cell is a numbered island cell

def solve_nurikabe(grid, solutions, max_solutions=2):
    """
    Recursive backtracking solver to find all solutions to a Nurikabe puzzle.
    - grid: Current puzzle state.
    - solutions: A list to store valid solutions.
    - max_solutions: Stop if more than this number of solutions are found.
    """
    if len(solutions) >= max_solutions:
        return

    if is_complete(grid):
        solutions.append(deepcopy(grid))
        return

    # Find the next unfilled cell to explore
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == UNFILLED:
                # Try filling it with WATER or ISLAND
                for state in [WATER, ISLAND]:
                    grid[x][y] = state
                    if is_valid(grid):
                        solve_nurikabe(grid, solutions, max_solutions)
                    grid[x][y] = UNFILLED  # Backtrack
                return

def is_complete(grid):
    """
    Checks if the grid meets all Nurikabe constraints.
    """
    return all_islands_complete(grid) and is_single_contiguous_water(grid) and no_2x2_water(grid)

def all_islands_complete(grid):
    """
    Checks if all numbered islands are complete and match their constraints.
    """
    visited = set()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if NUMBERED(grid[x][y]) and (x, y) not in visited:
                size = grid[x][y]
                if not bfs_check_island(grid, x, y, size, visited):
                    return False
    return True

def bfs_check_island(grid, start_x, start_y, size, visited):
    """
    Performs BFS to verify an island matches its size constraint.
    """
    queue = [(start_x, start_y)]
    count = 0
    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] not in {ISLAND, UNFILLED} and not NUMBERED(grid[x][y]):
            return False
        count += 1
        if count > size:
            return False
        for nx, ny in neighbors(grid, x, y):
            if (nx, ny) not in visited and grid[nx][ny] in {ISLAND, UNFILLED} or NUMBERED(grid[nx][ny]):
                queue.append((nx, ny))
    return count == size

def is_single_contiguous_water(grid):
    """
    Checks if all water cells form a single contiguous area.
    """
    visited = set()
    found_water = False
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == WATER:
                if found_water:
                    return bfs_check_water(grid, x, y, visited) == sum(
                        1 for row in grid for cell in row if cell == WATER
                    )
                else:
                    found_water = True
    return True

def bfs_check_water(grid, start_x, start_y, visited):
    """
    Performs BFS to count all contiguous water cells.
    """
    queue = [(start_x, start_y)]
    count = 0
    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] != WATER:
            return 0
        count += 1
        for nx, ny in neighbors(grid, x, y):
            if (nx, ny) not in visited and grid[nx][ny] == WATER:
                queue.append((nx, ny))
    return count

def no_2x2_water(grid):
    """
    Checks that no 2x2 block of water cells exists.
    """
    for x in range(len(grid) - 1):
        for y in range(len(grid[0]) - 1):
            if all(grid[x + dx][y + dy] == WATER for dx in range(2) for dy in range(2)):
                return False
    return True

def neighbors(grid, x, y):
    """
    Returns the valid neighbors of a cell in the grid.
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            yield nx, ny

def is_valid(grid):
    """
    Checks if the grid is valid so far (doesn't violate constraints).
    """
    return no_2x2_water(grid) and partial_islands_valid(grid)

def partial_islands_valid(grid):
    """
    Checks if numbered islands are valid so far (don't exceed size constraints).
    """
    visited = set()
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if NUMBERED(grid[x][y]) and (x, y) not in visited:
                size = grid[x][y]
                if not bfs_check_partial_island(grid, x, y, size, visited):
                    return False
    return True

def bfs_check_partial_island(grid, start_x, start_y, size, visited):
    """
    Checks if the partial island is valid (doesn't exceed size).
    """
    queue = [(start_x, start_y)]
    count = 0
    while queue:
        x, y = queue.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] not in {ISLAND, UNFILLED} and not NUMBERED(grid[x][y]):
            return False
        count += 1
        if count > size:
            return False
        for nx, ny in neighbors(grid, x, y):
            if (nx, ny) not in visited and (grid[nx][ny] in {ISLAND, UNFILLED} or NUMBERED(grid[nx][ny])):
                queue.append((nx, ny))

    print("Truwe")
    return True

def is_unique(grid):
    """
    Verifies if the Nurikabe puzzle has a unique solution.
    """
    solutions = []
    solve_nurikabe(grid, solutions)
    print(solutions)
    return len(solutions) == 1

# Example usage
initial_grid = [
    [-2, -2, -2, -2, -2],
    [1, -2, 1, -2, 2],
    [-2, -2, -2, -2, -2],
    [2, -2, -2, -2, 1],
    [-2, -2, 2, -2, -2],
]  # Example grid
print("Is the puzzle unique?", is_unique(initial_grid))
