"""Audit production recording times against the configured integration grid."""
import argparse, json, math, sys
from pathlib import Path
from .workbench.config import Experiment
from .workbench.engine import simulate

def audit(data):
    try: c=Experiment.model_validate(data)
    except Exception as e: raise ValueError(f"invalid experiment: {e}") from e
    r=simulate(c); steps=round(c.duration/c.dt); expected=list(range(0,steps+1,c.record_every))
    if not expected or expected[-1]!=steps: expected.append(steps)
    times=[i*c.dt for i in expected]; err=max((abs(a-b) for a,b in zip(r['t'],times)),default=0)
    return {"passed":len(r['t'])==len(times) and err<1e-12,"units":{"time":"ms"},"record_indices":expected,"times_ms":r['t'],"expected_times_ms":times,"max_grid_error_ms":err,"final_time_included":r['t'][-1]==c.duration,"manifest":r['manifest']}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('fixture');p.add_argument('--output');a=p.parse_args(argv)
    try:
        f=json.loads(Path(a.fixture).read_text());
        if f.get('units')!={"time":"ms","step":"1"}: raise ValueError('units must be ms and unitless step counts')
        r=audit(f['experiment']); r['passed']=r['passed'] and len(r['times_ms'])==len(f['expected_times_ms']) and all(abs(x-y)<1e-12 for x,y in zip(r['times_ms'],f['expected_times_ms']))
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as e: print(f'error: {e}',file=sys.stderr);return 2
    out=json.dumps(r,indent=2,sort_keys=True);Path(a.output).write_text(out+'\n') if a.output else None;print(out);return 0 if r['passed'] else 1
if __name__=='__main__': raise SystemExit(main())
