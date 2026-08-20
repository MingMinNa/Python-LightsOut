import pytest

from lightsout import Board, InvalidGrid, Position


class TestConstruction:

    def test_default_grid_is_all_off(self):
        board = Board(3)
        assert board.get_length() == 3
        assert board.get_grid() == [False] * 9
        assert board.is_all_off()

    def test_explicit_grid_is_used(self):
        grid = [True, False, False, True]
        board = Board(2, grid)
        assert board.get_grid() == grid

    def test_grid_is_deep_copied_on_construction(self):
        grid = [True, False, False, True]
        board = Board(2, grid)
        grid[0] = False
        # mutating the original list must not affect the board
        assert board.get_grid() == [True, False, False, True]

    @pytest.mark.parametrize("length", [1, 2, 5, 10])
    def test_various_valid_lengths(self, length):
        board = Board(length)
        assert board.get_length() == length
        assert len(board.get_grid()) == length * length


class TestConstructionErrors:

    @pytest.mark.parametrize("bad_length", ["3", None, [3], (3,)])
    def test_non_int_length_with_default_grid_raises_type_error(self, bad_length):
        with pytest.raises(TypeError, match="length must be integer"):
            Board(bad_length)

    def test_bool_length_raises_type_error(self):
        # bool is a subclass of int, but `type(length) is not int` correctly.
        with pytest.raises(TypeError, match="length must be integer"):
            Board(True)

    def test_non_int_length_with_explicit_grid_raises_type_error_with_message(self):
        # check_length() runs first and raises.
        with pytest.raises(TypeError, match="length must be integer"):
            Board("2", [True, False, True, False])

    @pytest.mark.parametrize("bad_length", [0, -1, -100])
    def test_non_positive_length_raises_value_error(self, bad_length):
        with pytest.raises(ValueError, match="length must be positive"):
            Board(bad_length)

    def test_grid_with_wrong_size_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="size of grid doesn't match"):
            Board(2, [True, False, True])  # needs 4 cells, got 3

    def test_grid_too_long_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="size of grid doesn't match"):
            Board(2, [True, False, True, False, True])

    def test_grid_not_a_list_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="data type of grid"):
            Board(2, (True, False, True, False))  # tuple, not list
    
    def test_grid_with_non_bool_cell_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="invalid value"):
            Board(2, [True, False, True, 1])  # 1 is not a bool

    def test_grid_of_none_type_cells_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="invalid value"):
            Board(2, [True, None, True, False]) # None is not a bool


class TestFromTwoDGrid:

    def test_valid_2d_grid(self):
        board = Board.from_2d_grid([[True, False], [False, True]])
        assert board.get_length() == 2
        assert board.get_grid() == [True, False, False, True]

    def test_ragged_rows_raise_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="the data type or the size of row doesn't match"):
            Board.from_2d_grid([[True, False], [True]])

    def test_non_sequence_input_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="list or tuple"):
            Board.from_2d_grid(123)

    def test_non_bool_elements_raise_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="containing invalid value"):
            Board.from_2d_grid([[1, 0], [0, 1]])

    def test_string_input_raises_invalid_grid(self):
        # str is technically a Sequence, so it slips past the outer check;
        # it still fails once individual "rows" (chars) are validated.
        with pytest.raises(InvalidGrid, match="the data type or the size of row doesn't match"):
            Board.from_2d_grid("ab")


class TestPress:

    def test_press_toggles_self_and_orthogonal_neighbors(self):
        board = Board(3)
        board.press(1, 1)
        expected = [
            False, True,  False,
            True,  True,  True,
            False, True,  False,
        ]
        assert board.get_grid() == expected

    def test_press_corner_only_toggles_valid_neighbors(self):
        board = Board(2)
        board.press(0, 0)
        # (0,0) toggles itself, (1,0) and (0,1); 
        # (−1,0) and (0,−1) are off-board
        assert board.get_grid() == [True, True, True, False]

    def test_double_press_same_cell_returns_to_original(self):
        board = Board(3)
        original = board.get_grid().copy()
        board.press(1, 1)
        board.press(1, 1)
        assert board.get_grid() == original

    @pytest.mark.parametrize("row,col", [
        (1.0 ,   1),    # float row
        (1   , 1.0),    # float col
        ("1" ,   1),    # str rows
        (None,   0),    # None row
        (True,   0),    # bool is not accepted as int here (strict type check)
    ])
    def test_press_with_non_int_coords_raises_type_error(self, row, col):
        board = Board(3)
        with pytest.raises(TypeError, match="row and col must be integer"):
            board.press(row, col)

    def test_press_row_too_large_raises_index_error(self):
        board = Board(3)
        with pytest.raises(IndexError, match="value range of row and col"):
            board.press(3, 0)

    def test_press_col_too_large_raises_index_error(self):
        board = Board(3)
        with pytest.raises(IndexError):
            board.press(0, 3)

    def test_press_negative_row_raises_index_error(self):
        board = Board(3)
        with pytest.raises(IndexError):
            board.press(-1, 0)

    def test_press_negative_col_raises_index_error(self):
        board = Board(3)
        with pytest.raises(IndexError):
            board.press(0, -1)

    def test_press_far_out_of_range_raises_index_error(self):
        board = Board(2)
        with pytest.raises(IndexError):
            board.press(10, 10)

    def test_press_out_of_range_does_not_mutate_board(self):
        board = Board(3)
        original = board.get_grid().copy()
        with pytest.raises(IndexError):
            board.press(5, 5)
        assert board.get_grid() == original


class TestCopy:

    def test_copy_produces_equal_but_independent_board(self):
        board = Board(3)
        board.press(0, 0)
        clone = board.copy()

        assert clone == board
        assert clone is not board

        clone.press(1, 1)
        assert clone != board  # mutating clone must not affect original

    def test_is_all_off_true_for_fresh_board(self):
        assert Board(4).is_all_off()

    def test_is_all_off_false_after_press(self):
        board = Board(4)
        board.press(0, 0)
        assert not board.is_all_off()


class TestDunders:

    def test_equal_boards(self):
        assert Board(2) == Board(2)

    def test_unequal_boards_different_grid(self):
        b1 = Board(2)
        b2 = Board(2)
        b2.press(0, 0)
        assert b1 != b2

    def test_eq_against_non_board_returns_false(self):
        assert (Board(2) == "not a board") is False
        assert (Board(2) == 5) is False
        assert (Board(2) == None) is False

    def test_repr_contains_length_and_grid(self):
        board = Board(2)
        r = repr(board)
        assert "Board(" in r
        assert "length=2" in r

    def test_str_produces_grid_with_correct_number_of_rows(self):
        board = Board(3)
        text = str(board)
        lines = text.splitlines()
        # header line + one line per row
        assert len(lines) == 3 + 1

    def test_str_reflects_on_off_state(self):
        board = Board(1)
        board.press(0, 0)
        assert "O" in str(board)

        board2 = Board(1)
        assert "." in str(board2) and "O" not in str(board2)


class TestPosition:

    def test_position_is_namedtuple_with_row_col(self):
        pos = Position(1, 2)
        assert pos.row == 1
        assert pos.col == 2
        assert pos == (1, 2)