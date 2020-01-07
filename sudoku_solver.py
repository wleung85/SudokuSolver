# This project solves sudoku problems


# This represents one index/square with one value
class Square:
    def __init__(self, value=0, solved=False):
        self.value = value
        self.solved = solved

# This represents the entire puzzle with a 9x9 grid of Squares
class Puzzle:
    def __init__(self, given_values=None):
        # Type check to make sure given values is a 2D array with lengths of 9x9
        if given_values != None:
            if not isinstance(given_values, list):
                return ValueError("Puzzle must be initialized with a 9x9 2D array")
            else:
                if len(given_values) != 9:
                    raise ValueError("Puzzle must be initialized with a 9x9 2D array")
                for i in range(9):
                    if len(given_values[i]) != 9:
                        raise ValueError("Puzzle must be initialized with a 9x9 2D array")
                    for j in range(9):
                        if given_values[i][j] < 0 or given_values[i][j] > 9:
                            raise ValueError("Puzzle must be initialized with values 1-9 or \
                                    value 0 to indicate an empty (unsolved) square")

        # Create grid with empty Squares
        if given_values == None:
            self.grid = []
            for i in range(9):
                row = []
                for j in range(9):
                    row.append(Square())
                self.grid.append(row)
        # TODO: fill grid according to given values, could combine with previous grid creation

    def __str__(self):
        # Method to give a string representation of what the puzzle looks like
        output = ""
        for i in range(9):
            for j in range(9):
                # Replace unsolved boxes with '_'
                value = self.grid[i][j].value
                value = value if (value != 0) else '_'
                output += str(value) + " "

                # Add grid lines to represent 3x3 grids
                if (j + 1) % 3 == 0 and j != 8:
                    output += "| "
            output += '\n'
            # Add grid lines to represent 3x3 grids
            if (i + 1) % 3 == 0 and i != 8:
                output += ("- " * 3 + '+ ') * 2 + "- " * 3 + '\n'
        return output

if __name__ == "__main__":
    # Create an empty puzzle with no squares filled
    empty_puzzle = Puzzle()
    for i in range(9):
        for j in range(9):
            empty_puzzle.grid[i][j].value = j + 1
    print(empty_puzzle)
