import pytest

from lightsout import Board, InvalidGrid, Position


class TestConstruction:

    def test_default_grid_is_all_off(self):
        board = Board(3, 4)
        assert board.get_height() == 3
        assert board.get_width() == 4
        assert board.get_grid() == [False] * 3 * 4
        assert board.is_all_off()

    @pytest.mark.parametrize("height,width,grid", [
        (2, 2, [True, False, False, True]),                                # square
        (2, 3, [True, False, True, False, True, False]),                   # rectangle
    ])
    def test_explicit_grid_is_used(self, height, width, grid):
        board = Board(height, width, grid)
        assert board.get_grid() == grid
        assert board.get_height() == height
        assert board.get_width() == width

    def test_grid_is_deep_copied_on_construction(self):
        grid = [True, False, False, True]
        board = Board(2, 2, grid)
        grid[0] = False
        # mutating the original list must not affect the board
        assert board.get_grid() == [True, False, False, True]

    @pytest.mark.parametrize("height,width", [
        (1, 1), (2, 2), (5, 5), (10, 10),  # square
        (1, 4), (4, 1),                    # single row / single column
        (2, 3), (3, 2),                    # small rectangles
        (3, 7), (7, 3),                    # larger rectangles
    ])
    def test_various_valid_shapes(self, height, width):
        board = Board(height, width)
        assert board.get_height() == height
        assert board.get_width() == width
        assert len(board.get_grid()) == height * width


class TestConstructionErrors:

    @pytest.mark.parametrize("bad_height", ["3", None, [3], (3,), True])
    def test_non_int_height_with_default_grid_raises_type_error(self, bad_height):
        with pytest.raises(TypeError, match="height must be integer"):
            Board(bad_height, 3)

    @pytest.mark.parametrize("bad_width", ["3", None, [3], (3,), True])
    def test_non_int_width_with_default_grid_raises_type_error(self, bad_width):
        with pytest.raises(TypeError, match="width must be integer"):
            Board(3, bad_width)

    def test_non_int_height_with_explicit_grid_raises_type_error_with_message(self):
        # check_length() run before grid validation and raise.
        with pytest.raises(TypeError, match="height must be integer"):
            Board("2", 2, [True, False, True, False])

    def test_non_int_width_with_explicit_grid_raises_type_error_with_message(self):
        with pytest.raises(TypeError, match="width must be integer"):
            Board(2, "2", [True, False, True, False])

    @pytest.mark.parametrize("bad_height", [0, -1, -100])
    def test_non_positive_height_raises_value_error(self, bad_height):
        with pytest.raises(ValueError, match="height must be positive"):
            Board(bad_height, 3)

    @pytest.mark.parametrize("bad_width", [0, -1, -100])
    def test_non_positive_width_raises_value_error(self, bad_width):
        with pytest.raises(ValueError, match="width must be positive"):
            Board(3, bad_width)

    @pytest.mark.parametrize("height,width,grid", [
        (2, 2, [True, False, True]),                       # square, needs 4 cells, got 3
        (2, 2, [True, False, True, False, True]),          # square, needs 4 cells, got 5 (too long)
        (2, 3, [True, False, True, False]),                # rectangle, needs 6 cells, got 4
    ])
    def test_grid_with_wrong_size_raises_invalid_grid(self, height, width, grid):
        with pytest.raises(InvalidGrid, match="size of grid doesn't match"):
            Board(height, width, grid)

    def test_grid_not_a_list_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="data type of grid"):
            Board(2, 2, (True, False, True, False))  # tuple, not list

    def test_grid_with_non_bool_cell_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="invalid value"):
            Board(2, 2, [True, False, True, 1])      # 1 is not a bool

    def test_grid_of_none_type_cells_raises_invalid_grid(self):
        with pytest.raises(InvalidGrid, match="invalid value"):
            Board(2, 2, [True, None, True, False])   # None is not a bool


class TestFromTwoDGrid:

    @pytest.mark.parametrize("grid_2d,expected_height,expected_width,expected_grid", [
        (
            [[True, False], [False, True]],                     # square
            2, 2, [True, False, False, True],
        ),
        (
            [[True, False, True], [False, True, False]],        # rectangle
            2, 3, [True, False, True, False, True, False],
        ),
    ])
    def test_valid_2d_grid(self, grid_2d, expected_height, expected_width, expected_grid):
        board = Board.from_2d_grid(grid_2d)
        assert board.get_height() == expected_height
        assert board.get_width() == expected_width
        assert board.get_grid() == expected_grid

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
        # str is technically a Sequence;
        with pytest.raises(InvalidGrid, match="list or tuple"):
            Board.from_2d_grid("ab")


