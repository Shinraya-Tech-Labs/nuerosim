"""Interoperability provenance and reference-harness helpers."""
import csv,io,json,hashlib
def license_provenance(name,license_text,source): return {"name":name,"license":license_text,"source":source}
def loss_report(source,target,losses=None): return {"source":source,"target":target,"losses":losses or []}
def registry(entries): return {e["name"]:e for e in entries}
def example(model,config): return {"model":model,"config":config,"format":"neurosim-example-v1"}
def integration_suite(cases): return {"case_count":len(cases),"cases":cases}
def reference_setup(simulator,scope): return {"simulator":simulator,"scope":scope,"status":"optional"}
def tolerance_matrix(values, tolerances): return [{"value":v,"tolerance":t} for v in values for t in tolerances]
def match_spikes(a,b,tolerance): return all(abs(x-y)<=tolerance + 1e-12 for x,y in zip(a,b)) and len(a)==len(b)
def rms_error(a,b): return (sum((x-y)**2 for x,y in zip(a,b))/len(a))**.5 if a else 0
def discrepancy(label,expected,actual): return {"label":label,"expected":expected,"actual":actual,"delta":actual-expected}
def seed_policy(base,count): return [base+i for i in range(count)]
def benchmark_report(name,results): return {"name":name,"results":results,"count":len(results)}
