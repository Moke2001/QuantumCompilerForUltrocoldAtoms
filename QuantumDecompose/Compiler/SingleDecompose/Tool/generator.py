import numpy as np


def generator(theta, n):
    [n_x, n_y, n_z] = n
    I = np.array([[1, 0], [0, 1]], dtype=complex)
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    moment = np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * (n_x * sigma_x + n_y * sigma_y + n_z * sigma_z)
    return moment