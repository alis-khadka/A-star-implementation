import heapq
import itertools

# Agent's intial state
initial_state = {
    # 5x5 grid
    # value 0: clean
    # value 1: dirty
    # the last fifth row (4, x) is dirty
    "grid": (
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (1, 1, 1, 1, 1)
    ),
    # Initial position of the agent at (first row, first column)
    # This is equivalent to (1,1) as per the question since the indexing starts at 0.
    "position": (0, 0)
}

# Actions of the agent
actions = [
    'Suck',
    'Right',
    'Left',
    'Up',
    'Down'
]

def goal_test(state):
    # Get the grid from the state
    grid = state['grid']

    # Check if all rows in the grid are clean
    for row in grid:
        # Check if every square in the current row is equal to 0
        for square in row:
            if square != 0:
                return False  # Return False if any square is dirty

    # If we reach this point, all squares in all rows are clean
    return True  # Return True if all squares are clean

def successor_state(state, action):
    new_grid = list(map(list, state['grid']))
    x, y = state['position']

    if action == 'Suck':
        new_grid[x][y] = 0
    elif action == 'Up' and x < 4:
        x += 1
    elif action == 'Down' and x > 1:
        x -= 1
    elif action == 'Left' and y > 1:
        y -= 1
    elif action == 'Right' and y < 4:
        y += 1

    return {
        "grid": tuple(map(tuple, new_grid)),
        "position": (x, y)
    }

def cost_function(current_state):
    # Get the current state of the grid
    grid = current_state['grid']

    num_dirty = 0

    # Iterate through each row in the grid
    for row in grid:
        # Sum up all the dirty squares in the current row
        for square in row:
            num_dirty += square  # Add the value of the square (1 if dirty, 0 if clean)

    # Calculate the total cost based on the number of dirty squares
    total_cost = 1 + 2 * num_dirty
    
    return total_cost  # Return the calculated cost

def state_to_tuple(state):
    return (state['position'], state['grid'])

def calc_dirty_squares(state):
    dirty_squares = []
    x, y = state['position']

    # Loop through each row and column in the 5x5 grid
    for i in range(5):
        for j in range(5):
            # Check if the current square is dirty
            if state['grid'][i][j] == 1:
                dirty_squares.append((i, j ))

    return dirty_squares

def calc_min_distance(state, dirty_squares):
    x, y = state['position']

    # Calculating minimum distance
    min_distance_to_dirty_square = None

    # Loop through each dirty square
    for d in dirty_squares:
        a, b = d

        # Calculate the Manhattan distance from the agent's position to the dirty square
        distance = abs(x - a) + abs(y - b)

        # Update the minimum distance if it's the first distance calculated
        # or if the current distance is smaller than the previously recorded minimum
        if min_distance_to_dirty_square is None or distance < min_distance_to_dirty_square:
            min_distance_to_dirty_square = distance

    return min_distance_to_dirty_square

# Admissible Heuristic Fucntion
def h1(state):
    dirty_sqrs = calc_dirty_squares(state)

    if not dirty_sqrs:
        return 0

    min_dist_to_dirty_sqrs = calc_min_distance(state, dirty_sqrs)

    # h1 = d + 2 * w(S) - 1
    return min_dist_to_dirty_sqrs + 2 * len(dirty_sqrs) - 1

# Heuristic Function h2 that dominates h1
def h2(state):
    dirty_sqrs = calc_dirty_squares(state)

    if not dirty_sqrs:
        return 0

    min_dist_to_dirty_sqrs = calc_min_distance(state, dirty_sqrs)

    num_dirty_sqrs = len(dirty_sqrs)
    # Penalty associated with squares left dirty after each step in addition to action of moving and cleaning.
    # penalty = d * 2 * w(S) + 2 * w(S) * ( w(S) - 1 )
    penalty = 2 * num_dirty_sqrs * min_dist_to_dirty_sqrs + 2 * num_dirty_sqrs * (num_dirty_sqrs - 1)

    # h2 = h1 + penalty
    return h1(state) + penalty

def a_star(initial_state, heuristic):
    counter = itertools.count()

    open_set = []

    g_value = 0
    h_value = heuristic(initial_state)
    f_value = g_value + h_value

    heapq.heappush(
        open_set,
        (
            f_value,
            next(counter),
            initial_state,
            [], # array of the actions
            g_value,
            h_value,
            f_value
        )
    )

    explored_nodes = set()
    number_of_expanded_nodes = 0
    node_index = 0

    while open_set:
        _, _, state, path, g_value, h_value, f_value = heapq.heappop(open_set)

        print(f"Node {node_index}=> \nState = {state}, \nactions = {path}, \ng(n) = {g_value}, \nh(n) = {h_value}, \nf(n) = {f_value}\n")
        node_index += 1

        if goal_test(state):
            print("########################################################################")
            print(f"Number of nodes expanded: {number_of_expanded_nodes}")

            print("########################################################################")
            print("Sequence of Actions on the Optimal Path:", path)

            return path

        state_tuple = state_to_tuple(state)
        if state_tuple not in explored_nodes:
            explored_nodes.add(state_tuple)
            number_of_expanded_nodes += 1

            for action in actions:
                next_state = successor_state(state, action)
                next_state_tuple = state_to_tuple(next_state)

                if next_state_tuple not in explored_nodes:
                    num_of_dirty_sqrs = len(calc_dirty_squares(next_state))

                    # g(n) = prev g(n) + (1 + 2 * remaining dirty)
                    new_g_value = g_value + (1 + 2 * num_of_dirty_sqrs)
                    # new h(n) value
                    new_h_value = heuristic(next_state)
                    # f(n) = g(n) + h(n)
                    new_f_value = new_g_value + new_h_value

                    heapq.heappush(
                        open_set,
                        (
                            new_f_value,
                            next(counter),
                            next_state,
                            path + [action],
                            new_g_value,
                            new_h_value,
                            new_f_value
                        )
                    )

    return None

def main():
    while True:
        option = input("\nChoose a heuristic (h1 or h2) or type 'exit' to quit: ").strip()

        if option == "h1":
            print("Running A* with h1 (Admissible Heuristic):")
            a_star(initial_state, h1)
        elif option == "h2":
            print("Running A* with h2 (Dominating Heuristic):")
            a_star(initial_state, h2)
        elif option.lower() == "exit":
            print("Exiting the program.")
            # Exit the loop and end the program
            break
        else:
            print("\nInvalid option. Please use 'h1', 'h2', or 'exit'.\n")

main()