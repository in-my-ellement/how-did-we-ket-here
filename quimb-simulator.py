import numpy as np
import quimb.tensor as qtn
import re
import math
import itertools as it
import matplotlib.pyplot as plt
from collections import Counter

file_name = "P4_golden_mountain.qasm"
num_qubits = 48

# one line of qasm to quimb gate
def qasm_to_gate(s: str) -> qtn.Gate:
    # my match case statement!
    if s[0] == "x":
        m = re.match(r"x q\[(\d+)\];", s)
        return qtn.Gate("X", params = [], qubits = [int(m[1])])


    match s[0:2]:
        case "sx": 
            m = re.match(r"sx q\w*\[(\d+)\];", s)
            return qtn.Gate("RX", params = [math.pi / 2], qubits = [int(m[1])])
        case "ry":
            t = re.sub(r"pi", "math.pi", s)
            m = re.match(r"ry\((.*)\) q\[(\d+)\];", t)
            return qtn.Gate("RY", params = [float(eval(m[1]))], qubits = [int(m[2])])
        case "rz": 
            m = re.match(r"rz\((-*\d\.\d+)\) q\w*\[(\d+)\];", s)
            return qtn.Gate("RZ", params = [float(m[1])], qubits = [int(m[2])])
        case "cz": 
            m = re.match(r"cz q\w*\[(\d+)\],\s*q\w*\[(\d+)\];", s)
            return qtn.Gate("CZ", params = [], qubits = [int(m[i]) for i in range(1, 3)])
        case "u3": 
            t = re.sub(r"pi", "math.pi", s)
            m = re.match(r"u3\((-*.+),(-*.+),(-*.+)\) q\w*\[(\d+)\];", t)
            return qtn.Gate("U3", params = [float(eval(m[i])) for i in range(1, 4)], qubits = [int(m[4])])
        case _: return "HELP"

# parse the file into a series of quimb gates
gates = []
with open(file_name, "r") as f:
    gates = [[qasm_to_gate(l)] for l in f.readlines()[3:]]

# use the mps simulator from quimb
qc = qtn.CircuitMPS.from_gates(gates, num_qubits, progbar = True, max_bond = 64, cutoff = 1e-4)
prob = np.array([0] * num_qubits)
c = Counter(qc.sample(100))
print(c.most_common(1))

# count results to find the peaks
plt.bar(list(c.keys()), list(c.values()))
plt.xlabel("")
plt.gca().set_xticklabels([])
plt.tight_layout()
plt.show()