import time
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


# import bluequbit
# from bluequbit.library import multi_adder

def run_local_sim(filename):
    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()

    sim = AerSimulator()
    tqc = transpile(qc)
    start = time.time()
    result = sim.run(tqc).result()
    end = time.time()
    return end - start

def run_blue_sim(filename, token):
    bq = bluequbit.init(token)

    qc = QuantumCircuit.from_qasm_file(filename)
    qc.measure_all()

    start = time.time()
    job = bq.run(qc)
    result = job.result()  # Waits for completion
    end = time.time()
    return end - start

run_blue_sim("P1_little_peak.qasm")

# files = ["P1_little_peak.qasm", "P2_swift_rise.qasm"]
# runtimes = [run_simulation(f) for f in files]

# plt.figure(figsize=(8, 5))
# plt.bar(files, runtimes, color=['skyblue', 'salmon'])
# plt.yscale('log')  
# plt.ylabel("Runtime (log scale, seconds)")
# plt.title("QASM Simulation Runtime Comparison (Log Scale)")
# plt.grid(axis='y', which='both', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()

