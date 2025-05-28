import heapq

MOVES = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

# def generate_goal_state(k):
#     goal = []
#     for i in range(k):
#         row = []
#         for j in range(k):
#             row.append((i*k + j + 1) % (k*k))
#         goal.append(row)
#     return goal

def generate_goal_state(k):
    goal = []
    count = 0
    for i in range(k):
        row = []
        for j in range(k):
            row.append(count)
            count += 1
        goal.append(row)
    return goal

            
            
def is_goal(state, goal_state):
    return state == goal_state

def find_zero(state):
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                return (i, j)

    raise ValueError("There is no zero in the start state")

def copy_state(state):
    return [row[:] for row in state]

def get_neighbours(state, k):
    neighbour = []
    x, y = find_zero(state)

    for move, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y + dy
        if 0<= nx < k and 0<= ny < k:
            new_state = copy_state(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbour.append((move, new_state))
    return neighbour

def serialize(state):
    return tuple(tuple(row) for row in state)

def manhattan_distance(state, goal, k):
    distance = 0
    pos = {}
    for i in range(k):
        for j in range(k):
            pos[goal[i][j]] = (i,j)

    for i in range(k):
        for j in range(k):
            val = state[i][j]
            if val != 0:
                goal_x, goal_y = pos[val]
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def a_star(start_state, goal_state, k):
    heap = []
    visited = set()

    h = manhattan_distance(start_state, goal_state, k)
    heapq.heappush(heap, (h, 0, start_state, []))
    visited.add(serialize(start_state))

    while heap:
        est_total, g, current_state, path = heapq.heappop(heap)

        if current_state == goal_state:
            return path

        for move, neighbor in get_neighbours(current_state, k):
            searlized = serialize(neighbor)
            if searlized not in visited:
                visited.add(searlized)
                cost = g + 1
                heuristic = manhattan_distance(neighbor, goal_state, k)
                heapq.heappush(heap, (cost+heuristic, cost, neighbor, path + [move]))

    return None

k = int(input())
puzzle = []

for _ in range(k * k):
    num = int(input())
    puzzle.append(num)

# Convert flat list into 2D list
start_state = [puzzle[i*k:(i+1)*k] for i in range(k)]


# Generate the goal state dynamically
goal_state = generate_goal_state(k)
print(f"Goal state is {goal_state}")

# Run A*
path = a_star(start_state, goal_state, k)

# Output
if path is not None:
    print(len(path))
    for move in path:
        print(move)
else:
    print("No solution found.")


