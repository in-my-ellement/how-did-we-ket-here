from qiskit import QuantumCircuit, transpile
import matplotlib.pyplot as plt

# import the qasm file and convert it to a qiskit circuit
qc = QuantumCircuit.from_qasm_file("P1_little_peak.qasm")
qc.measure_all()
qc.draw("mpl")
plt.show()

# simulate the circuit
from qiskit_aer import AerSimulator
sim = AerSimulator()
result = sim.run(transpile(qc, sim)).result()

# plot the results
from qiskit.visualization import plot_histogram
counts = result.get_counts(qc)
plot_histogram(counts, title='bitstrings')
plt.show()