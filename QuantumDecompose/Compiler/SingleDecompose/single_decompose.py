import numpy as np

from Compiler.SingleDecompose.Tool.Quaternion import Quaternion
from Compiler.SingleDecompose.Tool.generator import generator
from Compiler.SingleDecompose.Tool.judge_phase import judge_phase
from Compiler.SingleDecompose.single_decompose_0 import single_decompose_0, global_arctan


def single_decompose(gate, target):
    gate_vector = single_decompose_0(gate, target)
    alpha = gate_vector[2][1][1]
    beta = gate_vector[0][1][1]
    theta = gate_vector[1][1][1]
    delta = gate_vector[3][1][1]

    q_z_1 = Quaternion([np.cos(alpha / 2), 0, 0, np.sin(alpha / 2)])
    q_y = Quaternion([np.cos(theta / 2), 0, np.sin(theta / 2), 0])
    q_z_0 = Quaternion([np.cos(beta / 2), 0, 0, np.sin(beta / 2)])

    q = q_y * q_z_0
    q = q_z_1 * q
    [theta, [n_x, n_y, n_z]] = q.get_value()

    phi = global_arctan(n_z, np.sqrt(n_x ** 2 + n_y ** 2))
    psi = global_arctan(n_x / np.sin(phi), n_y / np.sin(phi))

    theta_0 = 2 * np.arccos(np.sqrt((np.cos(theta / 2) + 1) / 2) * abs(np.sin(phi)))
    moment=abs((np.cos(theta_0 / 2) ** 2 - np.cos(theta / 2)) / (1 - np.cos(theta_0 / 2) ** 2))
    if moment>1:
        moment=1
    psi_delta_a = np.arccos(moment)
    psi_delta_b = np.pi-psi_delta_a
    psi_delta_c = np.pi + psi_delta_a
    psi_delta_d = 2*np.pi - psi_delta_a
    psi_delta_e = psi_delta_a-np.pi
    psi_delta_f = -psi_delta_a

    psi_0_a = psi + psi_delta_a / 2
    psi_1_a = psi - psi_delta_a / 2

    psi_0_b = psi + psi_delta_b / 2
    psi_1_b = psi - psi_delta_b / 2

    psi_0_c = psi + psi_delta_c / 2
    psi_1_c = psi - psi_delta_c / 2

    psi_0_d = psi + psi_delta_d / 2
    psi_1_d = psi - psi_delta_d / 2

    psi_0_e = psi + psi_delta_e / 2
    psi_1_e = psi - psi_delta_e / 2

    psi_0_f = psi + psi_delta_f / 2
    psi_1_f = psi - psi_delta_f / 2

    G_0_a = generator(theta_0, [np.cos(psi_0_a), np.sin(psi_0_a), 0])
    G_1_a = generator(theta_0, [np.cos(psi_1_a), np.sin(psi_1_a), 0])
    G_0_b = generator(theta_0, [np.cos(psi_0_b), np.sin(psi_0_b), 0])
    G_1_b = generator(theta_0, [np.cos(psi_1_b), np.sin(psi_1_b), 0])
    G_0_c = generator(theta_0, [np.cos(psi_0_c), np.sin(psi_0_c), 0])
    G_1_c = generator(theta_0, [np.cos(psi_1_c), np.sin(psi_1_c), 0])
    G_0_d = generator(theta_0, [np.cos(psi_0_d), np.sin(psi_0_d), 0])
    G_1_d = generator(theta_0, [np.cos(psi_1_d), np.sin(psi_1_d), 0])
    G_0_e = generator(theta_0, [np.cos(psi_0_e), np.sin(psi_0_e), 0])
    G_1_e = generator(theta_0, [np.cos(psi_1_e), np.sin(psi_1_e), 0])
    G_0_f = generator(theta_0, [np.cos(psi_0_f), np.sin(psi_0_f), 0])
    G_1_f = generator(theta_0, [np.cos(psi_1_f), np.sin(psi_1_f), 0])
    G_a = G_1_a @ G_0_a
    G_b = G_1_b @ G_0_b
    G_c = G_1_c @ G_0_c
    G_d = G_1_d @ G_0_d
    G_e = G_1_e @ G_0_e
    G_f = G_1_f @ G_0_f

    if judge_phase(G_a,gate) and judge_phase(gate,G_a):
        psi_0 = psi_0_a
        psi_1 = psi_1_a
    elif judge_phase(G_b,gate) and judge_phase(gate,G_b):
        psi_0 = psi_0_b
        psi_1 = psi_1_b
    elif judge_phase(G_c,gate) and judge_phase(gate,G_c):
        psi_0 = psi_0_c
        psi_1 = psi_1_c
    elif judge_phase(G_d,gate) and judge_phase(gate,G_d):
        psi_0 = psi_0_d
        psi_1 = psi_1_d
    elif judge_phase(G_e,gate) and judge_phase(gate,G_e):
        psi_0 = psi_0_e
        psi_1 = psi_1_e
    else:
        psi_0 = psi_0_f
        psi_1 = psi_1_f

    G_a = generator(theta_0, [np.cos(psi_0), np.sin(psi_0), 0])
    G_b = generator(theta_0, [np.cos(psi_1), np.sin(psi_1), 0])
    G = G_b @ G_a

    correct_real = np.real(gate[0][0] / G[0][0])
    correct_imag = np.imag(gate[0][0] / G[0][0])
    delta_correct = global_arctan(correct_real, correct_imag)

    return ['c',target, theta_0, psi_0], ['c',target, theta_0, psi_1]
