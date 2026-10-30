"""Deterministic synaptic event kernels used by analysis fixtures."""
import math
def exponential_event(weight,t_ms,tau_ms=5):
    if tau_ms<=0 or t_ms<0: raise ValueError('time must be nonnegative and tau positive')
    return weight*math.exp(-t_ms/tau_ms)
def alpha_event(weight,t_ms,tau_ms=5):
    if tau_ms<=0 or t_ms<0: raise ValueError('time must be nonnegative and tau positive')
    return weight*(t_ms/tau_ms)*math.exp(1-t_ms/tau_ms)
def synaptic_current(g,voltage,reversal): return g*(reversal-voltage)
