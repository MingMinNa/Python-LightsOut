import pytest

from lightsout import Board, Position, Solver, UnsolvablePuzzle


def apply_solution(board: Board, solution: tuple[Position]) -> Board:
    result = board.copy()
    for pos in solution:
        result.press(pos.row, pos.col)
    return result


class TestConstruction:

    def test_accepts_board_instance(self):
        Solver(Board(3))  # should not raise

    @pytest.mark.parametrize("bad_board", ["not a board", 123, None, [1, 2], 3.0])
    def test_non_board_input_raises_type_error(self, bad_board):
        with pytest.raises(TypeError, match="must be an instance of Board"):
            Solver(bad_board)


class TestBasics:

    def test_all_off_board_has_empty_solution(self):
        board = Board(3)
        solver = Solver(board)
        assert solver.solve() == ()

    def test_solver_does_not_mutate_input_board(self):
        board = Board(3)
        board.press(1, 1)
        original = board.get_grid().copy()

        solver = Solver(board)
        solver.solve()

        assert board.get_grid() == original

    def test_single_press_is_self_solvable(self):
        board = Board(3)
        board.press(1, 1)

        solver = Solver(board)
        solution = solver.solve()

        # applying the found solution must clear the board
        solved_board = apply_solution(board, solution)
        assert solved_board.is_all_off()

    def test_solution_entries_are_positions(self):
        board = Board(2)
        board.press(0, 0)
        solver = Solver(board)
        solution = solver.solve()
        assert all(isinstance(p, Position) for p in solution)


class TestIsSolvable:

    def test_all_off_board_is_solvable(self):
        assert Solver(Board(4)).is_solvable()

    @pytest.mark.parametrize("length", [2, 3, 4, 5, 6])
    def test_boards_reachable_by_pressing_buttons_are_solvable(self, length):
        board = Board(length)
        board.press(0, 0)
        board.press(length - 1, length - 1)
        assert Solver(board).is_solvable()

    def test_is_solvable_does_not_mutate_board(self):
        board = Board(3)
        board.press(0, 1)
        original = board.get_grid().copy()
        Solver(board).is_solvable()
        assert board.get_grid() == original


class TestRoundTrip:

    @pytest.mark.parametrize("length", [2, 3, 4, 5])
    def test_solve_then_apply_clears_board(self, length):
        # build a scrambled but definitely-solvable board by pressing buttons
        board = Board(length)
        for r in range(length):
            for c in range(length):
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
        return Board(length, grid)

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