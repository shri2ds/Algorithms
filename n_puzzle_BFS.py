from collections import deque
from html5lib import serialize

MOVES = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

def generate_goal_state(k):
    goal = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append((i * k + j + 1) % (k * k))
        goal.append(row)
    return goal

def is_goal(state, goal_state):
    return state == goal_state

def find_zero(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return (i, j)
    raise ValueError("Zero tile not found in the given puzzle state.")

def copy_state(state):
    return [row[:] for row in state]

def get_neighbors(state, k):
    neighbors = []
    x, y = find_zero(state)

    for move, (dx, dy) in MOVES.items():
        nx, ny = x + dx, y  + dy
        if 0 <= nx < k and 0 <= ny < k:
            new_state = copy_state(state)
            new_state[x][y], new_state[nx][ny] = new_state[x][y], new_state[nx][ny]
            neighbors.append((new_state, move))
    return neighbors

def serialize(state):
    return tuple(tuple(row) for row in state)

def bfs(start_state, goal_state, k):
    queue = deque()
    visited = set()
    queue.append((start_state, []))
    visited.add(serialize(start_state))

    while queue:
        current_state, path = queue.popleft()

        if is_goal(start_state, goal_state):
            return path

        for neighbour, move in get_neighbors(current_state, k):
            serialized = serialize(neighbour)
            if serialized not in visited:
                visited.add(serialized)
                queue.append((neighbour, path + [move]))

    return None

k = int(input())
puzzle = []

for _ in range(k * k):
    num = int(input())
    puzzle.append(num)

start_state = [puzzle[i*k:(i+1)*k] for i in range(k)]
# print(f"Sample Input is {start_state}")

goal_state = generate_goal_state(k)
print(f"Goal State is {goal_state}")

path = bfs(start_state, goal_state, k)
if path is not None:
    print(len(path))
    for move in path:
        print(move)
else:
    print("No solution found")




# sample_queue = deque([0,1,1,2,1,1])
# _ , test1 = sample_queue.popleft()
# k = 3
# goal = []
# for i in range(k):
#     row = []
#     for j in range(k):
#         row.append((i * k + j + 1) % (k * k))
#     goal.append(row)
#     print(goal)




