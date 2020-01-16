# This project solves sudoku problems

PUZ_WIDTH = 9
PUZ_HEIGHT = 9

# This represents one index/square with one value
class Square:
    def __init__(self, value=0):
        self.possibles = []     # possible values
        self.value = value
        
        # Square is already solved and given if initialized with a non-zero/blank
        if value:
            self.solved = True
            self.given = True
        else:
            self.solved = False
            self.given = False

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        # Range check value
        if not isinstance(value, int) or value < 0 or value > 9:
            raise ValueError("Square must have value 1-9 or 0 to indicate no value")
        self._value = value
        if value == 0:
            self.possibles = [i for i in range(1,10)]
        else:
            self.possibles = [value]

    def __str__(self):
        return str(self.value)

# This represents the entire puzzle with a 9x9 grid of Squares
class Puzzle:
    def __init__(self, given_values=None):
        self.solved = False
        self.grid = []
        # Type check to make sure given values is a 2D array with lengths of 9x9
        if given_values != None:
            if not isinstance(given_values, list) or len(given_values) != PUZ_HEIGHT:
                raise ValueError("Puzzle must be initialized with a 9x9 2D array")
            for row in given_values:
                if len(row) != PUZ_HEIGHT:
                    raise ValueError("Puzzle must be initialized with a 9x9 2D array")
        
        # Fill grid with Squares
        for i in range(PUZ_HEIGHT):
            row = []
            for j in range(PUZ_WIDTH):
                value = 0 if given_values is None else given_values[i][j]
                row.append(Square(value))
            self.grid.append(row)

    # Returns True if Puzzle is solved, else False
    def is_solved(self):
        for row in range(PUZ_HEIGHT):
            lst = self.get_row(row)
            if not self.sqlist_is_solved(lst):
                return False

        for col in range(PUZ_WIDTH):
            lst = self.get_col(col)
            if not self.sqlist_is_solved(lst):
                return False

        for row in range(PUZ_HEIGHT // 3):
            for col in range(PUZ_WIDTH // 3):
                lst = self.get_subgrid(row * 3, col * 3)
                if not self.sqlist_is_solved(lst):
                    return False

        return True
            
    
    @staticmethod
    # Checks if list of squares is solved (i.e. contains values 1-9)
    def sqlist_is_solved(lst):
        solved = True
        if len(lst) != 9:
            solved = False
        else:
            for value in range(1, 10):
                value_found = False
                for square in lst:
                    if square.value == value:
                        value_found = True
                        break
                if not value_found:
                    solved = False
                    break

        return solved

    # Gets Square object using row and column index
    def get_square(self, row, col):
        return self.grid[row][col]
    
    # Gets list of Squares from 0-indexed row of grid
    def get_row(self, index):
        return self.grid[index]

    # Gets list of Squares from 0-indexed column of grid
    def get_col(self, index):
        col = []
        for row in range(len(self.grid)):
            col.append(self.grid[row][index])
        return col

    # Gets the 3x3 subgrid at which Square resides
    def get_subgrid(self, *args):
        # If square was used as an argument, iterate through Puzzle to find matching
        # Square. If no matching Square found, raise error
        if len(args) == 1 and isinstance(args[0], Square):
            square = args[0]
            square_found = False
            for row in range(PUZ_HEIGHT):
                for col in range(PUZ_WIDTH):
                    if self.grid[row][col] == square:
                        square_found = True
                        break
                if square_found:
                        break
            if not square_found:
                raise ValueError("Square was not found inside Puzzle")
        # If row and col indices were used, range check
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int):
            row = args[0]
            col = args[1]
            if row < 0 or row > 8 or col < 0 or col > 8:
                raise ValueError("Invalid index was used. Row and col index must be between 0 and 8, inclusive")
        else:
            raise ValueError("Method expects either a single Square argument or a row and column argument")

        # Find first index (top-left square) of subgrid
        row = row // 3 * 3
        col = col // 3 * 3
        result = []
        for row_iter in range(PUZ_HEIGHT // 3):
            for col_iter in range(PUZ_WIDTH // 3):
                result.append(self.grid[row + row_iter][col + col_iter])

        return result

    def __str__(self):
        # Method to give a string representation of what the puzzle looks like
        output = ""
        for i in range(PUZ_HEIGHT):
            for j in range(PUZ_WIDTH):
                # Replace unsolved boxes with '_'
                value = str(self.grid[i][j].value)
                value = value if (value != '0') else '_'
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
    print("-" * 20)
    print("Creating empty puzzle")
    empty_puzzle = Puzzle()
    print (empty_puzzle)

    # Create a Puzzle with values
    print("-" * 20)
    print("Creating filled puzzle")
    input_arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9],\
                 [2, 3, 4 ,5, 6, 7, 8, 9, 1],\
                 [3, 4, 5, 6, 7, 8, 9, 1, 2],\
                 [4, 5, 6, 7, 8, 9, 1, 2, 3],\
                 [5, 6, 7, 8, 9, 1, 2, 3, 4],\
                 [6, 7, 8, 9, 1, 2, 3, 4, 5],\
                 [7, 8, 9, 1, 2, 3, 4, 5, 6],\
                 [8, 9, 1, 2, 3, 4, 5, 6, 7],\
                 [9, 1, 2, 3, 4, 5, 6, 7, 8]]
    filled_puzzle = Puzzle(input_arr)
    print(filled_puzzle)
    
    print("-" * 20)
    print("Getting row 2")
    row = filled_puzzle.get_row(2)
    for val in row:
        print(val)
    print("-" * 20)
    print("Getting column 4")    
    col = filled_puzzle.get_col(4)
    for val in col:
        print(val)

    print("-" * 20)
    print("Printing subgrid from Square")
    subgrid = filled_puzzle.get_subgrid(filled_puzzle.get_square(2, 2))
    for square in subgrid:
        print(square)
    print("-" * 20)
    print("Printing subgrid from coordinates")
    subgrid = filled_puzzle.get_subgrid(2, 2)
    for square in subgrid:
        print(square)

    print("-" * 20)
    print("Check if list of squares is solved")
    lst = []
    for value in range(1, 10):
        lst.append(Square(value))
    print(Puzzle.sqlist_is_solved(lst))
    lst[0].value = 4
    print(Puzzle.sqlist_is_solved(lst))

    print("-" * 20)
    # print("Check if filled puzzle is solved")
    # print(filled_puzzle.is_solved())
    print("Check if solved puzzle is solved")
    input_arr = [[8, 2, 7, 1, 5, 4, 3, 9, 6],\
                 [9, 6, 5, 3, 2, 7, 1, 4, 8],\
                 [3, 4, 1, 6, 8, 9, 7, 5, 2],\
                 [5, 9, 3, 4, 6, 8, 2, 7, 1],\
                 [4, 7, 2, 5, 1, 3, 6, 8, 9],\
                 [6, 1, 8, 9, 7, 2, 4, 3, 5],\
                 [7, 8, 6, 2, 3, 5, 9, 1, 4],\
                 [1, 5, 4, 7, 9, 6, 8, 2, 3],\
                 [2, 3, 9, 8, 4, 1, 5, 6, 7]]
    solved_puzzle = Puzzle(input_arr)
    print(solved_puzzle)
    print(solved_puzzle.is_solved())

    # TODO: solved_puzzle should return solved, getting subgrid seems broken

    print("Finished run")
