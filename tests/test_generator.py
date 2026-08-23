import pytest

from lightsout import Board, Generator, Solver


class TestBasics:

    @pytest.mark.parametrize("height,width", [
        (4, 4),  # square
        (3, 5),  # rectangle
    ])
    def test_puzzle_has_requested_shape(self, height, width):
        gen = Generator(height, width, random_seed=1)
        puzzle = gen.get_puzzle()
        assert puzzle.get_height() == height
        assert puzzle.get_width() == width

    def test_puzzle_returns_board_instance(self):
        gen = Generator(3, 3, random_seed=1)
        assert isinstance(gen.get_puzzle(), Board)

    @pytest.mark.parametrize("height,width", [
        (2, 2),  # square
        (2, 4),  # rectangle
    ])
    def test_puzzle_is_never_all_off(self, height, width):
        # regenerate() explicitly avoids the trivial "all lights off" puzzle
        for seed in range(100):
            gen = Generator(height, width, random_seed=seed)
            assert not gen.get_puzzle().is_all_off()

    def test_get_puzzle_returns_independent_copy(self):
        gen = Generator(3, 3, random_seed=1)
        puzzle = gen.get_puzzle()
        puzzle.press(0, 0)
        # mutating the returned board must not affect the generator's board
        assert gen.get_puzzle() != puzzle


class TestDeterminism:

    @pytest.mark.parametrize("height,width", [
        (4, 4),  # square
        (3, 6),  # rectangle
    ])
    def test_same_seed_produces_same_puzzle(self, height, width):
        gen1 = Generator(height, width, random_seed=42)
        gen2 = Generator(height, width, random_seed=42)
        assert gen1.get_puzzle() == gen2.get_puzzle()

    def test_reset_seed_then_regenerate_reproduces_puzzle(self):
        gen = Generator(4, 4, random_seed=42)
        first = gen.get_puzzle()

        gen.regenerate()
        gen.reset_seed(42)
        gen.regenerate()

        assert gen.get_puzzle() == first

    def test_none_seed_still_produces_valid_puzzle(self):
        # just ensure no crash and validity
        gen = Generator(3, 3, random_seed=None)
        puzzle = gen.get_puzzle()
        assert puzzle.get_height() == 3
        assert puzzle.get_width() == 3
        assert not puzzle.is_all_off()


class TestRegenerate:

    @pytest.mark.parametrize("height,width", [
        (3, 3),  # square
        (2, 6),  # rectangle
    ])
    def test_regenerate_replaces_puzzle(self, height, width):
        gen = Generator(height, width, random_seed=1)

        before = gen.get_puzzle()
        gen.regenerate()
        after = gen.get_puzzle()

        assert after.get_height() == before.get_height() == height
        assert after.get_width() == before.get_width() == width
        assert not after.is_all_off()


class TestSolvability:

    @pytest.mark.parametrize("height,width", [
        (2, 2), (3, 3), (4, 4), (5, 5), (10, 10),  # square
        (2, 3), (3, 2), (2, 5), (5, 2), (4, 7),    # rectangular
    ])
    def test_generated_puzzles_are_always_solvable(self, height, width):
        # every puzzle produced by pressing buttons from the all-off state
        # must be solvable, for various board shapes
        for _ in range(50):
            gen = Generator(height, width)
            puzzle = gen.get_puzzle()
            solver = Solver(puzzle)
            assert solver.is_solvable()


class TestConstructionErrors:

    @pytest.mark.parametrize("bad_height", ["3", None, 3.0, [3], True])
    def test_non_int_height_raises_type_error(self, bad_height):
        with pytest.raises(TypeError, match="height must be integer"):
            Generator(bad_height, 3)

    @pytest.mark.parametrize("bad_width", ["3", None, 3.0, [3], True])
    def test_non_int_width_raises_type_error(self, bad_width):
        with pytest.raises(TypeError, match="width must be integer"):
            Generator(3, bad_width)

    @pytest.mark.parametrize("bad_height", [0, -1, -5])
    def test_non_positive_height_raises_value_error(self, bad_height):
        with pytest.raises(ValueError, match="height must be positive"):
            Generator(bad_height, 3)

    @pytest.mark.parametrize("bad_width", [0, -1, -5])
    def test_non_positive_width_raises_value_error(self, bad_width):
        with pytest.raises(ValueError, match="width must be positive"):
            Generator(3, bad_width)