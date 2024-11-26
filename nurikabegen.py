import random

'''

Output unsolved nurikabe format:

Any number > 0 is a numbered cell, which counts as an island, is given
Cell with string "." is an empty cell, which the player must fill in with either 0, an island cell, or -1, a water cell


Output solved nurikabe format:

Any number > 0 is a numbered cell, which counts as an island
Number = 0 is an island cell
Number = -1 is a water cell

'''

def isFilled(grid):
    for i in grid:
        for j in i:
            if j == 0:
                return False;
    return True;

def find_empty_cell(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ".":
                return (i, j);
    return None;


def find_first_water_cell(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == -1:
                return (i, j);
    return None;

def return_all_island_cells(grid):
    allcells = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                allcells.append((i, j));
    return allcells;

def get_neighbours(x, y):
    # return all neighbours of a cell
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)];

def get_2x2_neighbours(x, y):
    # x y
    # y y
    # return all y in the grid given x
    return [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)];


def check_in_bounds(grid, x, y):
    # check if a neighboured cell is within the bounds of the grid
    return x >= 0 and y >= 0 and x < len(grid) and y < len(grid[0]);

def flood_fill_water_connected(grid, x, y, visited, cellType):
    stack = [(x, y)];
    visited[x][y] = True;

    while stack:
        (cx, cy) = stack.pop();

        # check all neighbours
        for (Nx, Ny) in get_neighbours(cx, cy):
            # if the neighbour is within bounds, not visited, and is the same cell type (water)
            if check_in_bounds(grid, Nx, Ny) and not visited[Nx][Ny] and grid[Nx][Ny] == cellType:
                stack.append((Nx, Ny));
                visited[Nx][Ny] = True;

    return visited;

def flood_fill_island_count(grid, x, y, visited, cellType, wrongType):
    stack = [(x, y)];
    visited[x][y] = True;
    count = 1 # to include the starting numbered cell

    while stack:
        (cx, cy) = stack.pop();

        # check all neighbours
        for (Nx, Ny) in get_neighbours(cx, cy):
            # if the neighbour is within bounds, not visited, and is the same cell type (water)
            if check_in_bounds(grid, Nx, Ny) and not visited[Nx][Ny]:
                if grid[Nx][Ny] == cellType:
                    stack.append((Nx, Ny));
                    visited[Nx][Ny] = True;
                    count += 1;
                elif not wrongType == None and grid[Nx][Ny] == wrongType:
                    return -1;

    return count;

def flood_fill_island_positions(grid, x, y, visited, cellType, wrongType):
    stack = [(x, y)];
    visited[x][y] = True;
    count = 1
    island_cells = [(x, y)];

    while stack:
        (cx, cy) = stack.pop();

        # check all neighbours
        for (Nx, Ny) in get_neighbours(cx, cy):
            # if the neighbour is within bounds, not visited, and is the same cell type (water)
            if check_in_bounds(grid, Nx, Ny) and not visited[Nx][Ny]:
                if grid[Nx][Ny] == cellType:
                    stack.append((Nx, Ny));
                    island_cells.append((Nx, Ny));
                    visited[Nx][Ny] = True;
                    count += 1;
                elif not wrongType == None and grid[Nx][Ny] == wrongType:
                    return -1;

    return count, island_cells;

def flood_fill_unnumbered(grid, x, y, visited, cellType, wrongType):
    stack = [(x, y)];
    visited[x][y] = True;

    while stack:
        (cx, cy) = stack.pop();

        # check all neighbours
        for (Nx, Ny) in get_neighbours(cx, cy):
            # if the neighbour is within bounds, not visited, and is the same cell type (water)
            if check_in_bounds(grid, Nx, Ny): # and not visited[Nx][Ny]:
                if grid[Nx][Ny] == cellType:
                    stack.append((Nx, Ny));
                    visited[Nx][Ny] = True;
                if not wrongType == None and grid[Nx][Ny] > wrongType: # if the cell is a numbered cell
                    return True;

    return False; # no numbered cells found

def all_water_connected(grid):
    # use flood fill to check if all water cells are connected
    # temporary matrix to keep track of visited cells
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    # find first water cell
    cell = find_first_water_cell(grid);
    if cell == None:
        return True; # there are no water cells, so they technically are all connected. other functions will check for validity
    (startx, starty) = cell;

    # flood fill, starting from the first water cell
    visited = flood_fill_water_connected(grid, startx, starty, visited, -1);

    # check if all water cells are visited
    for i in range(len(visited)):
        for j in range(len(visited[0])):
            if not visited[i][j] and grid[i][j] == -1:
                return False;

    return True;

