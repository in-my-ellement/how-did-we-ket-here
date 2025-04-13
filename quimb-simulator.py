import numpy as np
import quimb.tensor as qtn
import re
import math

file_name = "P1_little_peak.qasm"
num_qubits = 4

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
qc = qtn.CircuitMPS.from_gates(gates)
prob = np.array([0] * num_qubits)
for b in qc.sample(20, seed=43): 
    prob += np.array([int(n) for n in list(b)])

print("".join(str(round(n)) for n in prob / 20))