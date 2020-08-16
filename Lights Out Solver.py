import tkinter as tk
import json
from collections import deque
import os


class LightsOutSolver(tk.Tk):
    """
    Application designed to solve the 1995 Tiger Electronics game, Lights Out.
    """

    def __init__(self):
        """
        Generate Lights Out Window
        """
        super().__init__()

        self.BOARD_SIZE = 5

        self.title('Lights Out Solver')

        self.board_vars = [[tk.IntVar() for _ in range(5)] for _ in range(5)]
        self.button_lookup = self.get_button_lookup()

        self.solutions = None

        self.main_frame = None
        self.control_frame = None
        self.new_button = None
        self.solve_button = None
        self.load_button = None
        self.board_frame = None
        self.check_buttons = None
        self.text_frame = None
        self.solution_text = None

        self.create_main_view()

    def create_main_view(self):
        """
        Creates the main window for application
        :return:
        """
        self.main_frame = tk.Frame(
            master=self
        )
        self.main_frame.pack()

        self.control_frame = tk.Frame(
            master=self.main_frame
        )
        self.control_frame.grid(row=0, column=0)

        self.new_button = tk.Button(
            master=self.control_frame,
            command=self.new,
            text='New',
            width=10
        )

        self.solve_button = tk.Button(
            master=self.control_frame,
            command=self.solve,
            text='Solve',
            width=10
        )

        self.load_button = tk.Button(
            master=self.control_frame,
            command=self.load_solutions,
            text='Load Solutions',
        )
        self.load_button.grid(row=0, column=0, columnspan=2)

        self.board_frame = tk.Frame(
            master=self.main_frame
        )
        self.board_frame.grid(row=1, column=0)

        # Place top labels
        for i in range(5):
            tk.Label(
                master=self.board_frame,
                text=i + 1
            ).grid(row=0, column=i + 1)

        # Place side Labels
        for i in range(5):
            tk.Label(
                master=self.board_frame,
                text='ABCDE'[i]
            ).grid(row=i + 1, column=0)

        # Place right padding
        for i in range(6):
            tk.Label(
                master=self.board_frame,
                text=' '
            ).grid(row=i, column=6)

        self.check_buttons = [[] for _ in range(self.BOARD_SIZE)]

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                chk_btn = tk.Checkbutton(
                    master=self.board_frame,
                    variable=self.board_vars[i][j],
                    state=tk.DISABLED
                )
                chk_btn.grid(row=i + 1, column=j + 1)

                self.check_buttons[i].append(chk_btn)

        self.text_frame = tk.Frame(
            master=self.main_frame
        )
        self.text_frame.grid(row=2, column=0)

        self.solution_text = tk.Text(
            master=self.text_frame,
            width=30,
            height=10,
            state=tk.DISABLED
        )
        self.solution_text.grid(row=0, column=0)

    def load_solutions(self):
        """
        Load the predetermined Lights Out solutions.
        :return:
        """
        # Check if file exists
        if not os.path.exists('data'):
            os.mkdir('data')

        if not os.path.exists('./data/solvable_states.json'):
            self.write_to_text('Generating Lights Out \nsolutions.\nWill take a while...')
            self.update()
            self.generate_solutions()

        with open('./data/solvable_states.json') as file:
            self.write_to_text('Loading Lights Out solutions.\nPlease be patient.')
            self.update()
            self.solutions = json.load(file)

        self.load_button.grid_forget()
        self.new_button.grid(row=0, column=0, padx=5, pady=5)
        self.solve_button.grid(row=0, column=1, padx=5, pady=5)
        self.new()
        self.update()

    def generate_solutions(self):
        """
        Generate the solutions dataset if doesn't exist.
        :return:
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

        start_state = 0
        state_lookup = {start_state: {'next_state': None, 'button': None}}

        queue = deque()
        queue.append(start_state)

        gen_msg = 'Generating Lights Out \nsolutions.\nWill take a while...\n\n'

        state_count = 0
        while queue:
            state_count += 1
            if state_count % 10000 == 0:

                self.write_to_text(gen_msg + f'Solutions generated\n{state_count:,}')
                self.update()
            current_state = queue.popleft()
            for button, mask in enumerate(masks):
                new_state = current_state ^ mask

                if new_state in state_lookup.keys():
                    continue

                state_lookup[new_state] = {'next_state': current_state, 'button': button}
                queue.append(new_state)

        with open('./data/solvable_states.json', 'w') as file:
            self.write_to_text(gen_msg + 'Writing solutions to disk.')
            self.update()
            json.dump(state_lookup, file)

    def new(self):
        """
        Reset the Lights Out Board and open Checkboxes for selection.
        :return:
        """
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.board_vars[i][j].set(0)
                self.check_buttons[i][j].config(state=tk.NORMAL)

        self.write_to_text('Check boxes for lights on.\n\nThen press "Solve" to solve \nthe board.')

    def solve(self):
        """
        Determine the solution and print results to the textbox.
        :return:
        """
        board = str(self.get_board())

        # Test if solvable.
        if board not in self.solutions.keys():
            self.write_to_text(f'Unsolvable board.\nBoard: {board}')
            return

        message_builder = ''

        state = board
        button = None

        steps = []
        while state != 'None':
            steps.append((state, button))

            new_state = self.solutions[state]['next_state']
            button = self.solutions[state]['button']

            state = str(new_state)

        for i, step in enumerate(steps):
            if i == 0:
                message_builder += 'Starting State\n'
            else:
                message_builder += f'Step {i}. Button {self.button_lookup[step[1]]}\n'
            message_builder += self.board_string(step[0])

        self.write_to_text(message_builder)

    def get_board(self):
        """
        Return the integer value of the board in the application checkboxes.
        :return: Integer of board to solve.
        """
        board_builder = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                board_builder.append(self.board_vars[i][j].get())
                self.check_buttons[i][j].config(state=tk.DISABLED)

        board = 0
        for i in range(len(board_builder)):
            board += board_builder[i] << i

        return board

    def write_to_text(self, message):
        """
        Clear the application text box and print message.
        :param message: Message to print.
        :return:
        """
        self.solution_text.config(state=tk.NORMAL)
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.insert(tk.END, message)
        self.solution_text.config(state=tk.DISABLED)

    def board_string(self, board):
        """
        Return a string representation of the given board.
        :param board: Board to represent.
        :return: String representation with "X" as light on and "O" as off.
        """
        board = int(board)

        board_builder = ''

        for i in range(self.BOARD_SIZE * self.BOARD_SIZE):
            mask = 1 << i

            if board & mask > 0:
                board_builder += 'X '
            else:
                board_builder += 'O '

            if (i + 1) % 5 == 0:
                board_builder += '\n'

        board_builder += '\n'

        return board_builder

    def get_button_lookup(self):
        """
        Generate the button_lookup variable to translate buttons based on grid.
        :return:
        """
        button_lookup = {}
        for i in range(self.BOARD_SIZE * self.BOARD_SIZE):
            grid_loc = f'{"ABCDE"[i // 5]}{(i % 5)+1}'

            button_lookup[i] = grid_loc

        return button_lookup


if __name__ == '__main__':
    solver = LightsOutSolver()

    solver.mainloop()
