import sys

"""
Let's take a look at our options for how we want to interpret the game board as a data structure.

Lights Out is a 5 x 5 square of lights. When a button is pressed, the lights of that button and the 4 adjacent are
switched.

Because the states of the buttons are only on or off, there are only two possible states. We can determine the number
of possible boards by raising the number of possible states of each button to the power of the total number of buttons.
"""

num_boards = 2 ** 25

print(f'Total possible board variations: {num_boards:,}')

"""
Since the board is a 5x5 grid, we have to determine a way to represent this structure in Python.

A simple approach would be to create a nested list structure. This would allow access to the state of each button using 
indexing.
"""

"""
Representing the following board: (Where X is a light on)

X O O O X
O X X X O
O X X X O
X O O O X
X X X X X
"""

list_board = [
    [True, False, False, False, True],
    [False, True, True, True, False],
    [False, True, True, True, False],
    [True, False, False, False, True],
    [True, True, True, True, True]
]

"""
The concern with the above is the size of the data structure, especially when repeated for all possible board
variations.
"""

# Get the size of the outer list
list_size = sys.getsizeof(list_board)

# Get the size of each inner list
for l in list_board:
    list_size += sys.getsizeof(l)

    # Get the size of all booleans in lists
    for b in l:
        list_size += sys.getsizeof(b)

print(f'Single list of lists size = {list_size:,} bytes')

"""
Now, repeating that size over the full possible combinations equals.
"""

print(f'Full list of lists size = {num_boards * list_size:,}')

"""
On my computer at the time of running this, that comes to just under 41.5 GB of data.
"""

"""
The question now is, how can we represent all possible boards in a manageable way?

The answer is using integers. Since there are only two states of each light, we can represent any board by using binary.
With a light on represented by a 1, and a light off represented by a 0. We'll assign each light a spot in a binary
digit based on the below.

00 01 02 03 04
05 06 07 08 09
10 11 12 13 14
15 16 17 18 19
20 21 22 23 24

Using the above, the below board

X O O O X
O X X X O
O X X X O
X O O O X
X X X X X

can be represented by the binary

1111110001011100111010001

or the number 33077713.

Now that we can represent a board with a single integer, let's find out how large populating all boards using integers
would be.
"""

int_size = sys.getsizeof(33077713)

print(f'Single int size = {int_size:,} bytes')
print(f'Full int size = {num_boards * int_size:,}')

"""
On my computer at time of running this, the full size is just under 1 GB.
"""

"""
To be fair, interpreting a board based on just an integer can be difficult. Let's create a quick helper function to 
print out the board represented.
"""


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


board_to_print = 33077713
print(f'Representation of {board_to_print}')
print_board(board_to_print)
