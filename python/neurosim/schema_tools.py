"""Portable metadata, provenance, migration and subset exchange helpers."""
import hashlib,json
def metadata(model,version=1): return {"schema_version":version,"model":model}
def stimulus_monitor(stimuli,monitors): return {"stimuli":stimuli,"monitors":monitors}
def fingerprint(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def migrate(data,from_version,to_version):
 out=dict(data);out['schema_version']=to_version;out['migrated_from']=from_version;return out
def neuroml_subset(data): return {"model":data.get('model'),"parameters":data.get('parameters',{})}
def sonata_nodes_csv(text):
 lines=text.strip().splitlines(); head=lines[0].split(','); return [dict(zip(head,line.split(','))) for line in lines[1:]]
def sonata_edges_csv(text): return sonata_nodes_csv(text)
def nwb_spikes(spikes): return {"spike_times_ms":list(spikes),"format":"NWB-spike-subset"}
def nwb_timeseries(times,values): return {"time_ms":list(times),"values":list(values),"format":"NWB-timeseries-subset"}
