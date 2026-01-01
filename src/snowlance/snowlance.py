import threading

from datetime import datetime
from .snowflake import SnowFlake
from .typecheck import typecheck
from .datatypes import Resolution
from .constants import (
    TIME_BIT_WIDTH,
    INSTANCE_BIT_WIDTH,
    SEQ_BIT_WIDTH,
    EPOCH,
)
from .util import (
    compute_lifespin,
    convert_datetime,
    current_time,
    get_monotonic_offset,
    to_days,
    to_period,
    to_years,
)

# TODO
"""
- handle wall timer going back word issue
    - soluition: use wall timer to caliborate a monotonic timer on each start, use the monotonic timer since ever
"""

Instance = str | int


class SnowLance:
    def __init__(
        self,
        timestamp_bit_width: int = TIME_BIT_WIDTH,
        instance_bit_width: int = INSTANCE_BIT_WIDTH,
        seq_bit_width: int = SEQ_BIT_WIDTH,
        epoch: datetime = EPOCH,
        resolution: Resolution = "ms",
    ) -> None:
        self.timestamp_bit_width = timestamp_bit_width
        self.instance_bit_width = instance_bit_width
        self.seq_bit_width = seq_bit_width
        self._epoch = convert_datetime(epoch, resolution)
        self._resolution = resolution

        # caliborate monotonic timer
        self._mono_offset = get_monotonic_offset(resolution)

        # thread states
        self.lock = threading.Lock()
        self.last_seq = 0
        self.last_t = None

    @property
    def epoch(self):
        return self._epoch

    @property
    def resolution(self):
        return self._resolution

    @property
    def bit_length(self):
        return self.timestamp_bit_width + self.instance_bit_width + self.seq_bit_width

    @property
    def time_left(self):
        """
        number of years current timestamp bit width can support before it run out of ids
        """
        past_time = current_time(self.resolution, self._mono_offset) - self.epoch
        time_left = pow(2, self.timestamp_bit_width) - past_time
        return to_period(time_left, self.resolution)

    @property
    def timestamp_mask(self):
        return ((1 << self.timestamp_bit_width) - 1) << (
            self.instance_bit_width + self.seq_bit_width
        )

    @property
    def instance_mask(self):
        return ((1 << self.instance_bit_width) - 1) << self.seq_bit_width

    @property
    def seq_mask(self):
        return (1 << self.seq_bit_width) - 1

    @property
    def _since_epoch(self) -> int:
        """
        Number of miliseconds sincd epoch
        """
        t = current_time(self.resolution, self._mono_offset) - self.epoch
        return t

    @typecheck
    def encode(self, t: int, instance: Instance, seq: int) -> SnowFlake:
        """
        Concatenate a SnowFlake ID
        """
        if t.bit_length() > self.timestamp_bit_width:
            raise ValueError(f"Timestamp too big: {t}")
        elif instance.bit_length() > self.instance_bit_width:
            raise ValueError(f"Instance number too big: {instance}")
        elif seq.bit_length() > self.seq_bit_width:
            raise ValueError(f"Seq number too big: {seq}")

        return SnowFlake(
            (t << (self.instance_bit_width + self.seq_bit_width))
            | (instance << self.seq_bit_width)
            | (seq),
            self.timestamp_bit_width,
            self.instance_bit_width,
            self.seq_bit_width,
        )

    @typecheck
    def decode(self, snowflake: int) -> tuple[int, int, int]:
        sf = SnowFlake(
            snowflake,
            self.timestamp_bit_width,
            self.instance_bit_width,
            self.seq_bit_width,
        )
        return sf.timestamp, sf.instance, sf.seq

    def snow(self, instance: Instance, seq: int) -> SnowFlake:
        """
        Generate a SnowFlake ID
        """
        return self.encode(self._since_epoch, instance, seq)

    def auto(self, instance: int = 0) -> SnowFlake:
        """
        Automatically generate a SnowFlake ID
        seq number is reset for every new timestamp, and monotonically increment within each timestamp
        """
        t = self._since_epoch
        with self.lock:
            if t == self.last_t:
                self.last_seq += 1
            else:
                self.last_t = t
                self.last_seq = 0
            return self.encode(self.last_t, instance, self.last_seq)
