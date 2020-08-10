import time
import sys

"""
With the ability to create our masks and every board variation, we can build out a graph connecting all board states
to one another. Essentially, each board state can be a node in our network, and if we can move from one state to
another with a mask, we'll add an edge.

To build out network, we're going to use the Python package, networkx.
"""

import networkx as nx

G = nx.Graph()

"""
Now that we have our graph, we can add all of our nodes. Because we are using a binary representation, this is as
simple as using a range() function to cycle through all possible variations.
"""

print('Creating nodes.')
start_time = time.time()

G.add_nodes_from(range(2**25))  # 2**25 = Total number of variations.

elapsed_time = time.time() - start_time
print(f'Graph created in {elapsed_time:.1f} secs.')

"""
On my computer this graph was built in just over 30 secs. Now, let's populate the edges.
"""

# Generate masks
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

print('Creating edges.')
start_time = time.time()

# Iterating through all boards and creating connections based on masks.
for board in range(2**25):
    edges = []
    for mask in masks:
        edges.append((board, board ^ mask))
    G.add_edges_from(edges)

elapsed_time = time.time() - start_time
print(f'Edges created in {elapsed_time:.1f} secs.')

"""
Uh oh. I got an error trying to create my edges.

    Process finished with exit code 137 (interrupted by signal 9: SIGKILL)

Looks like I ran out of memory trying to populate the edges. While all of the boards will fit in memory with just
under 1 GB, the connections between those nodes are too numerous to handle.

Looks like we have to try something else.
"""