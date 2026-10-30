import json
from pathlib import Path
import pytest
from neurosim.synapse_metrics import exponential_event, alpha_event, synaptic_current
F=Path(__file__).resolve().parent/'fixtures/omega'
def test_T046_exponential_excitatory_synapse_unit():
 f=json.loads((F/'T046-exponential-excitatory-synapses/valid.json').read_text()); assert exponential_event(f['weight'],f['time_ms'],f['tau_ms'])==pytest.approx(f['expected_conductance'])
def test_T047_exponential_inhibitory_synapse_unit():
 f=json.loads((F/'T047-exponential-inhibitory-synapses/valid.json').read_text()); assert synaptic_current(exponential_event(f['weight'],f['time_ms'],f['tau_ms']),f['voltage_mV'],-80)==pytest.approx(f['expected_current'])
def test_T048_alpha_function_synapse_unit():
 f=json.loads((F/'T048-alpha-function-synapses/valid.json').read_text()); assert alpha_event(f['weight'],f['time_ms'],f['tau_ms'])==pytest.approx(f['expected_conductance'])
def test_T049_conductance_excitatory_event_unit():
 f=json.loads((F/'T049-conductance-based-excitatory-event/valid.json').read_text()); assert synaptic_current(f['conductance'],f['voltage_mV'],0)==f['expected_current']
def test_T050_conductance_inhibitory_event_unit():
 f=json.loads((F/'T050-conductance-based-inhibitory-event/valid.json').read_text()); assert synaptic_current(f['conductance'],f['voltage_mV'],-80)==f['expected_current']
