#!/usr/bin/env python3

import random
from time import time

def datasource_dummy(telemetry: list,
                     permutation: float = 0.1):
    """
    The purpose of this function is to create dummy telemetry for debugging
    UI elements and plotting code. It will take a "telemetry" frame (a list),
    and then permutate it in the following way:
        - The first value (0) is a Unix timestamp, and it will update this
            value when returning the telemetry frame.
        - The other values it will random walk according to a permutation
            factor, which can be specified as input argument too. A permutation
            factor of 0 will keep the data constant.
        - It will take any telemetry list of size 1 and above.

    Returns: Python list with:
        [updated Unix stamp, data1_perm, data2_perm, ... , dataN_perm]
    """
    # Loop across all values in telemetry and mutate them, except entry 0:
    for i in range(len(telemetry)-1):
        # Mutate the telemetry
        telemetry[i+1] += random.uniform(-permutation, permutation)

    # Update the Unix timestamp
    telemetry[0] = time()

    return telemetry


# # Test code
# time0 = time()
#
# start_telemetry = [time0, 1.0, -12.0, 44.0]
# telemetry = start_telemetry
# cycles = 2000
#
#
# for i in range(cycles):
#     telemetry = datasource_dummy(telemetry,
#                                  permutation=0.1)
#     # print(telemetry)
#
# print("Completed", cycles, "cycles in", time()-time0, "s.")