class TestPress:

    def test_press_toggles_self_and_orthogonal_neighbors(self):
        board = Board(3, 3)
        board.press(1, 1)
        expected = [
            False, True,  False,
            True,  True,  True,
            False, True,  False,
        ]
        assert board.get_grid() == expected

    def test_press_corner_only_toggles_valid_neighbors(self):
        board = Board(2, 2)
        board.press(0, 0)
        # (0,0) toggles itself, (1,0) and (0,1); 
        # (-1,0) and (0,-1) are off-board
        assert board.get_grid() == [True, True, True, False]

    def test_double_press_same_cell_returns_to_original(self):
        board = Board(3, 3)
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
        board = Board(3, 3)
        with pytest.raises(TypeError, match="row and col must be integer"):
            board.press(row, col)

    def test_press_row_too_large_raises_index_error(self):
        board = Board(3, 3)
        with pytest.raises(IndexError, match="value range of row"):
            board.press(3, 0)

    def test_press_col_too_large_raises_index_error(self):
        board = Board(3, 3)
        with pytest.raises(IndexError):
            board.press(0, 3)

    def test_press_negative_row_raises_index_error(self):
        board = Board(3, 3)
        with pytest.raises(IndexError):
            board.press(-1, 0)

    def test_press_negative_col_raises_index_error(self):
        board = Board(3, 3)
        with pytest.raises(IndexError):
            board.press(0, -1)

    def test_press_far_out_of_range_raises_index_error(self):
        board = Board(2, 2)
        with pytest.raises(IndexError):
            board.press(10, 10)

    def test_press_out_of_range_does_not_mutate_board(self):
        board = Board(3, 3)
        original = board.get_grid().copy()
        with pytest.raises(IndexError):
            board.press(5, 5)
        assert board.get_grid() == original


class TestPressOnRectangularBoards:

    @pytest.mark.parametrize("height,width,bad_row,bad_col,good_row,good_col", [
        (3, 2, 2, 2, 2, 1),  # tall & narrow: col 2 is out of range (width is 2)
        (2, 3, 2, 2, 1, 2),  # short & wide: row 2 is out of range (height is 2)
    ])
    def test_press_respects_correct_bound_per_axis(self, height, width, bad_row, bad_col, good_row, good_col):
        board = Board(height, width)
        with pytest.raises(IndexError):
            board.press(bad_row, bad_col)
        board.press(good_row, good_col)  # last valid cell, should not raise

    @pytest.mark.parametrize("height,width,row,col,expected", [
        (2, 4, 0, 1, [                                    # wide board (2 rows x 4 cols)
            True,  True, True,  False,
            False, True, False, False,
        ]),
        (4, 2, 1, 0, [                                    # tall board (4 rows x 2 cols)
            True,  False,
            True,  True,
            True,  False,
            False, False,
        ]),
    ])
    def test_press_toggles_correct_neighbors_on_rectangular_board(self, height, width, row, col, expected):
        board = Board(height, width)
        board.press(row, col)
        assert board.get_grid() == expected


class TestCopy:

    def test_copy_produces_equal_but_independent_board(self):
        board = Board(3, 3)
        board.press(0, 0)
        clone = board.copy()

        assert clone == board
        assert clone is not board

        clone.press(1, 1)
        assert clone != board  # mutating clone must not affect original

    @pytest.mark.parametrize("height,width", [
        (3, 3),  # square
        (2, 5),  # rectangle
    ])
    def test_copy_preserves_shape(self, height, width):
        board = Board(height, width)
        clone = board.copy()
        assert clone.get_height() == height
        assert clone.get_width() == width

    def test_is_all_off_true_for_fresh_board(self):
        assert Board(4, 4).is_all_off()

    def test_is_all_off_false_after_press(self):
        board = Board(4, 4)
        board.press(0, 0)
        assert not board.is_all_off()


class TestDunders:

    def test_equal_boards(self):
        assert Board(2, 2) == Board(2, 2)

    def test_unequal_boards_different_grid(self):
        b1 = Board(2, 2)
        b2 = Board(2, 2)
        b2.press(0, 0)
        assert b1 != b2

    def test_unequal_boards_different_shape_same_cell_count(self):
        # a 2x3 board and a 3x2 board both have 6 cells but different shapes
        b1 = Board(2, 3)
        b2 = Board(3, 2)
        assert b1 != b2

    def test_eq_against_non_board_returns_false(self):
        assert (Board(2, 2) == "not a board") is False
        assert (Board(2, 2) == 5) is False
        assert (Board(2, 2) == None) is False

    def test_repr_contains_height_and_width_and_grid(self):
        board = Board(2, 3)
        r = repr(board)
        assert "Board(" in r
        assert "height=2" in r
        assert "width=3" in r

    def test_str_produces_grid_with_correct_number_of_rows(self):
        board = Board(3, 5)
        text = str(board)
        lines = text.splitlines()
        # header line + one line per row
        assert len(lines) == 3 + 1

    def test_str_reflects_on_off_state(self):
        board = Board(1, 1)
        board.press(0, 0)
        assert "O" in str(board)

        board2 = Board(1, 1)
        assert "." in str(board2) and "O" not in str(board2)


class TestPosition:

    def test_position_is_namedtuple_with_row_col(self):
        pos = Position(1, 2)
        assert pos.row == 1
        assert pos.col == 2
        assert pos == (1, 2)