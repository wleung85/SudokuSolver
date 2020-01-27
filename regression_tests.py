import unittest
from sudoku_solver import Puzzle, Square

PUZ_WIDTH = 9
PUZ_HEIGHT = 9
SAMPLE_INPUT = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
                [2, 3, 4, 5, 6, 7, 8, 9, 1],
                [3, 4, 5, 6, 7, 8, 9, 1, 2],
                [4, 5, 6, 7, 8, 9, 1, 2, 3],
                [5, 6, 7, 8, 9, 1, 2, 3, 4],
                [6, 7, 8, 9, 1, 2, 3, 4, 5],
                [7, 8, 9, 1, 2, 3, 4, 5, 6],
                [8, 9, 1, 2, 3, 4, 5, 6, 7],
                [9, 1, 2, 3, 4, 5, 6, 7, 8]]


class TestSudokuSolver(unittest.TestCase):
    # Helper function to create a puzzle using SAMPLE_INPUT
    @staticmethod
    def create_filled_puzzle():
        return Puzzle(SAMPLE_INPUT)

    # Test creating an empty puzzle
    def test_create_empty_puzzle(self):
        empty_puzzle = Puzzle()
        for row in range(PUZ_HEIGHT):
            for col in range(PUZ_WIDTH):
                self.assertEqual(empty_puzzle.get_square(row, col).value, 0)

    # Test creating filled puzzle
    def test_create_filled_puzzle(self):
        filled_puzzle = self.create_filled_puzzle()
        for row in range(PUZ_HEIGHT):
            for col in range(PUZ_WIDTH):
                self.assertEqual(filled_puzzle.get_square(row, col).value, SAMPLE_INPUT[row][col])

    # Test getting a row from a puzzle
    def test_get_row(self):
        filled_puzzle = self.create_filled_puzzle()
        row_index = 2
        row = filled_puzzle.get_row(row_index)
        for index, square in enumerate(row):
            self.assertEqual(square.value, SAMPLE_INPUT[row_index][index])

    # Test getting a row from a puzzle
    def test_get_col(self):
        filled_puzzle = self.create_filled_puzzle()
        col_index = 4
        col = filled_puzzle.get_col(col_index)
        for index, square in enumerate(col):
            self.assertEqual(square.value, SAMPLE_INPUT[index][col_index])

    # Test getting a subgrid from a Square
    def test_get_subgrid_from_Square(self):
        filled_puzzle = self.create_filled_puzzle()
        square_row_index = 4
        square_col_index = 4
        subgrid = filled_puzzle.get_subgrid(filled_puzzle.get_square(square_row_index,
                                                                     square_col_index))
        index = 0
        starting_row_index = square_row_index // 3 * 3
        starting_col_index = square_col_index // 3 * 3
        for row in range(starting_row_index, starting_row_index + 3):
            for col in range(starting_col_index, starting_col_index + 3):
                self.assertEqual(subgrid[index].value, SAMPLE_INPUT[row][col])
                index += 1

    # Test getting a subgrid from coordinates
    def test_get_subgrid_from_coord(self):
        filled_puzzle = self.create_filled_puzzle()
        square_row_index = 4
        square_col_index = 4
        subgrid = filled_puzzle.get_subgrid(square_row_index, square_col_index)
        index = 0
        starting_row_index = square_row_index // 3 * 3
        starting_col_index = square_col_index // 3 * 3
        for row in range(starting_row_index, starting_row_index + 3):
            for col in range(starting_col_index, starting_col_index + 3):
                self.assertEqual(subgrid[index].value, SAMPLE_INPUT[row][col])
                index += 1

    # Test if a list of Squares is solved
    def test_square_list_is_solved(self):
        # Create a list of values from 1 to 9 for a solved list.
        lst = []
        for value in range(1, 10):
            lst.append(Square(value))
        self.assertTrue(Puzzle.sqlist_is_solved(lst))

        # Replace a Square's value to force the list to not be solved
        lst[0].value = 4
        self.assertFalse(Puzzle.sqlist_is_solved(lst))

        # Make the same Square unsolved to again check for unsolved
        lst[0] = Square()
        self.assertFalse(Puzzle.sqlist_is_solved(lst))

    # Test to see a solved puzzle is solved
    def test_puzzle_is_solved(self):
        unsolved_puzzle = self.create_filled_puzzle()
        self.assertFalse(unsolved_puzzle.is_solved())

        solved_puzzle_input = [[8, 2, 7, 1, 5, 4, 3, 9, 6],
                               [9, 6, 5, 3, 2, 7, 1, 4, 8],
                               [3, 4, 1, 6, 8, 9, 7, 5, 2],
                               [5, 9, 3, 4, 6, 8, 2, 7, 1],
                               [4, 7, 2, 5, 1, 3, 6, 8, 9],
                               [6, 1, 8, 9, 7, 2, 4, 3, 5],
                               [7, 8, 6, 2, 3, 5, 9, 1, 4],
                               [1, 5, 4, 7, 9, 6, 8, 2, 3],
                               [2, 3, 9, 8, 4, 1, 5, 6, 7]]
        solved_puzzle = Puzzle(solved_puzzle_input)
        self.assertTrue(solved_puzzle.is_solved())

    # Test solving easy puzzle
    def test_solve_easy_puzzle(self):
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
        easy_puzzle.solve()
        self.assertTrue(easy_puzzle.is_solved())

    # Test solving medium puzzle
    def test_solve_medium_puzzle(self):
        input_arr = [[3, 0, 0, 0, 0, 8, 7, 4, 0],
                     [8, 0, 0, 3, 0, 0, 0, 2, 6],
                     [0, 0, 0, 4, 0, 0, 0, 0, 3],
                     [0, 0, 0, 0, 0, 0, 9, 3, 7],
                     [0, 1, 0, 0, 0, 0, 0, 8, 0],
                     [7, 6, 4, 0, 0, 0, 0, 0, 0],
                     [6, 0, 0, 0, 0, 4, 0, 0, 0],
                     [4, 8, 0, 0, 0, 7, 0, 0, 5],
                     [0, 7, 9, 8, 0, 0, 0, 0, 2]]
        medium_puzzle = Puzzle(input_arr)
        medium_puzzle.solve()
        self.assertTrue(medium_puzzle.is_solved())

    # Test solving hard puzzle
    def test_solve_hard_puzzle(self):
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
        hard_puzzle.solve()
        self.assertTrue(hard_puzzle.is_solved())

    # Test solving evil puzzle (guessing)
    def test_solve_evil_puzzle(self):
        input_arr = [[0, 3, 0, 0, 0, 5, 0, 0, 0],
                     [4, 0, 0, 6, 0, 0, 7, 1, 3],
                     [6, 0, 0, 0, 0, 0, 0, 9, 0],
                     [7, 0, 0, 0, 2, 0, 0, 0, 0],
                     [0, 1, 0, 4, 6, 9, 0, 8, 0],
                     [0, 0, 0, 0, 7, 0, 0, 0, 6],
                     [0, 8, 0, 0, 0, 0, 0, 0, 2],
                     [2, 4, 9, 0, 0, 6, 0, 0, 5],
                     [0, 0, 0, 9, 0, 0, 0, 6, 0]]
        evil_puzzle = Puzzle(input_arr)
        evil_puzzle.solve()
        self.assertTrue(evil_puzzle.is_solved())


if __name__ == "__main__":
    unittest.main()
