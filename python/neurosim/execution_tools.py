"""Deterministic execution, sweep, result and progress helpers."""
import hashlib,json,random,time
def parse_v2(data):
 out=dict(data); out["schema_version"]=2; return out
def validate_input(data,required=()):
 missing=[k for k in required if k not in data]
 if missing: raise ValueError('missing required fields: '+','.join(missing))
 return True
def quota(steps,limit):
 if steps>limit: raise ValueError('quota exceeded')
 return {"steps":steps,"limit":limit}
def progress_events(total): return [{"step":i,"fraction":i/total if total else 1} for i in range(total+1)]
def cancellation(flag): return bool(flag)
def queue_state(items): return {"pending":len(items),"items":list(items)}
def grid_sweep(values): return [{"value":v} for v in values]
def random_sweep(seed,count,low=0,high=1):
 r=random.Random(seed); return [r.uniform(low,high) for _ in range(count)]
def assign_seeds(base,count): return [base+i for i in range(count)]
def aggregate(values): return {"count":len(values),"mean":sum(values)/len(values) if values else None,"min":min(values) if values else None,"max":max(values) if values else None}
def manifest_hash(manifest): return hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate_archive(manifests): return all('config' in m and 'schema_version' in m for m in manifests)
def profile_sections(sections): return {k:sum(v) for k,v in sections.items()}
def chunk(values,size): return [values[i:i+size] for i in range(0,len(values),size)]
