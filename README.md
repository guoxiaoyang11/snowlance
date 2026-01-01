# Snow Lance

Thread safe, monotonic, customizable, eazy to use SnowFlake ID generator.

## Installation

```bash
pip install snowlance-0.1.0-py3-none-any.whl
```

## Usage

You can initiate a SnowLance as follow:

```python
lance = SnowLance() # all parameters have default values
print(lance.auto())
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

Timestamp resolution can be any of `["s", "ms", "us", "ns"]`. But be aware, you can *run out of time* with SnowFlake ID. You can call 'time_left' method to see how much time left for you current epoch and resolution.
```
lance = SnowLance()
print(lance.time_left)
>>(141.39613429224536, 'years')
```

With a 


## Garantees (Expected behavior)

- Thread safe
- Monotonic
    - A Snowlance instance garantee to produce monotonically increasing IDs for single runs
    - No garantee for multiple Snowlance instance with same epoch and resolution

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
- Current 