"""Small reproducible analysis helpers backed by the production simulator."""
import math
from .workbench.config import Experiment, Pulse
from .workbench.engine import simulate

def refractory_comparison(config_data, refractory_values):
    rows=[]
    for value in refractory_values:
        c=Experiment.model_validate({**config_data,"parameters":{**config_data.get("parameters",{}),"refractory":value}})
        r=simulate(c); times=r["spikes"][0]; rows.append({"refractory_ms":value,"spike_count":len(times),"spike_times_ms":times})
    return rows

def fi_curve(config_data, amplitudes):
    rows=[]
    for amplitude in amplitudes:
        c=Experiment.model_validate({**config_data,"pulses":[{"start":0,"stop":config_data.get("duration",50),"amplitude":amplitude}]})
        r=simulate(c); rows.append({"amplitude_uA_cm2":amplitude,"rate_hz":r["mean_rate_hz"],"spike_count":len(r["spikes"][0])})
    return rows

def adaptation_metrics(spike_times):
    intervals=[b-a for a,b in zip(spike_times,spike_times[1:])]
    return {"spike_count":len(spike_times),"intervals_ms":intervals,"first_interval_ms":intervals[0] if intervals else None,"last_interval_ms":intervals[-1] if intervals else None,"adaptation_ratio":intervals[-1]/intervals[0] if intervals else None}

def bursts(spike_times, max_interval_ms=10):
    groups=[]
    for t in spike_times:
        if not groups or t-groups[-1][-1]>max_interval_ms: groups.append([t])
        else: groups[-1].append(t)
    return [{"start_ms":g[0],"end_ms":g[-1],"spike_count":len(g)} for g in groups if len(g)>1]

def model_gallery(configs):
    return [{"model":c["model"],"spike_count":len((r:=simulate(Experiment.model_validate(c)))["spikes"][0]),"manifest":r["manifest"]} for c in configs]
