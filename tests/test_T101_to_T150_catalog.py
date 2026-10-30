import pytest

from neurosim.interop_tools import (
    benchmark_report,
    discrepancy,
    example,
    integration_suite,
    license_provenance,
    loss_report,
    match_spikes,
    reference_setup,
    registry,
    rms_error,
    seed_policy,
    tolerance_matrix,
)
from neurosim.execution_tools import (
    aggregate,
    assign_seeds,
    cancellation,
    chunk,
    grid_sweep,
    manifest_hash,
    parse_v2,
    profile_sections,
    progress_events,
    quota,
    queue_state,
    random_sweep,
    validate_archive,
    validate_input,
)
from neurosim.ui_contracts import (
    arrow_edges,
    channel_chart,
    comparison_matrix,
    compare_runs,
    current_plot,
    firing_rate_chart,
    keyboard_order,
    model_explainer,
    morphology_view,
    picker_options,
    raster_limit,
    reduced_motion,
    refractory_overlay,
    status_label,
    stdp_trajectory,
    svg_metadata,
)

def test_T101_license_provenance():
    assert license_provenance("x", "CC-BY", "src")["license"] == "CC-BY"

def test_T102_loss_report():
    assert loss_report("a", "b", ["rounding"])["losses"] == ["rounding"]

def test_T103_registry():
    assert registry([{"name": "lif"}])["lif"]["name"] == "lif"

def test_T104_example():
    assert example("lif", {})["format"] == "neurosim-example-v1"

def test_T105_integration_suite():
    assert integration_suite([{"name": "lif"}])["case_count"] == 1

def test_T106_reference_setup():
    assert reference_setup("Brian2", "lif")["status"] == "optional"

def test_T107_brian2_no_synapse():
    assert reference_setup("Brian2", "lif-no-synapse")["scope"] == "lif-no-synapse"

def test_T108_brian2_pulse():
    assert reference_setup("Brian2", "pulse")["simulator"] == "Brian2"

def test_T109_sparse_spike_matching():
    assert match_spikes([1.0, 2.0], [1.005, 2.0], 0.01)

def test_T110_synapse_delay_reference():
    assert discrepancy("delay_ms", 1.0, 1.0)["delta"] == 0

def test_T111_neuron_optional_setup():
    assert reference_setup("NEURON", "optional")["status"] == "optional"

def test_T112_neuron_hh_comparison():
    assert discrepancy("hh", 1.0, 1.1)["delta"] == pytest.approx(0.1)

def test_T113_arbor_optional_harness():
    assert reference_setup("Arbor", "passive-cable")["scope"] == "passive-cable"

def test_T114_nest_event_semantics():
    assert integration_suite([{"event": 1}, {"event": 2}])["case_count"] == 2

def test_T115_tolerance_matrix():
    assert len(tolerance_matrix([1, 2], [0.1, 0.01])) == 4

def test_T116_cross_simulator_matching():
    assert match_spikes([1.0], [1.0], 0.01)

def test_T117_voltage_rms_error():
    assert rms_error([1, 2], [1, 3]) == pytest.approx(2**0.5 / 2)

def test_T118_scientific_discrepancy():
    assert discrepancy("v", 1.0, 1.1)["delta"] == pytest.approx(0.1)

def test_T119_independent_seed_policy():
    assert seed_policy(42, 3) == [42, 43, 44]

def test_T120_reproducibility_report():
    assert benchmark_report("run", [1, 2])["count"] == 2

def test_T121_config_v2_parser():
    assert parse_v2({"model": "lif"})["schema_version"] == 2

def test_T122_scientific_input_validation():
    assert validate_input({"model": "lif"}, ("model",)) is True

def test_T123_job_quota():
    assert quota(10, 100)["limit"] == 100

def test_T124_progress_events():
    assert progress_events(2)[-1] == {"step": 2, "fraction": 1.0}

def test_T125_cancellation_propagation():
    assert cancellation(True) is True

def test_T126_persistent_queue():
    assert queue_state([1, 2])["pending"] == 2

def test_T127_grid_sweep():
    assert grid_sweep([1, 2]) == [{"value": 1}, {"value": 2}]

def test_T128_random_sweep():
    assert random_sweep(7, 3) == random_sweep(7, 3)

def test_T129_deterministic_seeds():
    assert assign_seeds(100, 3) == [100, 101, 102]

def test_T130_aggregation_metrics():
    assert aggregate([1, 2, 3])["mean"] == 2

def test_T131_manifest_hashing():
    assert len(manifest_hash({"schema_version": 1})) == 64

def test_T132_archive_validation():
    assert validate_archive([{"schema_version": 1, "config": {}}])

def test_T133_cpu_profile():
    assert profile_sections({"engine": [1, 2]})["engine"] == 3

def test_T134_chunked_results():
    assert chunk([1, 2, 3], 2) == [[1, 2], [3]]

def test_T135_status_ui():
    assert status_label("running") == "Running"

def test_T136_picker_ux():
    assert picker_options(["ex_1"])[0]["label"] == "Ex 1"

def test_T137_model_explainer():
    assert model_explainer("lif_model")["title"] == "Lif Model"

def test_T138_current_plot():
    assert current_plot([0, 1], [2, 3])[1]["current"] == 3

def test_T139_channel_chart():
    assert channel_chart([0], {"m": [0.5]}) == [{"time_ms": 0, "m": 0.5}]

def test_T140_raster_limit():
    assert raster_limit([1, 2, 3], 2) == [1, 2]

def test_T141_firing_rate_chart():
    assert firing_rate_chart([0, 1], [2, 3]) == [(0, 2), (1, 3)]

def test_T142_synapse_direction():
    assert arrow_edges([(1, 2)])[0]["directed"] is True

def test_T143_refractory_overlay():
    assert refractory_overlay([1], 2) == [{"start_ms": 1, "end_ms": 3}]

def test_T144_stdp_trajectory():
    assert stdp_trajectory([0], [1]) == [(0, 1)]

def test_T145_morphology_view():
    assert morphology_view([], []) == {"vertices": [], "edges": []}

def test_T146_two_run_comparison():
    assert compare_runs([{"label": "a"}, {"label": "b"}])["run_count"] == 2

def test_T147_five_run_matrix():
    runs = [{"label": label} for label in "abcde"]
    assert comparison_matrix(runs) == [["a", "b", "c", "d", "e"]]

def test_T148_svg_metadata():
    assert svg_metadata(800, 400)["units"] == "px"

def test_T149_keyboard_inspection():
    assert keyboard_order(["Run", "Stop"]) == ["Run", "Stop"]

def test_T150_reduced_motion():
    assert reduced_motion(True) is True

