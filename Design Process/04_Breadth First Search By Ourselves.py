"""
Let's start by bringing in some work from the previous steps to setup our environment.
"""

from collections import deque


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
The plan for using networkx was to efficiently find the shortest distance between any two board states. This way we
could find the shortest distance between our current state and done, the zero state.

Unfortunately, our game was too much for networkx to hold it all in memory. Rather than trying to find a way to
store the full network, let's just do a shortest distance algorithm ourselves, the Breadth First Search.

The idea of a breadth first search is to search all connections in a network one layer at time. We can generate what
that next layer will look like by applying all of our masks to any given state.

This will be our starting state to work with.

X X O X X
X O O O X
O O O O O
O O O O O
O O O O O
"""
start_state = 0b1000111011

new_states = [m ^ start_state for m in masks]

print_board(start_state)
print()
print_board(new_states[0])
print()

"""
We have a starting state and all the states that come after. This can be defined as a parent-child relationship.
With our starting state as the parent, all of the possible new states would be the child. We can store these
relationships in a dictionary for faster lookup.

We'll use the child state as our key, and store the parent.
"""

state_lookup = {}

for m in masks:
    parent = start_state
    child = start_state ^ m
    state_lookup[child] = parent

"""
Now that we can build the relationship to the next layer down in a network, let's take it one step deeper. To do this,
we're going to build a queue.

Using the Python deque object in collections, we will be able to build a first in first out method of diving down a
layer at a time.

Basically, from our starting point, we will add all next states to our list to process. After we finish the initial
state, we'll do the same thing for the first of the 25 new states. That new state will become our new starting point
and we will add the next 25 new states to the back of the queue. By adding new states in on the right, and pulling
what we are working on from the left, we are guaranteed to pull in all of our new states from the initial start before
we process the second layer of states.

We have to add one bit of logic into this to make it work correctly. It is possible to already visit a state we've been
to before. Imagine pressing the same button twice in a row. We've already been there, and don't need to add it to our
processing queue. So, before adding a state to the queue, we make sure we have not already check it.

Finally, when we reach state 0, where all the lights are off, we can break out of our search.
"""
######### Leveraging the Queue for next layer

queue = deque()
state_lookup = {start_state: None}

queue.append(start_state)

while queue:
    state = queue.popleft()

    for m in masks:
        new_state = state ^ m

        if new_state not in (state_lookup.keys()):
            state_lookup[new_state] = state
            queue.append(new_state)

    if 0 in state_lookup.values():
        break

"""
We have generated all the data we need to build our shortest path from our starting state to the 0 state, or having
the game completed. What we need to do is traverse through our parent-child relationships and build out the appropriate
steps.

We'll start with the 0 state, our goal, and get the parent state, basically what state got us to this point, and add
it to our steps list. Then we'll choose the parent up from there, and so on until we get to our starting state, which
has a parent of None.

Finally, we have a list of all steps back to our parent state. Now we just have to reverse our list, and we have a
path to solution!
"""

start_state = 0
steps = []

while True:
    steps.append(start_state)

    if state_lookup[start_state]:
        start_state = state_lookup[start_state]

    else:
        break

steps.reverse()

for i, step in enumerate(steps):
    print(f'Step {i}')
    print_board(step)
    print()

"""
Now that we have this, we can repeat this process for every possible state and get a full list of solutions! We'll just
let that run...
"""

"""
Nope, just kidding, that's a terribly inefficient way of doing this. Let's take a look at a better way in the next
section.
"""