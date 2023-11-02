from collections import Counter
import math
import time


def Markov(sequence, order) -> (dict, float, float):
    # 實現Markov models of any order
    M_time = time.perf_counter()
    prob = {}
    log_p = 0
    for i in range(len(sequence) - order):
        text = str(sequence[i:i + order])
        next_char = str(sequence[i + order])
        if text not in prob:
            prob[text] = Counter()
        prob[text][next_char] += 1
    # 計算Markov model probability
    for text, next_chars in prob.items():
        total_count = (sum(next_chars.values()))
        prob[text] = {char: count / total_count for char, count in next_chars.items()}

    # 計算log base 2 probability
    for i in range(len(sequence) - order):
        text = str(sequence[i:i + order])
        next_char = str(sequence[i + order])
        log_p += math.log2(prob[text][next_char])
    run_time = time.perf_counter() - M_time

    return prob, log_p, run_time
