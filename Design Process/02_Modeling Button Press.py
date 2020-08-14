"""
Now that we have a way to represent a Lights Out board, we need to manage how to simulate button presses.

When a button is pressed on a Lights Out board, the light on the button pressed and the adjacent buttons toggle. Since
we are using binary representation of the board, we can leverage bitwise operators to toggle. We'll specifically use
the XOR operator, ^, which when paired with an appropriate mask can perform the task we want.
"""

print(f'{bin(7)} XOR {bin(3)} == {bin(7 ^ 3)}')
print()

"""
To leverage XOR, we're going to need a series of masks to represent our button presses. Determining the central button 
pressed is pretty simple. We'll start at 0, to represent the top left button, and move to 24, to represent the last
button.

First, let's bring back our print_board function.
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


"""
Now, let's iterate over all the central presses of our button. By taking 1 and shifting the bit to the left the
through 0-24, we'll get each button pressed.

We'll only print the Button 7 as a representation.
"""

print('Lighting up Button 7.')
for i in range(25):
    if i == 7:  # We are using 7 here, because the 8th bit is shifted 7 to the left of the 1st.
        print_board(1 << i)
print()

"""
Toggling the buttons to the left and right of the button pressed, at first, appears simple. We'll just add another bit
to the left and right of the one pressed.
"""

print('Lighting up Button 7 & buttons to left & right.')
for i in range(25):
    if i == 7:
        board = 0
        board += 1 << i
        board += 1 << i + 1  # Light to the right
        board += 1 << i - 1  # Light to the left

        print_board(board)
print()

"""
But now we run into a problem. What if we press one of the edge buttons? Say, Button 5.
"""

print('Lighting up Button 5 & buttons to left & right.')
for i in range(25):
    if i == 5:
        board = 0
        board += 1 << i
        board += 1 << i + 1
        board += 1 << i - 1

        print_board(board)
print()

"""
Button 4, which is on the far right of the 1st row, lights up as well. That's not supposed to happen. We need a way
to determine if an edge button is being pressed, and if so, to not toggle an incorrect light.

Here, we can use the modulo operator to determine if a button is on the edge, and to disregard a light if appropriate.
"""

print('Lighting up the 6th button correctly.')
for i in range(25):
    if i == 5:
        board = 0
        board += 1 << i
        if (i + 1) % 5 != 0:  # Detect if on the right edge
            board += 1 << i + 1
        if i % 5 != 0:  # Detect if on the left edge
            board += 1 << i - 1

        print_board(board)
print()

"""
Now that we have left and right sorted out, we need work on the lights above and below.

Similar to left & right, above and below can be managed by shifting new bits 5 places, instead of 1. This would give us
the pattern we are looking for.
"""

print('Lighting up Button 7, with above, below, and both sides.')
for i in range(25):
    if i == 7:
        board = 0
        board += 1 << i
        if (i + 1) % 5 != 0:
            board += 1 << i + 1
        if i % 5 != 0:
            board += 1 << i - 1
        board += 1 << i + 5  # Light above
        board += 1 << i - 5  # Light below

        print_board(board)
print()

"""
We know we'll run into issues on the top and bottom edges, because of our experience with the left & right. Let's
go ahead and solve those issues now.
"""

print('Lighting up Button 2 correctly.')
for i in range(25):
    if i == 2:
        board = 0
        board += 1 << i
        if (i + 1) % 5 != 0:
            board += 1 << i + 1
        if i % 5 != 0:
            board += 1 << i - 1
        if i + 5 <= 24:  # Detect if on bottom row.
            board += 1 << i + 5
        if i - 5 > 0:  # Detect if on top row.
            board += 1 << i - 5

        print_board(board)
print()

"""
With all of that handled, we can populate a full list of all available masked for any button press.
"""

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

mask_to_print = 16
print(f'Printing mask for Button {mask_to_print}.')
print_board(masks[mask_to_print])
print()

"""
Finally, now that we have a mask we can use this with the XOR operator to simulate a button pressed.
"""

board_to_print = 33077713
print(f'Representation of {board_to_print}')
print_board(board_to_print)
print(f'Pressing button {mask_to_print}')
print(f'Board after button press.')
print_board(board_to_print ^ masks[mask_to_print])