from .constants import TIME_BIT_WIDTH, INSTANCE_BIT_WIDTH, SEQ_BIT_WIDTH


class SnowFlake(int):
    def __new__(
        cls,
        value,
        timestamp_bit_width: int = TIME_BIT_WIDTH,
        instance_bit_width: int = INSTANCE_BIT_WIDTH,
        seq_bit_width: int = SEQ_BIT_WIDTH,
    ):
        width = timestamp_bit_width + instance_bit_width + seq_bit_width
        max_value = (1 << width) - 1
        if value < 0 or value > max_value:
            raise ValueError(f"Value too big: {value}")
        obj = super().__new__(cls, value)
        obj._timestamp_bit_width = timestamp_bit_width
        obj._instance_bit_width = instance_bit_width
        obj._seq_bit_width = seq_bit_width
        return obj

    @property
    def timestamp_bit_width(self):
        return self._timestamp_bit_width

    @property
    def instance_bit_width(self):
        return self._instance_bit_width

    @property
    def seq_bit_width(self):
        return self._seq_bit_width

    @property
    def width(self):
        return self.timestamp_bit_width + self.instance_bit_width + self.seq_bit_width

    @property
    def _timestamp_mask(self):
        return ((1 << self.timestamp_bit_width) - 1) << (
            self.instance_bit_width + self.seq_bit_width
        )

    @property
    def _instance_mask(self):
        return ((1 << self.instance_bit_width) - 1) << self.seq_bit_width

    @property
    def _seq_mask(self):
        return (1 << self.seq_bit_width) - 1

    @property
    def timestamp(self):
        return (self & self._timestamp_mask) >> (
            self.instance_bit_width + self.seq_bit_width
        )

    @property
    def instance(self):
        return (self & self._instance_mask) >> self.seq_bit_width

    @property
    def seq(self):
        return self & self._seq_mask


if __name__ == "__main__":
    pass
