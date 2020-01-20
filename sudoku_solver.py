# This project solves sudoku problems
import copy


PUZ_WIDTH = 9
PUZ_HEIGHT = 9


# This represents one index/square with one value
class Square:
    def __init__(self, value=0, x=None, y=None):
        self.possibles = []     # possible values
        self.value = value
        self.x = x
        self.y = y
        
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
        if given_values is not None:
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
                row.append(Square(value=value, x=j, y=i))
            self.grid.append(row)

    # Returns True if Puzzle is solved, else False
    def is_solved(self):
        all_square_lists = self.get_all_sqlists()
        for sqlist in all_square_lists:
            if not self.sqlist_is_solved(sqlist):
                return False

        return True
    
    # Returns True if Puzzle is valid, else False
    def is_valid(self):
        all_square_lists = self.get_all_sqlists()
        for sqlist in all_square_lists:
            if not self.sqlist_is_valid(sqlist):
                return False

        return True

    # Iterates through all rows and columns and subgrids while eliminating
    # possibilities and solving. Returns False if puzzle did not change
    def eval_all_sqlist(self):
        puzzle_changed = False
        all_square_lists = self.get_all_sqlists()
        sqlist_iter = -1        # TODO: debug tracker, remove later
        for sqlist in all_square_lists:
            sqlist_iter += 1
            if self.sqlist_eval_possibles(sqlist):
                puzzle_changed = True
        return puzzle_changed

    # Continuously runs eval_all_sqlist to eliminate possibilities. Will stop
    # if puzzle is solved or puzzle doesn't change after an iteration. Returns
    # true if puzzle is solved, else false
    def solve(self, verbose=False):
        if verbose:
            print(self)

        # Use process of elimination until no more possibilities can be eliminated
        while not self.is_solved() and self.is_valid() and self.eval_all_sqlist():
            if verbose:
                print(self)

        # If still not solved, make a guess and see if that puzzle can be solved
        if not self.is_solved() and self.is_valid():
            solution_found = False
            for unknown_square in self.get_all_unknown_squares():
                for guess in unknown_square.possibles:
                    if verbose:
                        print("**** Making guess ****")
                    puzzle_copy = copy.deepcopy(self)
                    puzzle_copy.grid[unknown_square.y][unknown_square.x].value = guess
                    puzzle_copy.solve(verbose=verbose)
                    if puzzle_copy.is_solved():
                        self.copy_puzzle(puzzle_copy, self)
                        solution_found = True
                        break
                if solution_found:
                    break

        return self.is_solved()

    # Copy values from input puzzle into self
    @staticmethod
    def copy_puzzle(copy_from, copy_to):
        for row in range(PUZ_HEIGHT):
            for col in range(PUZ_WIDTH):
                copy_to.grid[row][col].value = copy_from.grid[row][col].value

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

    @staticmethod
    # Checks if list of squares is valid (no duplicates)
    def sqlist_is_valid(lst):
        valid = True
        if len(lst) != 9:
            valid = False
        else:
            seen = []
            for square in lst:
                # Range check value and add to seen list if unknown
                if square.value < 0 or square.value > 9 or square.value in seen:
                    valid = False
                    break
                elif square.value != 0:
                    seen.append(square.value)
        return valid

    @staticmethod
    # Parses list of squares to find values and eliminates seen values from unknown
    # squares' possible values. If only one possible is left, the square is solved.
    # If no possibles were changed (i.e. no new info) returns false
    def sqlist_eval_possibles(lst):
        possibles_eliminated = False
        if not Puzzle.sqlist_is_solved(lst) and Puzzle.sqlist_is_valid(lst):
            # Append all known values to seen list
            seen = []
            for square in lst:
                if square.value != 0:
                    seen.append(square.value)

            # Remove seen values from unknown squares' list of possible values
            unknown_squares = []
            for square in lst:
                if square.value == 0:
                    for value in seen:
                        try:
                            square.possibles.remove(value)
                            possibles_eliminated = True
                        except ValueError:
                            # Seen value isn't in possibles list
                            pass
                    if len(square.possibles) == 1:
                        square.value = square.possibles[0]
                        seen.append(square.value)
                    else:
                        unknown_squares.append(square)

            # Final pass-through of unknown squares to look for values that only exist
            # in one square's possibles
            for square in unknown_squares:
                # Create list of other squares' possibles
                other_square_possibles = []
                other_squares = unknown_squares.copy()
                other_squares.remove(square)
                for other_square in other_squares:
                    for value in other_square.possibles:
                        if value not in other_square_possibles:
                            other_square_possibles.append(value)

                # If a square's possibles aren't in the other squares' possibles or seen written in another square,
                # then safe to assume that this square value must be that possible
                for value in square.possibles:
                    if value not in other_square_possibles and value not in seen:
                        square.value = value
                        seen.append(value)
                        possibles_eliminated = True
                        unknown_squares.remove(square)
                        break

        return possibles_eliminated

    # Gets Square object using row and column index
    def get_square(self, row, col):
        return self.grid[row][col]

    # Gets 1D list of all squares in grid
    def get_all_squares(self):
        lst = []
        for row in range(PUZ_HEIGHT):
            for col in range(PUZ_WIDTH):
                lst.append(self.get_square(row, col))
        return lst

    # Gets 1D list of all unknown squares in grid and sorts them by number of possibles from lowest to greatest
    def get_all_unknown_squares(self):
        lst = []

        # Get all unknown squares
        for row in range(PUZ_HEIGHT):
            for col in range(PUZ_WIDTH):
                square = self.get_square(row, col)
                if square.value == 0:
                    lst.append(square)

        # Sort list of unknown squares from least number of possibles to greatest
        lst.sort(key=lambda unknown_square: len(unknown_square.possibles))

        return lst

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

    # Returns a list of all combinations of rows, columns, and subgrids
    def get_all_sqlists(self):
        result = []
        for row in range(PUZ_HEIGHT):
            result.append(self.get_row(row))

        for col in range(PUZ_WIDTH):
            result.append(self.get_col(col))

        for row in range(PUZ_HEIGHT // 3):
            for col in range(PUZ_WIDTH // 3):
                result.append(self.get_subgrid(row * 3, col * 3))

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
    print(empty_puzzle)

    # Create a Puzzle with values
    print("-" * 20)
    print("Creating filled puzzle")
    input_arr = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                 [2, 3, 4, 5, 6, 7, 8, 9, 1],
                 [3, 4, 5, 6, 7, 8, 9, 1, 2],
                 [4, 5, 6, 7, 8, 9, 1, 2, 3],
                 [5, 6, 7, 8, 9, 1, 2, 3, 4],
                 [6, 7, 8, 9, 1, 2, 3, 4, 5],
                 [7, 8, 9, 1, 2, 3, 4, 5, 6],
                 [8, 9, 1, 2, 3, 4, 5, 6, 7],
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
    input_arr = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
                 [9, 6, 5, 3, 2, 7, 1, 4, 8],
                 [3, 4, 1, 6, 8, 9, 7, 5, 2],
                 [5, 9, 3, 4, 6, 8, 2, 7, 1],
                 [4, 7, 2, 5, 1, 3, 6, 8, 9],
                 [6, 1, 8, 9, 7, 2, 4, 3, 5],
                 [7, 8, 6, 2, 3, 5, 9, 1, 4],
                 [1, 5, 4, 7, 9, 6, 8, 2, 3],
                 [2, 3, 9, 8, 4, 1, 5, 6, 7]]
    solved_puzzle = Puzzle(input_arr)
    print(solved_puzzle)
    print(solved_puzzle.is_solved())

    print("-" * 20)
    print("Check is valid, is solved, and eliminating possibles from list of squares")
    square_list = [Square(8), Square(0), Square(7),
                   Square(9), Square(6), Square(5),
                   Square(3), Square(4), Square(1)]
    print("List of squares is valid?", Puzzle.sqlist_is_valid(square_list))
    print("List of squares is solved?", Puzzle.sqlist_is_solved(square_list))
    Puzzle.sqlist_eval_possibles(square_list)

    print("-" * 20)
    print("Evaluate solving easy puzzle")
    input_arr = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
                 [6, 8, 0, 0, 7, 0, 0, 9, 0],
                 [1, 9, 0, 0, 0, 4, 5, 0, 0],
                 [8, 2, 0, 1, 0, 0, 0, 4, 0],
                 [0, 0, 4, 6, 0, 2, 9, 0, 0],
                 [0, 5, 0, 0, 0, 3, 0, 2, 8],
                 [0, 0, 9, 3, 0, 0, 0, 7, 4],
                 [0, 4, 0, 0, 5, 0, 0, 3, 6],
                 [7, 0, 3, 0, 1, 8, 0, 0, 0]]
    easy_puzzle = Puzzle(input_arr)
    # print(easy_puzzle)
    # while not easy_puzzle.is_solved():
    #     easy_puzzle.eval_all_sqlist()
    #     print(easy_puzzle)
    easy_puzzle.solve(verbose=True)

    print("-" * 20)
    print("Evaluate solving medium puzzle")
    input_arr = [[3, 0, 0, 0, 0, 8, 7, 4, 0],
                 [8, 0, 0, 3, 0, 0, 0, 2, 6],
                 [0, 0, 0, 4, 0, 0, 0, 0, 3],
                 [0, 0, 0, 0, 0, 0, 9, 3, 7],
                 [0, 1, 0, 0, 0, 0, 0, 8, 0],
                 [7, 6, 4, 0, 0, 0, 0, 0, 0],
                 [6, 0, 0, 0, 0, 4, 0, 0, 0],
                 [4, 8, 0, 0, 0, 7, 0, 0, 5],
                 [0, 7, 9, 8, 0, 0, 0, 0, 2]]
    med_puzzle = Puzzle(input_arr)
    med_puzzle.solve(verbose=True)

    print("-" * 20)
    print("Evaluate solving hard puzzle")
    input_arr = [[0, 3, 0, 0, 0, 5, 0, 0, 0],
                 [4, 0, 0, 6, 0, 0, 7, 1, 3],
                 [6, 0, 0, 0, 0, 0, 0, 9, 0],
                 [7, 0, 0, 0, 2, 0, 0, 0, 0],
                 [0, 1, 0, 4, 6, 9, 0, 8, 0],
                 [0, 0, 0, 0, 7, 0, 0, 0, 6],
                 [0, 8, 0, 0, 0, 0, 0, 0, 2],
                 [2, 4, 9, 0, 0, 6, 0, 0, 5],
                 [0, 0, 0, 9, 0, 0, 0, 6, 0]]
    hard_puzzle = Puzzle(input_arr)
    hard_puzzle.solve(verbose=True)

    print("-" * 20)
    print("Evaluate solving evil puzzle")
    input_arr = [[0, 0, 0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 5, 1, 3, 0, 8, 0, 7],
                 [0, 9, 0, 6, 0, 8, 3, 0, 0],
                 [6, 1, 0, 0, 0, 0, 0, 0, 0],
                 [3, 0, 0, 0, 0, 0, 0, 0, 6],
                 [0, 0, 0, 0, 0, 0, 0, 8, 9],
                 [0, 0, 3, 8, 0, 2, 0, 4, 0],
                 [2, 0, 1, 0, 9, 7, 6, 0, 0],
                 [0, 0, 0, 0, 5, 0, 0, 0, 0]]
    evil_puzzle = Puzzle(input_arr)
    evil_puzzle.solve(verbose=True)
    print(f"Puzzle is valid: {evil_puzzle.is_valid()}")
    print(f"Puzzle is solved: {evil_puzzle.is_solved()}")

    print("Finished run")
