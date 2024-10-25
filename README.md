# A\* Algorithm implementation for a vacuum cleaning agent in a 5x5 grid.

## **Project Overview**
The agent move through the grid by cleaning the dirty squares.

### Heuristic Function
The project uses two heuristic functions (h1 and h2).

### Grid
The grid is a 5x5 matrix. Each cell has 0 (clean) or 1 (dirty) value.

The initial position of agent is (0, 0) (first row, first column).

### Actions

The agent can perform the following actions:
- Right
- Left
- Up
- Down
- Suck


---

## How to Run the Program
- Make sure to have python3 installed.
- Run the A\* implementation using the following command:

   ```bash
   python3 a_star.py
   ```
- It will ask input from the user.

  ```bash
  Choose a heuristic (h1 or h2) or type 'exit' to quit:
  ```
- Type `h1` or `h2` to view the A\* algorithm working.
- Type `exit` to exit from the program.

---
## Sample Output

```bash
Choose a heuristic (h1 or h2) or type 'exit' to quit: h1
Node 0=> 
State = {'grid': ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (1, 1, 1, 1, 1)), 'position': (0, 0)}, 
actions = [], 
g(n) = 0, 
h(n) = 13, 
f(n) = 13

Node 1=> 
State = {'grid': ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (1, 1, 1, 1, 1)), 'position': (1, 0)}, 
actions = ['Up'], 
g(n) = 11, 
h(n) = 12, 
f(n) = 23
...
########################################################################
Number of nodes expanded: 65
########################################################################
Sequence of Actions on the Optimal Path: ['Up', 'Up', 'Up', 'Up', 'Suck', 'Right', 'Suck', 'Right', 'Suck', 'Right', 'Suck', 'Right', 'Suck']

Choose a heuristic (h1 or h2) or type 'exit' to quit: 
```
