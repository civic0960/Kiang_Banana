# Genome Informatics Homework 1
    Markov Model and Hidden Markov Model in Python

## Author
Name : Peng, Hao-Ting(彭皓廷)  
Student ID : P76121495

## Problem 1
計算Markov Model order 0、1、2情況時，generating sequence(NC_000006.12[100,000 - 1,200,000])的機率  
列出此model fit sequence(NC_000006.12[100,000 - 1,200,200])的機率(log base 2)  
底下機率皆已log base 2表示

Result :
- Probability of order 0: -2186074.8514462523
- Probability of order 1: -2138762.2347436263
- Probability of order 2: -2125610.024357469
- Run time: 3.889421100029722 s

## Problem 2
實作Hidden Markov model  
new_s為NC_000007.14[100,000 - 1,200,000]  
初始參數設定
- initial_probability = [0.4, 0.6]
- transition_probability = [[0.65, 0.35], [0.25, 0.75]]
- emission_probability = [[0.1, 0.2, 0.15, 0.55], [0.4, 0.1, 0.3, 0.2]]
- n_iter = 20 

Result:
- A = [[0.71581425, 0.28418575], [0.21199861, 0.78800139]]
- B = [[0.11433548, 0.33673729, 0.10194746, 0.44697977], [0.41341841, 0.12929801, 0.30114849, 0.15613508]]
- HMM run time 420.22919879993424 s
- HMM observation probability for S : -2171777.827432846
- HMM observation probability for new_S (use parameters from S): -2216733.1200483264

嘗試更改參數設定以尋找最佳的參數
- initial_probability = [0.6, 0.4]
- transition_probability = [[0.7, 0.3], [0.2, 0.8]]
- emission_probability = [[0.1, 0.2, 0.2, 0.5], [0.5, 0.1, 0.2, 0.2]]
- n_iter = 20 

Result:
- A = [[0.75738426, 0.24261574], [0.19072137, 0.80927863]]
- B = [[0.11790304, 0.31050476, 0.12999975, 0.44159245], [0.41748635, 0.14515301, 0.28367367, 0.15368698]]
- HMM run time 441.97530549997464 s
- HMM observation probability for S : -2171753.4056057176
- HMM observation probability for new_S (use parameters from S): -2217586.148820572

嘗試更改參數設定以尋找最佳的參數
- initial_probability = [0.4, 0.6]
- transition_probability = [[0.6, 0.4], [0.3, 0.7]]
- emission_probability = [[0.15, 0.15, 0.3, 0.4], [0.4, 0.2, 0.2, 0.2]]
- n_iter = 20 

Result:
- A = [[0.67837774, 0.32162226], [0.25172647, 0.74827353]]
- B = [[0.09196903, 0.19216037, 0.24585223, 0.47001837], [0.43720939, 0.23809613, 0.19270333, 0.13199115]]
- HMM run time 459.0996639999794 s
- HMM observation probability for S : -2177269.317238166
- HMM observation probability for new_S (use parameters from S): -2224655.292037804

Total run time : 500.29267740016803 s  
Total memory usage 9163567 bytes