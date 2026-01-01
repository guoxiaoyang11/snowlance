# Snow Lance

Thread safe, monotonic, customizable, eazy to use SnowFlake ID generator.

## Installation

```bash
pip install snowlance
```

## Usage

You can initiate a SnowLance as follow:

```python
lance = SnowLance() # all parameters have default values
print(lance.auto())

>>> 251078994034688
```

You may decide the number of bits for each part of the SnowFlake ID, system epoch, as well as timestamp resolution.

```python
lance = SnowLance(
    timestamp_bit_width=42,
    instance_bit_width=10,
    seq_bit_width=12,
    epoch=datetime(2025, 1, 1),
    resolution="ms",
)
```

Since python does not have a limit on number of bits for intergers, neither does SnowLance. For the sake of compatibility with other non-python systems, you may want to keep the sum of the bits to be 64.  

```python
lance = SnowLance(
    timestamp_bit_width=100,
    instance_bit_width=14,
    seq_bit_width=14,
)
```

Timestamp resolution can be any of `["s", "ms", "us", "ns"]`. But be aware, you can *run out of time* with SnowFlake ID. You can call 'time_left' method to see how much time left for you current epoch and resolution. Be aware that if you choose nanososecond as you resolution and wish to keep the IDs within 64 bits, the amount of time available could be very short.
```python
lance = SnowLance()
print(lance.time_left)
>>> (141.39613429224536, 'years')
```

With a SnowLance instance, you can generate Snowflake IDs with `.auto()` method by providing the instance id:

```python
lance.auto(1)       # can provide instance id, sequence number is automatically managed
lance.auto()        # default to instance '0'
```
A `ValueError` will be raised if the sequence number you provide has been used within that milisecond (or whichever resolution you choosed)
You may also use `.snow()` method, in which case you will need to manage the sequence number your self:

```python
lance.snow(1, 2)    # need to provide both instance id and sequence number
```

You can use both methods interchangeably without compromising the monotonic garantee, but you will need to carefully make sure the sequence number you provide in `.snow()` has not been used by `.auto()`, otherwise the `ValueError` will be raised

You can also use the `.decode()` method to put a custom timestamp, an instance ID, and a sequence number together to get a Snowflake ID. In which case, the number you provide need to match the bit settings, and no garantee is made to Snowflake IDs produced in such a way, as the timestamp and sequence number will not be recorded:

```python
lance.encode(60176267, 0, 1)
>>> 252397557383169
```


You can decode a Snowflake ID using `.decode()` method, in which case you need to make sure the Snowflake ID you provide use the same bit settings as the `SnowLance` instance. Epoch and resolution have not influence on this step.

```python
timestamp, instance, seq = lance.decode(252397557383169)
```

## Garantees (Expected behavior)

- Thread safe
- Monotonic
    - A single `Snowlance` instance garantee to produce monotonically increasing IDs for single runs
    - No garantee for multiple Snowlance instances with same epoch and resolution

## Run, build, and test

### Install current source code

```bash
pip install -e .
```

### Unit test

```bash
pip install -e .[test] && pytest
```

### Build from source

```bash
rm -rf build/ dist/ *.egg-info/ && python -m build --wheel
```

You should be able to find the `whl` file in `/dist` directory

## TODOs

There are a few things to consider
- Monotonic garantee across multiple SnowLance instances