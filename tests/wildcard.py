from snowlance import SnowLance, SnowFlake

lance = SnowLance(
    resolution="ns"
)

print(lance.time_left)
