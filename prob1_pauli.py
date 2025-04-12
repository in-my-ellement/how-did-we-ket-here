import numpy as np
import math

def calcBit(calc_state):
    return np.abs(calc_state[0, 0])**2 < np.abs(calc_state[1, 0])**2

I = np.array([[1, 0],
              [0, 1]], dtype=complex)

sigma_x = np.array([[0, 1],
                    [1, 0]])

sigma_y = np.array([[0, -1j],
                    [1j,  0]], dtype=complex)

sigma_z = np.array([[1, 0],
                    [0, -1]], dtype=complex)

def Rx(θ):
    return np.cos(theta/2) * I - 1j * np.sin(theta/2) * sigma_x

def Ry(θ):
    return np.cos(θ/2) * I - 1j * np.sin(θ/2) * sigma_y

def Rz(θ):
    return np.cos(θ/2) * I - 1j * np.sin(θ/2) * sigma_z
    
gates = np.array([
    [Ry(0.8 * np.pi)],
    [sigma_x, Ry(0.8 * np.pi)],
    [sigma_x, Ry(0.8 * np.pi)],
    [Ry(0.8 * np.pi)]
], dtype=object)

ket_zero = np.array([[1],
                     [0]], dtype=complex)
ket_one = np.array([[0],
                    [1]], dtype=complex)

bits = []

for i in range(0, 4):
    state = ket_zero
    for j in gates[i]:
        state = np.dot(j, state)
    bits.append(int(calcBit(state)))

print("Final state:")
print(bits)
