"""
While the previous job of building out solutions was running, I realized that we were doing everything backwards.

In the previous attempt, we were taking every start, then doing a breadth first search until we traversed to the
zero state, the solved solution. However, a more efficient approach would be to start with the zero state and build
out the state tree from there. This will allow us to build a path to all possible solvable states with one pass
of the algorithm.

Let's start with bringing in the functions and variables we need from the previous steps.
"""

from collections import deque
import json


def print_board(board):
    """
    Print a representation of a Lights Out board based on the given board number.
    :param board: Board to be printed.
    :return:
    """
    for i in range(25):
        mask = 1 << i

        if board & mask > 0:
            light = 'X'
        else:
            light = 'O'

        print(f'{light} ', end='')

        if (i + 1) % 5 == 0:
            print()


masks = []

for i in range(25):
    board = 0
    board += 1 << i
    if (i + 1) % 5 != 0:
        board += 1 << i + 1
    if i % 5 != 0:
        board += 1 << i - 1
    if i + 5 <= 24:
        board += 1 << i + 5
    if i - 5 > 0:
        board += 1 << i - 5

    masks.append(board)

"""
Let's start with the 0 state.
"""

start_state = 0

"""
Now, let's do our breadth first search starting with zero, and going out until the queue is finally empty.

But, let's add just a little bit more functionality. Let's also store what button to press to get to the new state.
By doing so, we will know what is the next state we need to get to, and what button will get us there.
"""

state_lookup = {start_state: {'next_state': None, 'button': None}}

queue = deque()
queue.append(start_state)

state_count = 0

print('Generating Lookup')
while queue:
    state_count += 1
    if state_count % 100000 == 0:
        print(f'\rProcessing State {state_count:,}', end='')
    current_state = queue.popleft()
    for button, mask in enumerate(masks):
        new_state = current_state ^ mask

        if new_state in state_lookup.keys():
            continue

        state_lookup[new_state] = {'next_state': current_state, 'button': button}
        queue.append(new_state)
print()

print(f'Final states length: {len(state_lookup.keys())}')

"""
Finishing building out the dataset, there's only 16,777,216 total states in the list, out of 33,554,432 possible
states. Half of the states possible don't have parents that lead to the solution state. This means that half of all
possible board setups are actually unsolvable.

On such unsolvable state is board 25620444.

O O X X X 
X O X X O 
O O X O O 
O X X X O 
O X O O O 

The minimum unsolvable state is actually board 2.

O X O O O 
O O O O O 
O O O O O 
O O O O O 
O O O O O 

All boards that would derive from this board are actually unsolvable, this just so happens to be exactly half of all
the possible boards.

Now that we have all the possible solvable states, let's determine how to use that dataset to solve any solvable board.
We'll use board 20448899 as our example board.

X X O O O 
O O X O X 
X O O O O 
O O O O X 
X X O O X 
"""

state = 20448899
button = None

steps = []

while state is not None:
    steps.append((state, button))

    new_state = state_lookup[state]['next_state']
    button = state_lookup[state]['button']

    state = new_state

for i, step in enumerate(steps):
    print(f'Step {i}. Button {step[1]}')
    print_board(step[0])
    print()

"""
Now that we generated all possible solvable states, and what step leads the shortest path to zero, let's save our 
newly created dataset for future lookups.
"""

with open('../data/solvable_states.json', 'w') as file:
    json.dump(state_lookup, file)

"""
All that's left is to create a UI to drive our new tool.
"""