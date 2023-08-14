import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from util_hypothesis_tests import *



folders = ["csv/aligned/c8_orb_stereo", "csv/aligned/c8_orb_d435"]
folder_save = "/mnt/c/Users/Daniel/Studium_AI_Engineering/0_Masterarbeit/Latex/results/"
alpha = 0.05
print_every = False
precision = 6

test_name = "mwu"
col_name = 'dist'
df_latex, df_pvalues_latex = make_tables_from_experiment(folder_save, test_name, col_name, folders, alpha, precision=6, print_every=print_every)

test_name = "kolmogorov"
col_name = 'dist'
df_latex, df_pvalues_latex = make_tables_from_experiment(folder_save, test_name, col_name, folders, alpha, precision=6, print_every=print_every)

test_name = "mwu"
col_name = 'ffd'
df_latex, df_pvalues_latex = make_tables_from_experiment(folder_save, test_name, col_name, folders, alpha, precision=6, print_every=print_every)

test_name = "kolmogorov"
col_name = 'ffd'
df_latex, df_pvalues_latex = make_tables_from_experiment(folder_save, test_name, col_name, folders, alpha, precision=6, print_every=print_every)