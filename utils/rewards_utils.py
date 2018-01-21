from __future__ import division
import numpy as np


def calculate_cmab_rewards(variables, c_bkt, d_bkt, aggregate=False, alpha=1.):
    """
    Calculate rewards of cmab section.

    Args:
        variables(variables): variables
        c_bkt(matrix): c_bkt
        d_bkt(matrix): d_bkt
        aggregate(boolean): whether to aggregate the rewards
        alpha(float): alpha
    """
    delta = max(variables.sizes) * (1 / variables.v_bd + 1 / variables.v_cb)
    c_kt = np.sign(c_bkt.sum(axis=0))
    v_bd, v_bb, v_cb = variables.v_bd, variables.v_bb, variables.v_cb
    file_info = variables.file_info
    r_0 = 1
    rewards = dict()
    for base_station in variables.base_stations:
        identity = base_station.identity
        c_bt = c_bkt[identity, :]
        d_bt = d_bkt[identity, :]
        reward = 0
        for f in variables.files:
            latency = file_info[f] * (1. / v_bd + (1. - c_bt[f]) * (1. * c_kt[f] / v_bb + (1. - c_kt[f]) / v_cb))
            reward += d_bt[f] * (delta - latency) * r_0
        rewards[identity] = reward * alpha
    if aggregate:
        return sum(rewards.values())
    return rewards


def calculate_cftl_rewards():
    """
    Calculate rewards in cftl section.
    """
    pass
