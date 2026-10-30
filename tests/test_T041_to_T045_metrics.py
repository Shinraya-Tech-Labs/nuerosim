import json
from pathlib import Path
from neurosim.analysis_metrics import refractory_comparison, fi_curve, adaptation_metrics, bursts, model_gallery
F=Path(__file__).parent/'fixtures/omega'
def test_T041_refractory_comparison_battery_unit():
 f=json.loads((F/'T041-refractory-comparison-battery/valid.json').read_text()); assert [x['spike_count'] for x in refractory_comparison(f['base'],f['refractory_ms'])]==f['expected_counts']
def test_T042_firing_rate_input_current_curves_unit():
 f=json.loads((F/'T042-firing-rate-input-current-curves/valid.json').read_text()); assert [x['spike_count'] for x in fi_curve(f['base'],f['amplitudes'])]==f['expected_counts']
def test_T043_frequency_adaptation_metrics_unit(): assert adaptation_metrics([1,3,6,10])['adaptation_ratio']==2
def test_T044_burst_detection_metrics_unit(): assert len(bursts([1,3,5,20],3))==1
def test_T045_model_comparison_gallery_unit():
 f=json.loads((F/'T045-model-comparison-gallery/valid.json').read_text()); assert [x['model'] for x in model_gallery(f['configs'])]==f['expected_models']
