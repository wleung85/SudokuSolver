# This project solves sudoku problems


# This represents one index/square with one value
class Square:
    def __init__(self, value=0, solved=False):
        self.possibles = []     # possible values
        self.value = value
        self.solved = solved

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        # Range check value
        if value < 0 or value > 9:
            raise ValueError("Square must have value 1-9 or 0 to indicate no value")
        self._value = value
        if value == 0:
            self.possibles = [i for i in range(1,10)]
        else:
            self.possibles = [value]

# This represents the entire puzzle with a 9x9 grid of Squares
class Puzzle:
    def __init__(self, given_values=None):
        self.grid = []
        # Type check to make sure given values is a 2D array with lengths of 9x9
        if given_values != None:
            if not isinstance(given_values, list) or len(given_values) != 9:
                raise ValueError("Puzzle must be initialized with a 9x9 2D sarray")
            for row in given_values:
                if len(row) != 9:
                    raise ValueError("Puzzle must be initialized with a 9x9 2D sarray")
        
        # Fill grid with Squares
        for i in range(9):
            row = []
            for j in range(9):
                value = 0 if given_values is None else given_values[i][j]
                row.append(Square(value))
            self.grid.append(row)

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
    print("Creating empty puzzle")
    empty_puzzle = Puzzle()
    print (empty_puzzle)

    # Create a Puzzle with values
    print("Creating filled puzzle")
    input_arr = []
    for i in range(9):
        row = [i for i in range(1, 10)]
        input_arr.append(row)
    filled_puzzle = Puzzle(input_arr)
    print(filled_puzzle)
