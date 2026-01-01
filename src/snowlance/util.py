from datetime import datetime
from .datatypes import Resolution
import time


def get_monotonic_offset(resolution: Resolution) -> int:

    if resolution == "ns":
        wall_time = time.time_ns()
        mono_time = time.monotonic_ns()
        return mono_time - wall_time

    wall_time = time.time()
    mono_time = time.monotonic()
    offset = mono_time - wall_time
    if resolution == "s":
        return int(offset)
    if resolution == "ms":
        return int(offset * 1000)
    if resolution == "us":
        return int(offset * 1000_000)


def convert_datetime(date: datetime, resolution: Resolution) -> int:
    if resolution == "s":
        return int(date.timestamp())
    if resolution == "ms":
        return int(date.timestamp() * 1000)
    if resolution == "us":
        return int(date.timestamp() * 1000_000)
    if resolution == "ns":
        return int(date.timestamp() * 1000_000_000)


def current_time(resolution: Resolution, monotonic_offset: int) -> int:
    if resolution == "s":
        return int(time.monotonic()) - monotonic_offset
    if resolution == "ms":
        return int(time.monotonic() * 1000) - monotonic_offset
    if resolution == "us":
        return int(time.monotonic() * 1000_000) - monotonic_offset
    if resolution == "ns":
        return int(time.monotonic_ns()) - monotonic_offset


def compute_lifespin(bit_width: int, resolution: Resolution) -> float:
    number = pow(2, bit_width)
    return to_years(number, resolution)


def to_years(t: int, resolution: Resolution) -> float:
    if resolution == "s":
        return t / (86400 * 30 * 12)
    if resolution == "ms":
        return t / (1000 * 86400 * 30 * 12)
    if resolution == "us":
        return t / (1000_000 * 86400 * 30 * 12)
    if resolution == "ns":
        return t / (1000_000_000 * 86400 * 30 * 12)


def to_days(t: int, resolution: Resolution) -> float:
    if resolution == "s":
        return t / (86400)
    if resolution == "ms":
        return t / (1000 * 86400)
    if resolution == "us":
        return t / (1000_000 * 86400)
    if resolution == "ns":
        return t / (1000_000_000 * 86400)


def to_seconds(t: int, resolution: Resolution) -> float:
    if resolution == "s":
        return t
    if resolution == "ms":
        return t / 1000
    if resolution == "us":
        return t / 1000_000
    if resolution == "ns":
        return t / 1000_000_000


def to_period(t: int, resolution: Resolution) -> tuple[float, str]:
    if t <= 0:
        return 0, "years"

    years = to_years(t, resolution)

    if years > 1:
        return years, f"years"

    days = to_days(t, resolution)
    if days > 1:
        return days, f"days"

    return to_seconds(t,  resolution), f"seconds"
