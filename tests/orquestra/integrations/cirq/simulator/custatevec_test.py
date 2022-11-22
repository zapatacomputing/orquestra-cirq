################################################################################
# © Copyright 2021-2022 Zapata Computing Inc.
################################################################################
import numpy as np
import pytest
from cirq import depolarize
from orquestra.quantum.api.circuit_runner_contracts import (
    CIRCUIT_RUNNER_CONTRACTS,
    STRICT_CIRCUIT_RUNNER_CONTRACTS,
)
from orquestra.quantum.api.wavefunction_simulator_contracts import (
    simulator_contracts_for_tolerance,
)
from orquestra.quantum.circuits import CNOT, Circuit, H, X
from orquestra.quantum.operators import PauliSum

from orquestra.integrations.custatevec.simulator import CuStateVecSimulator


@pytest.fixture()
def simulator():
    return CuStateVecSimulator()


@pytest.mark.custatevec
class TestCirqBasedSimulator:
    def test_setup_basic_simulators(self):
        assert isinstance(simulator, CuStateVecSimulator)
        assert simulator.noise_model is None

    def test_run_and_measure(self):
        # Given
        runner = CuStateVecSimulator()
        circuit = Circuit([X(0), CNOT(1, 2)])
        measurements = runner.run_and_measure(circuit, n_samples=100)
        assert len(measurements.bitstrings) == 100

        for measurement in measurements.bitstrings:
            assert measurement == (1, 0, 0)

    def test_measuring_inactive_qubits(self):

        runner = CuStateVecSimulator()
        # Given
        circuit = Circuit([X(0), CNOT(1, 2)], n_qubits=4)

        measurements = runner.run_and_measure(circuit, n_samples=100)
        assert len(measurements.bitstrings) == 100

        for measurement in measurements.bitstrings:
            assert measurement == (1, 0, 0, 0)

    def test_run_batch_and_measure(self):

        runner = CuStateVecSimulator()
        # Given
        circuit = Circuit([X(0), CNOT(1, 2)])
        n_circuits = 5
        n_samples = 100
        # When
        measurements_set = runner.run_batch_and_measure(
            [circuit] * n_circuits, n_samples=[100] * n_circuits
        )
        # Then
        assert len(measurements_set) == n_circuits
        for measurements in measurements_set:
            assert len(measurements.bitstrings) == n_samples
            for measurement in measurements.bitstrings:
                assert measurement == (1, 0, 0)

    def test_run_circuit_and_measure_seed(self):
        # Given
        circuit = Circuit([X(0), CNOT(1, 2)])
        simulator1 = CuStateVecSimulator(seed=12)
        simulator2 = CuStateVecSimulator(seed=12)

        # When
        measurements1 = simulator1.run_and_measure(circuit, n_samples=1000)
        measurements2 = simulator2.run_and_measure(circuit, n_samples=1000)

        # Then
        for (meas1, meas2) in zip(measurements1.bitstrings, measurements2.bitstrings):
            assert meas1 == meas2

    def test_get_wavefunction(self):
        runner = CuStateVecSimulator()
        # Given
        circuit = Circuit([H(0), CNOT(0, 1), CNOT(1, 2)])

        # When
        wavefunction = runner.get_wavefunction(circuit)
        # Then
        assert isinstance(wavefunction.amplitudes, np.ndarray)
        assert len(wavefunction.amplitudes) == 8
        assert np.isclose(
            wavefunction.amplitudes[0], (1 / np.sqrt(2) + 0j), atol=10e-15
        )
        assert np.isclose(
            wavefunction.amplitudes[7], (1 / np.sqrt(2) + 0j), atol=10e-15
        )

    def test_get_noisy_exact_expectation_values(self):
        # Given
        noise = 0.0002
        noise_model = depolarize(p=noise)
        runner = CuStateVecSimulator(noise_model=noise_model)
        circuit = Circuit([H(0), CNOT(0, 1), CNOT(1, 2)])
        qubit_operator = PauliSum("-1*Z0*Z1 + X0*X2")
        target_values = np.array([-0.9986673775881747, 0.0])

        expectation_values = runner.get_exact_noisy_expectation_values(
            circuit, qubit_operator
        )
        np.testing.assert_almost_equal(
            expectation_values.values[0], target_values[0], 2
        )
        np.testing.assert_almost_equal(expectation_values.values[1], target_values[1])


@pytest.mark.custatevec
@pytest.mark.parametrize("contract", CIRCUIT_RUNNER_CONTRACTS)
def test_cirq_runner_fulfills_circuit_runner_contracts(contract):
    runner = CuStateVecSimulator()
    assert contract(runner)


@pytest.mark.custatevec
@pytest.mark.parametrize("contract", simulator_contracts_for_tolerance())
def test_cirq_simulator_fulfills_simulator_contracts(simulator, contract):
    runner = CuStateVecSimulator()
    assert contract(runner)


@pytest.mark.custatevec
@pytest.mark.parametrize("contract", STRICT_CIRCUIT_RUNNER_CONTRACTS)
def test_cirq_simulator_fulfills_strict_circuit_runnner(simulator, contract):
    runner = CuStateVecSimulator()
    assert contract(runner)