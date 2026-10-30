# Solver selection

In **New simulation**, choose **RK4** or **Euler** from the Integrator selector. The selection updates the experiment JSON sent to the existing CPU simulation endpoint. The backend validates solver/model/dt combinations. If the JSON is malformed, correct it in the editor before using the selector.

The selector does not recommend a solver for every scientific use. Compare timestep convergence for the model and question at hand. See the [contract](contracts/T030-solver-selection-ux.md) and the [workbench solver guidance](../SCIENCE.md).
