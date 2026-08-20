import pytest

from lightsout import Board, Generator, Solver


class TestBasics:

    def test_puzzle_has_requested_length(self):
        gen = Generator(4, random_seed=1)
        puzzle = gen.get_puzzle()
        assert puzzle.get_length() == 4

    def test_puzzle_returns_board_instance(self):
        gen = Generator(3, random_seed=1)
        assert isinstance(gen.get_puzzle(), Board)

    def test_puzzle_is_never_all_off(self):
        # regenerate() explicitly avoids the trivial "all lights off" puzzle
        for seed in range(100):
            gen = Generator(2, random_seed=seed)
            assert not gen.get_puzzle().is_all_off()

    def test_get_puzzle_returns_independent_copy(self):
        gen = Generator(3, random_seed=1)
        puzzle = gen.get_puzzle()
        puzzle.press(0, 0)
        # mutating the returned board must not affect the generator's board
        assert gen.get_puzzle() != puzzle


class TestDeterminism:

    def test_same_seed_produces_same_puzzle(self):
        gen1 = Generator(4, random_seed=42)
        gen2 = Generator(4, random_seed=42)
        assert gen1.get_puzzle() == gen2.get_puzzle()

    def test_reset_seed_then_regenerate_reproduces_puzzle(self):
        gen = Generator(4, random_seed=42)
        first = gen.get_puzzle()

        gen.regenerate()
        gen.reset_seed(42)
        gen.regenerate()

        assert gen.get_puzzle() == first

    def test_none_seed_still_produces_valid_puzzle(self):
        # just ensure no crash and validity
        gen = Generator(3, random_seed=None)
        puzzle = gen.get_puzzle()
        assert puzzle.get_length() == 3
        assert not puzzle.is_all_off()


class TestRegenerate:

    def test_regenerate_replaces_puzzle(self):
        gen = Generator(3, random_seed=1)

        before = gen.get_puzzle()
        gen.regenerate()
        after = gen.get_puzzle()

        assert after.get_length() == before.get_length()
        assert not after.is_all_off()


class TestSolvability:

    @pytest.mark.parametrize("length", [2, 3, 4, 5, 10])
    def test_generated_puzzles_are_always_solvable(self, length):
        # every puzzle produced by pressing buttons from the all-off state
        # it must be solvable, for various board sizes
        for _ in range(50):
            gen = Generator(length)
            puzzle = gen.get_puzzle()
            solver = Solver(puzzle)
            assert solver.is_solvable()


class TestConstructionErrors:

    @pytest.mark.parametrize("bad_length", ["3", None, 3.0, [3], True])
    def test_non_int_length_raises_type_error(self, bad_length):
        with pytest.raises(TypeError, match="length must be integer"):
            Generator(bad_length)

    @pytest.mark.parametrize("bad_length", [0, -1, -5])
    def test_non_positive_length_raises_value_error(self, bad_length):
        with pytest.raises(ValueError, match="length must be positive"):
            Generator(bad_length)