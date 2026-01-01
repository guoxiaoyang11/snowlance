import pytest

from snowlance import SnowFlake


def test_init():
    test_int = 200598221754368
    flake = SnowFlake(
        test_int, timestamp_bit_width=42, instance_bit_width=10, seq_bit_width=12
    )

    assert flake == test_int
    assert flake.width == 64


def test_overflow():
    with pytest.raises(ValueError):
        SnowFlake(99999999999999999999)
