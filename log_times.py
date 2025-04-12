import time
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def run_simulation(filename):
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()

    sim = AerSimulator()  # You could also use: AerSimulator(method='statevector')
    
    # Avoid targeting a backend that can't handle large qubit counts
    tqc = transpile(qc)  # no backend passed
    start_time = time.time()
    result = sim.run(tqc).result()
    end_time = time.time()

    return end_time - start_time

# List of QASM files
files = ["P1_little_peak.qasm", "P2_swift_rise.qasm", "P3_sharp_peak.qasm"]
runtimes = [run_simulation(f) for f in files]

# Plotting
# Logarithmic bar plot
plt.figure(figsize=(8, 5))
plt.bar(files, runtimes, color=['skyblue', 'salmon'])
plt.yscale('log')  # 🔁 this is the key line
plt.ylabel("Runtime (log scale, seconds)")
plt.title("QASM Simulation Runtime Comparison (Log Scale)")
plt.grid(axis='y', which='both', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()