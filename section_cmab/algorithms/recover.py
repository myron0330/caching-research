# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Recover methods
# **********************************************************************************#


def recover_from_(variables, c_bk):
    """
    Recover from c_bk

    Args:
        variables(variables): variable parameters
        c_bk(matrix): relaxing problem solution
    """
    keys = range(c_bk.shape[1])
    file_info = variables.file_info
    base_stations = variables.base_stations
    for index in xrange(c_bk.shape[0]):
        result = dict(zip(keys, c_bk[index, :]))
        sorted_keys = sorted(result, key=lambda _: result[_], reverse=True)
        candidates, total_size = list(), 0
        base_station = base_stations[index]
        for candidate in sorted_keys:
            if result[candidate] == 0 or total_size + file_info[candidate] > base_station.memory:
                break
            candidates.append(candidate)
            total_size += file_info[candidate]
        c_bk[index, :] = [0] * c_bk.shape[1]
        c_bk[index, candidates] = [1] * len(candidates)
    return c_bk
