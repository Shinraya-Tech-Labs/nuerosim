"""Small deterministic plasticity and motif primitives for reproducible audits."""
import math
def pair_stdp(delta_ms,a_plus=.01,a_minus=.012,tau_plus=20,tau_minus=20): return a_plus*math.exp(-delta_ms/tau_plus) if delta_ms>0 else -a_minus*math.exp(delta_ms/tau_minus)
def additive_bound(weight,delta,wmin=0,wmax=1): return min(wmax,max(wmin,weight+delta))
def multiplicative_bound(weight,delta,wmin=0,wmax=1): return min(wmax,max(wmin,weight+delta*(wmax-weight if delta>0 else weight-wmin)))
def depression(weight,spikes,tau=800): return weight*math.exp(-spikes/tau)
def facilitation(weight,spikes,u=.2): return weight*(1+u*spikes)
def hebbian(pre,post,rate=.01): return rate*pre*post
def homeostatic_scale(weights,target,current,rate=.01): return [w+rate*(target-current)*w for w in weights]
