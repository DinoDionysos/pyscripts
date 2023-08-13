import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests import *

folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
test_name = "mwu"
col_name = 'dist'
alpha = 0.05
print_every = True
pmean_values, pvalues = mean_hypo(test_name, folders, col_name, alpha, print_every)

column_names = []
for name in folders:
    column_names.append(name.split('/')[-1].split('_',1)[1].replace('_','\_'))
df = pd.DataFrame(pmean_values, columns = column_names, index=column_names)

caption = "mean p values over 20 experiments for the mann whitney u test"
label = "tab:mean_pvalues_mwu"
precision = 6
# df_latex_2 = df.style.to_latex(
#     hrules=True,
#     position_float="centering",
#     caption=caption,
#     label=label)
# with open(folder_save+'result_pmean_2.tex', 'w') as f:
#     f.write(df_latex_2)
# print(df_latex_2)

# take the dataframe df and make a latex table out of it
df_latex = "\centering\n"
df_latex += df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
df_latex = df_latex.replace('-1.' + '0' * precision, '-')
# append the caption and label to the latex table string
df_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
with open(folder_save+'result_pmean.tex', 'w') as f:
    f.write(df_latex)
# print(df_latex)

# take pvalues and make a latex table out of it
caption = "p values for the mann whitney u test"
label = "tab:pvalues_mwu"
precision = 6
pvalues = np.array(pvalues)
df_pvalues = pd.DataFrame()
# for every entry of pvalues, make a new column in the dataframe
for i in range(0, len(pvalues)):
    df_pvalues[str(i)] = pvalues[i]
df_pvalues.columns = ['stereo stereo', 'stereo rgbd', 'rgbd rgbd'] 
# add a row at the bottom with the mean of the pvalues
pmean_values_flat = []
for i in range(0, len(folders)):
    for j in range(0, len(folders)):
        if i < j: 
            break
        pmean_values_flat.append(pmean_values[i][j])
df_pvalues.loc['mean'] = pmean_values_flat
# make another row with if mean is > alpha than say 'rejected' else 'failed to reject'
rejected = df_pvalues.loc['mean'] < alpha
rejected = rejected.replace(True, 'rejected')
rejected = rejected.replace(False, 'failed')
df_pvalues.loc['result'] = rejected

df_pvalues_latex = "\centering\n"
df_pvalues_latex += df_pvalues.to_latex(header=True, float_format=f"%.{precision}f", index=True)
# replace all the occurences of -1 with a dash
df_pvalues_latex = df_pvalues_latex.replace('-1.' + '0' * precision, '-')
df_pvalues_latex = df_pvalues_latex.replace('\nmean &', '\n\midrule\nmean &')
df_pvalues_latex += "\caption{"+caption+"}\n\label{"+label+"}\n"
with open(folder_save+'result_pvalues.tex', 'w') as f:
    f.write(df_pvalues_latex)
print(df_pvalues_latex)

sys.exit(1)