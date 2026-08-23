import pytest

from lightsout import Board, Position, Solver, UnsolvablePuzzle


def apply_solution(board: Board, solution: tuple[Position]) -> Board:
    result = board.copy()
    for pos in solution:
        result.press(pos.row, pos.col)
    return result


class TestConstruction:

    @pytest.mark.parametrize("height,width", [
        (3, 3),  # square
        (2, 5),  # rectangle
    ])
    def test_accepts_board_instance(self, height, width):
        Solver(Board(height, width))  # should not raise

    @pytest.mark.parametrize("bad_board", ["not a board", 123, None, [1, 2], 3.0])
    def test_non_board_input_raises_type_error(self, bad_board):
        with pytest.raises(TypeError, match="must be an instance of Board"):
            Solver(bad_board)


class TestBasics:

    def test_all_off_board_has_empty_solution(self):
        board = Board(3, 3)
        solver = Solver(board)
        assert solver.solve() == ()

    def test_solver_does_not_mutate_input_board(self):
        board = Board(3, 3)
        board.press(1, 1)
        original = board.get_grid().copy()

        solver = Solver(board)
        solver.solve()

        assert board.get_grid() == original

    def test_single_press_is_self_solvable(self):
        board = Board(3, 3)
        board.press(1, 1)

        solver = Solver(board)
        solution = solver.solve()

        # applying the found solution must clear the board
        solved_board = apply_solution(board, solution)
        assert solved_board.is_all_off()

    def test_solution_entries_are_positions(self):
        board = Board(2, 2)
        board.press(0, 0)
        solver = Solver(board)
        solution = solver.solve()
        assert all(isinstance(p, Position) for p in solution)


class TestIsSolvable:

    def test_all_off_board_is_solvable(self):
        assert Solver(Board(4, 4)).is_solvable()

    @pytest.mark.parametrize("height,width", [
        (2, 2), (3, 3), (4, 4), (5, 5), (6, 6),  # square
        (2, 3), (3, 2), (2, 5), (4, 7),          # rectangle
    ])
    def test_boards_reachable_by_pressing_buttons_are_solvable(self, height, width):
        board = Board(height, width)
        board.press(0, 0)
        board.press(height - 1, width - 1)
        assert Solver(board).is_solvable()

    def test_is_solvable_does_not_mutate_board(self):
        board = Board(3, 3)
        board.press(0, 1)
        original = board.get_grid().copy()
        Solver(board).is_solvable()
        assert board.get_grid() == original


class TestRoundTrip:

    @pytest.mark.parametrize("height,width", [
        (2, 2), (3, 3), (4, 4), (5, 5),   # square
        (2, 3), (3, 2), (2, 5), (4, 7),   # rectangular
    ])
    def test_solve_then_apply_clears_board(self, height, width):
        # build a scrambled but definitely-solvable board by pressing buttons
        board = Board(height, width)
        for r in range(height):
            for c in range(width):
                if (r + c) % 2 == 0:
                    board.press(r, c)

        solver = Solver(board)
        solution = solver.solve()
        solved_board = apply_solution(board, solution)
        assert solved_board.is_all_off()


class TestUnsolvableRaisesException:

    def _unsolvable_board(self, length: int = 4) -> Board:
        # a single light on a 4x4 grid is a known unsolvable configuration
        size = length * length
        grid = [False] * size
        grid[0] = True
        return Board(length, length, grid)

    def test_solve_raises_unsolvable_puzzle(self):
        board = self._unsolvable_board()
        solver = Solver(board)
        with pytest.raises(UnsolvablePuzzle):
            solver.solve()

    def test_is_solvable_returns_false_for_unsolvable_board(self):
        board = self._unsolvable_board()
        solver = Solver(board)
        assert solver.is_solvable() is False

    def test_solve_does_not_mutate_board_even_on_failure(self):
        board = self._unsolvable_board()
        original = board.get_grid().copy()
        solver = Solver(board)
        with pytest.raises(UnsolvablePuzzle):
            solver.solve()
        assert board.get_grid() == original