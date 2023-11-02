from sklearn.preprocessing import LabelEncoder
import math
import numpy as np
import time

start_time = time.perf_counter()


def translation(sequence):
    # 將基因體序列轉化方便程式執行
    # a -> 0, c -> 1, g -> 2, t-> 3
    le = LabelEncoder()
    le.fit(["a", "c", "g", "t"])
    sequence = le.transform(sequence)
    return sequence


def forward(o, i_p, A, B):
    # o: observation sequence
    # i_p: initial probability
    # A: transition probability
    # B: emission probability
    l = len(o)
    l_state = len(A)
    alpha = np.zeros((l, l_state))
    scaled_alpha = np.zeros((l, l_state))
    scaling_coefficient = np.zeros(l)
    p = 0

    for t in range(l):
        for state in range(l_state):
            if t == 0:
                alpha[t, state] = i_p[state] * B[state, o[t]]
                # HMM scaling
                scaling_coefficient[t] += alpha[t, state]
            else:
                alpha[t, state] = scaled_alpha[t - 1] @ A[:, state] * B[state, o[t]]
                scaling_coefficient[t] += alpha[t, state]
        scaling_coefficient[t] = 1 / scaling_coefficient[t]
        p += math.log2(scaling_coefficient[t])
        # use scaling to avoid underflow
        scaled_alpha[t, :] = alpha[t, :] * (scaling_coefficient[t])

    return scaled_alpha, -p, scaling_coefficient


def backward(o, A, B, C):
    # C: scaling coefficient
    l = len(o)
    l_state = len(A)
    beta = np.zeros((l, l_state))
    scaled_beta = np.zeros((l, l_state))
    beta[-1] = np.ones(l_state)
    for t in range(l - 1, -1, -1):
        for state in range(l_state):
            if t == l - 1:
                beta[t, state] = 1
                scaled_beta[t, state] = beta[t, state] * C[t]
            else:
                beta[t, state] = (scaled_beta[t + 1] * B[:, o[t + 1]]) @ A[state, :]
                scaled_beta[t, state] = beta[t, state] * C[t]

    return scaled_beta


def Baum_Welch(o, i_p, A, B, n_iter=30):
    #n_iter: 訓練次數
    times = len(o)
    l_state = len(A)

    for _ in range(n_iter):
        print('Computing...')
        # estimation step
        alpha, P, scaling_coefficient = forward(o, i_p, A, B)
        beta = backward(o, A, B, scaling_coefficient)
        # initial xi
        xi = np.zeros((l_state, l_state, times - 1))

        # compute xi
        for t in range(times - 1):
            down = (alpha[t, :].T @ A * B[:, o[t + 1]].T) @ beta[t + 1, :]
            for state in range(l_state):
                up = alpha[t, state] * A[state, :] * B[:, o[t + 1]].T * beta[t + 1, :].T
                xi[state, :, t] = up / down

        # compute gamma
        gamma = np.sum(xi, axis=1)
        # update a -> sum(xi) / sum(gamma)
        A = np.sum(xi, 2) / np.sum(gamma, axis=1).reshape((-1, 1))
        # last Time'th gamma
        gamma = np.hstack((gamma, np.sum(xi[:, :, times - 2], axis=0).reshape((-1, 1))))

        # use gamma to update b
        # K is the number of observation type
        K = B.shape[1]
        down = np.sum(gamma, axis=1)
        for l_type in range(K):
            B[:, l_type] = np.sum(gamma[:, o == l_type], axis=1)
        B = np.divide(B, down.reshape((-1, 1)))
    run_time = time.perf_counter() - start_time
    return A, B, run_time