def correct_island_size(grid):
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 0 and not visited[i][j]: # if the cell is a numbered cell and not visited
                count = flood_fill_island_count(grid, i, j, visited, 0, None);
                if count != grid[i][j]: # if the count of cells in island is not equal to the number on the cell
                    return False;
    
    return True;

def has_pool(grid):
    # if a 2x2 square of water exists, that must mean a pool of any size exists
    result = False;

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (grid[i][j] == -1):
                result = True; # assume pool until proven false
                for (Px, Py) in get_2x2_neighbours(i, j):
                    if check_in_bounds(grid, Px, Py):
                        if grid[Px][Py] > -1:
                            result = False;
                    # edge of grid, cannot be a pool
                    else:
                        result = False;
                if result:
                    return True;

    return False;

def has_connected_islands(grid):
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 0 and not visited[i][j]: # if the cell is a numbered cell and not visited
                count = flood_fill_island_count(grid, i, j, visited, 0, 1);
                if count == -1:
                    return True;
    
    return False;

def has_unnumbered_islands(grid):
    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0 and not visited[i][j]: # if the cell is an island cell and not visited
                if not flood_fill_unnumbered(grid, i, j, visited, 0, 0):
                    return True;
    
    return False;

def check_for_violations(grid):
    # check if all water cells are connected
    if not all_water_connected(grid):
        print("Water cells are not connected")
        return False;

    # check for pools
    if has_pool(grid):
        print("Pool exists")
        return False;

    # check for correct island size
    if not correct_island_size(grid):
        print("Island size is incorrect")
        return False;

    # check for no connected islands
    if has_connected_islands(grid):
        print("Connected islands exist")
        return False;

    if has_unnumbered_islands(grid):
        print("Unnumbered islands exist")
        return False;

    return True;

def solve_nurikabe(grid):
    # implement later, make sure nurikabe is solvable

    # rules to keep in mind:
    # player must fill in the grid such that:
    # each numbered cell has an island (non-filled in squares)
    # a numbered cell shows how many cells make up that island
    # each island can only contain one numbered cell
    # there is only one sea (must all be connected), no pools allowed, i.e. 2+ x 2+ sized squares.

    # methods to check for solution validity:
    # 

    #if check_for_violations(grid):
    #    return grid;

    number_position_pairs = [] # cell position, numbered cell number

    all_island_cells = return_all_island_cells(grid);
    if len(all_island_cells) == 0:
        return grid;

    visited = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    
    while len(all_island_cells) > 0:
        count, cell_positions = flood_fill_island_positions(grid, all_island_cells[0][0], all_island_cells[0][1], visited, 0, 0);
        number_position_pairs.append((random.choice(cell_positions), count));
        for cell in cell_positions:
            all_island_cells.remove(cell);

    # print grid in formatted way
    for i in range(len(grid)):
        string = ""
        for j in range(len(grid[0])):
            if (i, j) in [x[0] for x in number_position_pairs]:
                string += str([x[1] for x in number_position_pairs if x[0] == (i, j)][0]) + " "
            elif grid[i][j] == -1:
                string += "- "
            else:
                string += str(grid[i][j]) + " "
        print(string)
    print("\n")



def generate_islands(grid, sizex, sizey, island_count, maxsize):
    # Randomly place numbered islands on the grid.
    for _ in range(island_count):
        while True:
            x, y = random.randint(0, sizex - 1), random.randint(0, sizey - 1)
            if grid[y][x] == 0:
                grid[y][x] = random.randint(1, maxsize) # random island size depending on input
                break
    return grid

def generate_nurikabe(sizex, sizey, max_islands, max_island_size):
    # Generate a Nurikabe puzzle of a given grid size and max islands
    grid = [[0 for _ in range(sizex)] for _ in range(sizey)]
    print(grid)
    grid = generate_islands(grid, sizex, sizey, max_islands, max_island_size)

    solved = solve_nurikabe(grid);
        # Retry generation if the grid is invalid.
        #return generate_nurikabe(sizex, sizey, max_islands, max_island_size)

    return grid, solved

#Testing

# generates all possible combinations of one row
def generate_rows(index, generated_rows, pattern, sizex, sizey):
    if index < sizex:
        pattern[index] = -1
        generate_rows(index + 1, generated_rows, pattern, sizex, sizey)

        pattern[index] = 0
        generate_rows(index + 1, generated_rows, pattern, sizex, sizey)
    else:
        final_pattern = pattern.copy()
        generated_rows.append(final_pattern)

    return generated_rows

