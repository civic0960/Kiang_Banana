from pyfaidx import Fasta
from guppy import hpy
import numpy as np
import Markov
import Hidden_Markov

if __name__ == "__main__":
    hxx = hpy()
    hxx_status1 = hxx.heap()
    # 讀取'GRCh38_latest_genomic.fna'
    genes = Fasta('GRCh38_latest_genomic.fna')
    # 提取NC_000006.12內100,000 ~ 1,200,000
    S = genes['NC_000006.12'][100000:1200000]
    # 將S內的字符轉為小寫
    S = str(S)
    S = S.lower()
    # 將S內的字符中的n移除
    S = S.replace('n', '')
    S = list(S)

    # 初始參數
    initial_probability = np.array((0.4, 0.6))
    # 初始transition_probability
    transition_probability = np.array([[0.6, 0.4], [0.3, 0.7]])
    # 初始emission_probability
    # (a, c, g, t)
    emission_probability = np.array([[0.15, 0.15, 0.3, 0.4], [0.4, 0.2, 0.2, 0.2]])
    # Markov total run time
    m_time = 0

    # Problem 1
    # Plain Markov Model
    for order in range(3):
        markov_model_probability, log2_p, g_time = Markov.Markov(S, order)
        m_time += g_time
        print(f"Run time: {g_time}")
        print(f"Probability of order {order}(log base 2): {log2_p}")
    print(f"Markov total run time {m_time} s")

    # Problem 2.1
    S = Hidden_Markov.translation(S)
    # Baum-Welch 訓練次數 
    n_iter = 20
    # a_model: 訓練出的transition_probability
    # b_model: 訓練出的emission_probability
    a_model, b_model, runHMM_time = Hidden_Markov.Baum_Welch(S.copy(), initial_probability.copy(), transition_probability.copy(), emission_probability.copy(), n_iter)
    print(f'A: {a_model} B: {b_model}')
    print(f"HMM run time {runHMM_time} s")
    print(f"HMM observation probability for S : {Hidden_Markov.forward(S, initial_probability, a_model, b_model)[1]}")

    # Problem 2.2
    # 提取NC_000007.14內100,000 ~ 1,200,000
    new_S = genes["NC_000007.14"][100000:1200000]
    new_S = str(new_S)
    new_S = new_S.lower()
    new_S = new_S.replace("n", "")
    new_S = list(new_S)
    new_S = Hidden_Markov.translation(new_S)
    print(f"HMM observation probability for new_S (use parameters from S): {Hidden_Markov.forward(new_S, initial_probability, a_model, b_model)[1]}")
    print(f"Total run time {m_time + runHMM_time} s")
    hxx_status2 = hxx.heap()
    print(f"Memory usage {hxx_status2.size - hxx_status1.size} bytes")