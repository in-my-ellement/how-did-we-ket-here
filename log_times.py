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
import quimb_simulator

def run_local_sim(filename):
    start = time.time()
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()
    sim = AerSimulator()
    tqc = transpile(qc)
    result = sim.run(tqc).result()
    end = time.time()
    return end - start

def run_blue_sim(filename):
    
    start = time.time()

    bq = bluequbit.init(env.bluetoken)
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()
    
    result = bq.run(qc, device="mps.cpu")
    counts = result.get_counts()
    end = time.time()

    # Sort and keep only the top 10 most common results
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20])

    print(sorted_counts)

    return end - start

def quimb_sim(filename, num_qubits=48):
    start = time.time()
    result = quimb_simulator.calc(filename, num_qubits)
    print(result)
    end = time.time()
    return end - start

# # QASM files to compare
files = ["P1_little_peak.qasm", "P2_swift_rise.qasm"]
pfiles = ["P1_little_peak.qasm", "P2_swift_rise.qasm", "P3_sharp_peak.qasm"]
qfiles = ["P1_little_peak.qasm", "P2_swift_rise.qasm", "P3_sharp_peak.qasm"]

# # Collect runtimes
local_runtimes = [run_local_sim(f) for f in files]
blue_runtimes = [run_blue_sim(f) for f in pfiles]
quimb_runtimes = [quimb_sim(f) for f in qfiles]

# # Plot as line graph
plt.figure(figsize=(9, 5))
plt.plot(files, local_runtimes, marker='o', label='Local (AerSimulator)', color='skyblue')
plt.plot(pfiles, blue_runtimes, marker='s', label='BlueQubit (mps.cpu)', color='salmon')
plt.plot(qfiles, quimb_runtimes, marker='s', label='Quimb', color='teal')
plt.yscale('log')
plt.ylabel("Runtime (log scale, seconds)")
plt.title("Runtime Comparisons of various different quantum algorithms")
plt.grid(axis='y', which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
