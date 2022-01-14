""" Location binning """
__RANGE_BIN_SIZE = 50

""" Determine bin """
def num(location):
    global __RANGE_BIN_SIZE
    return (int(location.x / __RANGE_BIN_SIZE), int(location.y / __RANGE_BIN_SIZE), int(location.z / __RANGE_BIN_SIZE))

""" Bins to check """
def search(bins, location, rng):
    objs = []
    for x in range(int((location.x - rng) / __RANGE_BIN_SIZE), int((location.x + rng) / __RANGE_BIN_SIZE) + 1):
        for y in range(int((location.y - rng) / __RANGE_BIN_SIZE), int((location.y + rng) / __RANGE_BIN_SIZE) + 1):
            for z in range(int((location.z - rng) / __RANGE_BIN_SIZE), int((location.z + rng) / __RANGE_BIN_SIZE) + 1):
                bin_num = (x, y, z)
                for obj in bins.get(bin_num, []):
                    objs.append((obj, bin_num))
    return objs
