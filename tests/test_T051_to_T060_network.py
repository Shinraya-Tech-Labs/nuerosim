import json
from pathlib import Path
import pytest
from neurosim.network_diagnostics import delay_roundtrip,tie_order,directed_edges,superpose,recurrent_summary,sparse_summary,inspect_synapses,benchmark_events
from neurosim.synapse_metrics import synaptic_current
F=Path(__file__).parent/'fixtures/omega'
def test_T051_synaptic_delay_roundtrip_unit():
 f=json.loads((F/'T051-synaptic-delay-roundtrip/valid.json').read_text());r=delay_roundtrip(f['delay_ms'],f['dt_ms']);assert r['steps']==f['expected_steps'];assert r['effective_delay_ms']==pytest.approx(f['expected_effective_delay_ms'])
def test_T052_event_ordering_deterministic_tie_unit():
 f=json.loads((F/'T052-event-ordering-deterministic-tie/valid.json').read_text());assert tie_order(f['events'])==f['expected_source_order']
def test_T053_pairwise_directed_connections_unit():
 f=json.loads((F/'T053-pairwise-directed-connections/valid.json').read_text());assert len(directed_edges(f['config']))==f['expected_edge_count']
def test_T054_multi_input_superposition_unit():
 f=json.loads((F/'T054-multi-input-superposition/valid.json').read_text());assert superpose(f['weights'],f['time_ms'],f['tau_ms'])==pytest.approx(f['expected_conductance'])
def test_T055_reversal_potential_unit():
 f=json.loads((F/'T055-reversal-potential-unit-tests/valid.json').read_text());assert synaptic_current(f['conductance'],f['voltage_mV'],0)==f['expected_excitatory_current'];assert synaptic_current(f['conductance'],f['voltage_mV'],-80)==f['expected_inhibitory_current']
def test_T056_recurrent_network_scheduler_unit():
 f=json.loads((F/'T056-recurrent-network-scheduler/valid.json').read_text());assert recurrent_summary(f['config'])['edge_count']>0
def test_T057_sparse_adjacency_representation_unit():
 f=json.loads((F/'T057-sparse-adjacency-representation/valid.json').read_text());assert sparse_summary(f['config'])['edge_count']==f['expected_edge_count']
def test_T058_synapse_inspector_api_unit():
 f=json.loads((F/'T058-synapse-inspector-api/valid.json').read_text());assert len(inspect_synapses(f['config']))==f['expected_edge_count']
def test_T059_synapse_visualization_tests_unit():
 f=json.loads((F/'T059-synapse-visualization-tests/valid.json').read_text());rows=inspect_synapses(f['config']);assert all(x['source']!=x['target'] for x in rows)
def test_T060_synapse_benchmarks_unit():
 f=json.loads((F/'T060-synapse-benchmarks/valid.json').read_text());assert benchmark_events(f['count'])['checksum']==pytest.approx(f['expected_checksum'])

def test_T051_delay_rejects_zero_step():
 with pytest.raises(ValueError): delay_roundtrip(0,0)
def test_T052_empty_tie_is_deterministic(): assert tie_order([])==[]
def test_T053_self_edges_are_excluded(): assert all(s!=t for s,t,_ in directed_edges({'model':'lif','n':3,'probability':1,'pulses':[]}))
def test_T054_empty_superposition_is_zero(): assert superpose([],5)==0
def test_T055_reversal_signs_are_opposite(): assert synaptic_current(.02,-65,0)>0 and synaptic_current(.02,-65,-80)<0
def test_T056_recurrent_summary_is_manifest_backed(): assert 'manifest' in recurrent_summary({'model':'lif','n':2,'duration':1,'dt':.025,'pulses':[]})
def test_T057_sparse_summary_has_edges(): assert sparse_summary({'model':'lif','n':3,'probability':1,'pulses':[]})['edge_count']==6
def test_T058_inspector_fields_are_complete(): assert set(inspect_synapses({'model':'lif','n':2,'probability':1,'pulses':[]})[0])=={'source','target','inhibitory'}
def test_T059_visualization_rows_are_directed(): assert all('source' in row and 'target' in row for row in inspect_synapses({'model':'lif','n':2,'probability':1,'pulses':[]}))
def test_T060_benchmark_rejects_no_work(): assert benchmark_events(0)['checksum']==0
