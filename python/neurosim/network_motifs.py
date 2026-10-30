"""Deterministic graph motifs used by network catalogue tasks."""
def feedforward(n=3): return [(i,i+1) for i in range(n-1)]
def inhibitory_motif(n=3): return [(i,j) for i in range(n) for j in range(n) if i!=j and i%2==0]
def balance(edges,inhibitory): return {"excitatory":sum(not inhibitory.get(e,False) for e in edges),"inhibitory":sum(inhibitory.get(e,False) for e in edges)}
def ring(n): return [(i,(i+1)%n) for i in range(n)]
def small_world(n,k=2): return [(i,(i+j)%n) for i in range(n) for j in range(1,k+1)]
def modular(sizes):
 out=[]; start=0
 for size in sizes: out += [(i,j) for i in range(start,start+size) for j in range(start,start+size) if i!=j]; start+=size
 return out
def provenance(edges,source='generated'): return {"source":source,"edge_count":len(edges),"edges":[list(e) for e in edges]}
def presets(): return {"feedforward":feedforward(),"ring":ring(4),"small_world":small_world(6,2),"modular":modular([2,2])}
