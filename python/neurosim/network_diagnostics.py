"""Reproducible diagnostics for production event scheduling and synapse analysis."""
import time
from .workbench.engine import effective_delay_steps, connectivity, simulate
from .workbench.config import Experiment
from .synapse_metrics import exponential_event, synaptic_current

def delay_roundtrip(delay_ms, dt_ms):
    if delay_ms <= 0 or dt_ms <= 0: raise ValueError('delay and dt must be positive')
    steps=effective_delay_steps(delay_ms,dt_ms)
    return {"delay_ms":delay_ms,"dt_ms":dt_ms,"steps":steps,"effective_delay_ms":steps*dt_ms}

def tie_order(events):
    return [event[1] for event in sorted(events, key=lambda event: (event[0], event[1]))]

def directed_edges(config_data):
    c=Experiment.model_validate(config_data)
    return connectivity(c)

def superpose(weights, t_ms, tau_ms=5):
    return sum(exponential_event(w,t_ms,tau_ms) for w in weights)

def recurrent_summary(config_data):
    c=Experiment.model_validate(config_data); r=simulate(c)
    return {"spike_count":sum(map(len,r["spikes"])),"edge_count":len(r["edges"]),"manifest":r["manifest"]}

def sparse_summary(config_data):
    edges=directed_edges(config_data); return {"edge_count":len(edges),"edges":edges}

def inspect_synapses(config_data):
    c=Experiment.model_validate(config_data); return [{"source":s,"target":t,"inhibitory":i} for s,t,i in connectivity(c)]

def benchmark_events(count=10000):
    start=time.perf_counter(); total=sum(exponential_event(0.05,i%10) for i in range(count)); return {"count":count,"seconds":time.perf_counter()-start,"checksum":total}
