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

    # if action == 'Suck' and x < 5 and y < 5:
    if action == 'Suck':
        new_grid[x][y] = 0
        # new_grid[x-1][y-1] = 0
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

def calc_num_of_dirty_squares_and_min_distance(state):
    # Initially set min-distance to a large (infinity) value.
    min_distance = float('inf')
    num_of_dirty_squares = 0

    x, y = state['position']

    for i in range(5):
        for j in range(5):
            if state['grid'][i][j] == 1:
                num_of_dirty_squares += 1
                distance = abs((i) - x) + abs((j) - y)
                min_distance = min(min_distance, distance)

    return (num_of_dirty_squares, min_distance)

# Admissible Heuristic Fucntion
def h1(state):
    num_dirty_squares, min_distance = calc_num_of_dirty_squares_and_min_distance(state)

    # The min-distance will be infinity if there are no dirty squares.
    # So, we return zero in such case.
    if num_dirty_squares == 0:
        return 0

    # h1 = d + 2 * w(S) - 1
    return min_distance + 2 * num_dirty_squares - 1

# Heuristic Function h2 that dominates h1
def h2(state):
    num_dirty_squares, min_distance = calc_num_of_dirty_squares_and_min_distance(state)

    # The min-distance will be infinity if there are no dirty squares.
    # So, we return zero in such case.
    if num_dirty_squares == 0:
        return 0

    # Penalty associated with squares left dirty after each step in addition to action of moving and cleaning.
    # penalty = d * 2 * w(S) + 2 * w(S) * ( w(S) - 1 )
    penalty = 2 * num_dirty_squares * min_distance + 2 * num_dirty_squares * (num_dirty_squares - 1)

    # h2 = h1 + penalty
    return h1(state) + penalty

def a_star(initial_state, heuristic):
    counter = itertools.count()

    open_set = []

    # Store f(n) initially instead of storing the whole state directly
    heapq.heappush(open_set, (0, next(counter), initial_state, [], 0, 0))
    explored = set()
    num_expanded = 0

    # For tracking f(n) values in the optimal path
    f_values_on_path = []
    # For tracking states in the optimal path including initial state
    states_on_path = [initial_state]
    # For tracking the actions in the optimal path
    actions_on_path = [[]]

    while open_set:
        f, _, state, path, curr_cost, f_value = heapq.heappop(open_set)

        if goal_test(state):
            f_values_on_path.append(f_value)
            states_on_path.append(state)
            actions_on_path.append(path)

            print("Node: state, f(n) values, and actions that leads to the nodes in the optimal path:")
            for i, (fn_value, node_state, actions_taken) in enumerate(zip(f_values_on_path, states_on_path, actions_on_path)):
                print(f"Node: {i + 1}=> \nState = {node_state}, \nactions = {actions_taken}, \nf(n) value = {fn_value}")
                print("\n")

            print("########################################################################")
            print(f"Number of nodes expanded: {num_expanded}")

            print("########################################################################")
            print(f"f(n) value at the final goal state: {f}")

            print("########################################################################")
            print("Sequence of Actions on the Optimal Path:", path)

            return path

        state_tuple = state_to_tuple(state)
        if state_tuple not in explored:
            explored.add(state_tuple)
            num_expanded += 1

            for action in actions:
                next_state = successor_state(state, action)
                next_state_tuple = state_to_tuple(next_state)

                if next_state_tuple not in explored:
                    new_cost = curr_cost + cost_function(next_state)
                    next_f_value = new_cost + heuristic(next_state)

                    heapq.heappush(open_set, (next_f_value, next(counter), next_state, path + [action], new_cost, next_f_value))

                    f_values_on_path.append(next_f_value)
                    states_on_path.append(next_state)
                    actions_on_path.append(path + [action])

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