def generate_random_rows(index, generated_rows, pattern, sizex, sizey):
    if index < sizex:
        pattern[index] = random.randint(-1, 0)
        generate_random_rows(index + 1, generated_rows, pattern, sizex, sizey)

        pattern[index] = random.randint(-1, 0)
        generate_random_rows(index + 1, generated_rows, pattern, sizex, sizey)
    else:
        final_pattern = pattern.copy()
        if final_pattern not in generated_rows:
            generated_rows.append(final_pattern)

    return generated_rows

def generate_water_pattern2(index, pattern, generated_rows, pattern_count, recursive_calls, pattern_check, sizex, sizey):
    if recursive_calls % 1000 == 0:
        print("Progress: ", pattern_count)

    if index < sizey:
        for row in generated_rows:
            pattern[index] = row

            #print(pattern, index)

            if index != 0:
                #if pattern[index - 1] == pattern[index]:
                #    return
                pattern_check = not has_pool(pattern)
                if pattern_check:
                    pattern_check = all_water_connected(pattern)
                    if not pattern_check:
                        if index < (sizey - 1):
                            for row_index in generated_rows:
                                pattern[index + 1] = row_index
                                if all_water_connected(pattern):
                                    break

            if pattern_check or index == 0:
                generate_water_pattern(index + 1, pattern, generated_rows, pattern_count, recursive_calls, pattern_check, sizex, sizey)
                recursive_calls += 1
    elif pattern_check:
        pattern_count += 1
        print(pattern)
        if pattern not in matrix_list:
            matrix_list.append(pattern[:])

def generate_water_pattern(index, pattern, generated_rows, pattern_count, recursive_calls, pattern_check, sizex, sizey):
    if index == sizey:
        # Validate the final pattern before adding it to the matrix_list
        if all_water_connected(pattern) and not has_pool(pattern):
            matrix_list.append([row.copy() for row in pattern])  # Add a deep copy of the pattern
        return
    random.shuffle(generated_rows)
    for row in generated_rows:
        pattern[index] = row
        if index > 0:
            # Validate partial patterns only if they connect properly
            partial_valid = all_water_connected(pattern) and not has_pool(pattern)
            if not partial_valid:
                continue  # Skip invalid partial patterns

        generate_water_pattern(index + 1, pattern, generated_rows, pattern_count, recursive_calls, pattern_check, sizex, sizey)

def print_grid(grid):
    for row in grid:
        print(" ".join(str(cell) if cell > 0 else "." for cell in row))

def seed_islands(grid, max_islands, max_island_size):
    """Place numbered cells and grow islands."""
    for _ in range(max_islands):
        size = random.randint(1, max_island_size)
        x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1)

        # Place numbered cell
        if grid[x][y] == ".":
            grid[x][y] = size
            grow_island(grid, x, y, size)

def grow_island(grid, x, y, size):
    """Grow an island from a numbered cell."""
    stack = [(x, y)]
    while stack and size > 1:
        cx, cy = stack.pop()
        for nx, ny in get_neighbours(cx, cy):
            if check_in_bounds(grid, nx, ny) and grid[nx][ny] == ".":
                grid[nx][ny] = 0  # Mark as island
                stack.append((nx, ny))
                size -= 1
                if size == 1:
                    break


if __name__ == "__main__":
    # Customize grid size and island count
    grid_size_x = 5
    grid_size_y = 7
    max_islands = 5
    max_island_size = 3

    sizex = 5
    sizey = 5
    amount = 10
    generated_rows = []
    matrix_list = []
    pattern = [0] * sizex
    patternLast = []

    puzzle = [
        [0, 2, -1, -1, -1], #   2 - - -
        [-1, -1, 1, -1, 2], # - - 1 - 2
        [0, -1, -1, -1, 0], #   - - -   
        [2, -1, 2, -1, -1], # 2 - 2 - -
        [-1, -1, 0, -1, 1], # - -   - 1
    ]
    
    #print(is_valid_nurikabe(puzzle))

    for i in range(sizey):
        patternLast.append([0] * sizex)
    generated_rows = generate_random_rows(0, generated_rows, pattern, sizex, sizey)
    #print(generated_rows)
    while len(generated_rows) < amount:
        generated_rows = generate_random_rows(0, generated_rows, pattern, sizex, sizey)
    for i in range(len(generated_rows) - amount):
        generated_rows.pop()
    print(generated_rows)
    generate_water_pattern(0, patternLast, generated_rows, 0, 0, True, sizex, sizey)
    #print(matrix_list)
    
    #for grid in matrix_list:
    #    solve_nurikabe(grid)

    for i in range(10):
        solve_nurikabe(random.choice(matrix_list))

    #puzzle = generate_nurikabe(grid_size_x, grid_size_y, max_islands, max_island_size)
    #print_grid(puzzle)
