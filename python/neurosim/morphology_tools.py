"""Minimal SWC and passive morphology utilities."""
def parse_swc(text):
 rows=[]
 for line in text.splitlines():
  line=line.strip()
  if not line or line.startswith('#'): continue
  fields=line.split()
  if len(fields)!=7: raise ValueError('SWC rows require seven fields')
  rows.append(tuple(float(x) if i else int(x) for i,x in enumerate(fields)))
 return rows
def validate_swc(rows):
 ids={r[0] for r in rows}
 if any(r[6] not in (-1,0) and r[6] not in ids for r in rows): raise ValueError('SWC parent missing')
 return len(rows)>0
def topology(rows): return [(int(r[0]),int(r[6])) for r in rows if r[6] not in (-1,0)]
def passive_edges(rows): return topology(rows)
def coupling_matrix(n,edges,g):
 m=[[0.0]*n for _ in range(n)]
 for i,j in edges: m[i][i]+=g;m[j][j]+=g;m[i][j]-=g;m[j][i]-=g
 return m
def map_sites(rows,ids): return {site:next((r[0] for r in rows if r[0]==site),None) for site in ids}
def swc_roundtrip(rows): return '\n'.join(' '.join(str(x) for x in r) for r in rows)+'\n'
