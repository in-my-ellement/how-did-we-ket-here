import time
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from qiskit_aer import StatevectorSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import env
import bluequbit

def run_local_sim(filename):
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()
    sim = AerSimulator()
    tqc = transpile(qc)
    start = time.time()
    result = sim.run(tqc).result()
    end = time.time()
    return end - start

def run_blue_sim(filename):
    bq = bluequbit.init(env.bluetoken)
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()
    start = time.time()
    # options = {
    #     'mps_bond_dimension': 32,  # Adjust based on available RAM
    #     'mps_truncation_threshold': 1e-16,
    # }
    result = bq.run(qc, device="mps.cpu")  # Already returns a JobResult
    counts = result.get_counts()
    # sort counts by value
    end = time.time()
    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    print(counts)
    return end - start

def statevector(filename):
    qc = QuantumCircuit.from_qasm_file(filename)
    cut_pass = CutQubits([24])  # Cut at qubit 24 (middle of the circuit)
    cut_circuits = cut_pass.run(qc)
    sim = AerSimulator()
    sampler = SamplerV2(sim)
    qc.save_statevector('final')
    qc.measure_all()
    sim = AerSimulator(method='statevector', device='GPU')
    qc_opt = transpile(qc, sim, optimization_level=3)
    result = sim.run(qc_opt, shots=512).result()
    counts = result.get_counts()
    # sort counts by value
    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    print(counts)
    plt.show()

# run_blue_sim("P4_golden_mountain.qasm")

# # QASM files to compare
files = ["P1_little_peak.qasm", "P2_swift_rise.qasm"]
pfiles = ["P1_little_peak.qasm", "P2_swift_rise.qasm", "P3_sharp_peak.qasm"]

# Collect runtimes
local_runtimes = [run_local_sim(f) for f in files]
blue_runtimes = [run_blue_sim(f) for f in pfiles]

# Plot as line graph
plt.figure(figsize=(9, 5))
plt.plot(files, local_runtimes, marker='o', label='Local (AerSimulator)', color='skyblue')
plt.plot(pfiles, blue_runtimes, marker='s', label='BlueQubit (mps.cpu)', color='salmon')
plt.yscale('log')
plt.ylabel("Runtime (log scale, seconds)")
plt.title("Local vs BlueQubit QASM Simulation Runtime")
plt.grid(axis='y', which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
