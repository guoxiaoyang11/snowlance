import pytest
from datetime import datetime, timezone, timedelta
from snowlance import SnowLance


def test_init_ms():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)
    assert lance.bit_length == 64


def test_encode_ms():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)

    t = datetime.now()
    time_ms = int(((t - epoch).total_seconds()) * 1000)
    flake = lance.encode(time_ms, 1, 2)

    assert flake > 0
    assert flake.timestamp == time_ms
    assert flake.instance == 1
    assert flake.seq == 2


def test_snow_ms():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)
    flake = lance.snow(3, 4)

    assert flake > 0
    assert flake.instance == 3
    assert flake.seq == 4


def test_auto_ms():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)
    flake = lance.auto(1)
    assert flake > 0
    assert flake.timestamp > 0
    assert flake.seq == 0


def test_init_s():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch, "s")
    assert lance.bit_length == 64


def test_encode_s():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch, "s")

    t = datetime.now()
    time_ms = int(((t - epoch).total_seconds()) * 1000)
    flake = lance.encode(time_ms, 1, 2)

    assert flake > 0
    assert flake.timestamp == time_ms
    assert flake.instance == 1
    assert flake.seq == 2


def test_snow_s():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)
    flake = lance.snow(3, 4)

    assert flake > 0
    assert flake.instance == 3
    assert flake.seq == 4


def test_auto_s():
    epoch = datetime(1970, 1, 1)
    lance = SnowLance(42, 10, 12, epoch)
    flake = lance.auto(1)
    assert flake > 0
    assert flake.timestamp > 0
    assert flake.seq == 0
