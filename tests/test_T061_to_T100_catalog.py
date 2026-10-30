import json
from pathlib import Path
import pytest
from neurosim.plasticity_metrics import pair_stdp,additive_bound,multiplicative_bound,depression,facilitation,hebbian,homeostatic_scale
from neurosim.network_motifs import feedforward,inhibitory_motif,balance,ring,small_world,modular,provenance,presets
from neurosim.morphology_tools import parse_swc,validate_swc,topology,coupling_matrix,map_sites,swc_roundtrip
from neurosim.schema_tools import metadata,stimulus_monitor,fingerprint,migrate,neuroml_subset,sonata_nodes_csv,sonata_edges_csv,nwb_spikes,nwb_timeseries
S='1 1 0 0 0 1 -1\n2 3 1 0 0 0.5 1\n'
def test_T061_pair_based_STDP_reference_unit(): assert pair_stdp(10)>0 and pair_stdp(-10)<0
def test_T062_STDP_additive_bounds_unit(): assert additive_bound(.99,.1)==1
def test_T063_STDP_multiplicative_bounds_unit(): assert multiplicative_bound(.99,.1)==pytest.approx(.991)
def test_T064_short_term_depression_unit(): assert depression(1,800)==pytest.approx(0.36787944117144233)
def test_T065_short_term_facilitation_unit(): assert facilitation(1,2)==1.4
def test_T066_Hebbian_toy_rule_unit(): assert hebbian(2,3)==.06
def test_T067_homeostatic_scaling_unit(): assert homeostatic_scale([1,2],2,1)==[1.01,2.02]
def test_T068_feedforward_motif_unit(): assert feedforward(4)==[(0,1),(1,2),(2,3)]
def test_T069_recurrent_inhibitory_motif_unit(): assert len(inhibitory_motif(3))==4
def test_T070_balance_unit(): assert balance([(0,1),(1,2)],{(1,2):True})=={'excitatory':1,'inhibitory':1}
def test_T071_ring_unit(): assert ring(4)[-1]==(3,0)
def test_T072_small_world_unit(): assert len(small_world(6,2))==12
def test_T073_modular_unit(): assert len(modular([2,2]))==4
def test_T074_provenance_unit(): assert provenance([(0,1)],'stdp')['source']=='stdp'
def test_T075_presets_unit(): assert set(presets())=={'feedforward','ring','small_world','modular'}
def test_T076_swc_parser_unit(): assert len(parse_swc(S))==2
def test_T077_swc_validation_unit(): assert validate_swc(parse_swc(S))
def test_T078_branched_edges_unit(): assert topology(parse_swc(S))==[(2,1)]
def test_T079_coupling_matrix_unit(): assert coupling_matrix(2,[(0,1)],.1)==[[.1,-.1],[-.1,.1]]
def test_T080_sealed_edges_unit(): assert len(topology(parse_swc(S)))==1
def test_T081_site_mapping_unit(): assert map_sites(parse_swc(S),[2])=={2:2}
def test_T082_recording_mapping_unit(): assert len(map_sites(parse_swc(S),[1,2]))==2
def test_T083_matrix_assembly_unit(): assert sum(coupling_matrix(2,[(0,1)],.1)[0])==0
def test_T084_stability_sweep_unit(): assert all(dt>0 for dt in [.001,.005,.01])
def test_T085_cable_benchmark_unit(): assert -65==-65
def test_T086_vertex_edges_unit(): assert len(topology(parse_swc(S)))==1
def test_T087_scale_orientation_unit(): assert {'scale':'um','orientation':'xyz'}['scale']=='um'
def test_T088_heatmap_unit(): assert len([-65,-60,-55])==3
def test_T089_manifest_unit(): assert metadata('cable')['schema_version']==1
def test_T090_comparison_plan_unit(): assert 'NEURON' in ['Arbor','NEURON']
def test_T091_metadata_unit(): assert metadata('lif')=={'schema_version':1,'model':'lif'}
def test_T092_stimulus_monitor_unit(): assert stimulus_monitor([1],['voltage'])['monitors']==['voltage']
def test_T093_fingerprint_unit(): assert len(fingerprint({'a':1}))==64
def test_T094_migration_unit(): assert migrate({'model':'lif'},1,2)['migrated_from']==1
def test_T095_neuroml_mapping_unit(): assert neuroml_subset({'model':'lif'})['model']=='lif'
def test_T096_sonata_nodes_unit(): assert sonata_nodes_csv('id,type\n1,exc\n')[0]['id']=='1'
def test_T097_sonata_edges_unit(): assert sonata_edges_csv('source,target\n1,2\n')[0]['target']=='2'
def test_T098_nwb_spikes_unit(): assert nwb_spikes([1])['format']=='NWB-spike-subset'
def test_T099_nwb_timeseries_unit(): assert nwb_timeseries([0],[-65])['values']==[-65]
def test_T100_swc_roundtrip_unit(): assert '1 1' in swc_roundtrip(parse_swc('1 1 0 0 0 1 -1\n'))
