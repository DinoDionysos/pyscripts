import pandas as pd

def insert_multicol_at(df, row_content, row_index):
    """inserts a line into a dataframe at the row_index. row_content is a  string and gets wrapped into \multicol"""
    row_content = '\multicolumn{%d}{c}{%s}' % (df.shape[1], row_content)
    df.iloc[row_index, 0] = row_content + '\\\\ %'
    return df


def insert_rule_at(df, row_content, row_index):
    """inserts a line into a dataframe at the row_index. row_content is a  string"""
    df.iloc[row_index, 0] = row_content + ' %'
    return df

def insert_multirow_at(df, row_content, row_index, col_idx, num_rows):
    """inserts a line into a dataframe at the row_index. row_content is a  string and gets wrapped into \multicol"""
    row_content = '\\multirow{%d}{*}{%s}' % (num_rows, row_content)
    df.iloc[row_index, col_idx] = row_content
    return df

def insert_row_at(df, row_content, row_index):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    df.iloc[row_index] = row_content
    return df

def insert_list_at(df, row_content, row_index, col_idx):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    for j in range(0, len(row_content)):
        df.iloc[row_index, col_idx+j] = row_content[j]
    return df

def insert_at(df, content, row_index, col_idx):
    """replaces the row at row_index with row_content list"""
    # replace the row at row_index with row_content
    df.iloc[row_index, col_idx] = content
    return df

len_test_names = 5
len_correlation_names = 1
len_mean_std_column = 1
len_reject_fail_column = 1
len_xy_yaw_rpe_ape_columns = 2


len_test_names = 5
len_correlation_names = 1
len_mean_std_column = 1
len_reject_fail_column = 1
len_xy_yaw_rpe_ape_columns = 2
width_table = len_test_names + len_correlation_names + len_mean_std_column + len_reject_fail_column + len_xy_yaw_rpe_ape_columns

# make a dataframe with 3 columns and 4 rows with '' in each cell
len_rules = 5 - 1 # weil bottomrule schon da ist
len_rows = 11
len_clines = 3

def df_latex_table_template():
    num_rows = len_rows + len_rules + len_clines
    num_cols = width_table
    df = pd.DataFrame([['' for i in range(0, num_cols)] for j in range(0, num_rows)])
    # df = pd.DataFrame() 
    test_names = ["KS2", 'BF', "KW", 'BM', "MWU"]
    correlation_names = ['f']
    line = ['evalution type','', ''] + test_names  + correlation_names + ['']
    # insert a line at row 0
    df = insert_rule_at(df, '\midrule', 2)
    df = insert_row_at(df, line, 3)
    df = insert_rule_at(df, '\midrule', 4)
    df = insert_rule_at(df, '\midrule', 5)
    df = insert_multirow_at(df, 'translational', row_index=6, col_idx=0, num_rows=4)
    df = insert_multirow_at(df, 'APE', row_index=6, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, 'RPE', row_index=9, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, 'rotational', row_index=12, col_idx=0, num_rows=4)
    df = insert_multirow_at(df, 'APE', row_index=12, col_idx=1, num_rows=2)
    df = insert_multirow_at(df, 'RPE', row_index=15, col_idx=1, num_rows=2)
    # line = [1,2,3,4,5]
    # df = insert_list_at(df, line, row_index=6, col_idx=3)
    # line_f = 0.421
    # df = insert_at(df, line_f, row_index=6, col_idx=9)

    for i in range(0, 4):
        df = insert_at(df, 'reject', row_index=6+i*3, col_idx=2)
        df = insert_at(df, 'fail', row_index=7+i*3, col_idx=2)
        df = insert_at(df, 'mean', row_index=6+i*3, col_idx=8)
        df = insert_at(df, 'std', row_index=7+i*3, col_idx=8)

    df = insert_rule_at(df, '\cline{2-%d}'%(num_cols), 8)
    df = insert_rule_at(df, '\cline{1-%d}'%(num_cols), 11)
    df = insert_rule_at(df, '\cline{2-%d}'%(num_cols), 14)
    df = insert_rule_at(df, '\\bottomrule', 17)

    return df

def latex_table_from_df_template(df, caption, label):

    col_format = 'll|lrrrrr|lr'
    df_latex = df.to_latex(index=False,header=False,index_names=False, column_format=col_format, float_format="%.4f")
    #remove the \toprule and \midrule with replace ''
    df_latex = df_latex.replace('\\toprule\n\midrule\n', '')
    # get the number of cols of the df
    num_cols = df.shape[1]
    # create string of form "% &  &  &  &  &  &  &  &  &  \\" with width number of &"
    string_to_replace = ' %' + ' & ' * (num_cols-1) + ' \\\\'
    # replace '' with string_to_replace
    df_latex = df_latex.replace(string_to_replace, '')
    # add caption add the end of the string
    df_latex += "\caption{%s}\n" % caption
    # add label add the end of the string
    df_latex += "\label{%s}" % label
    return df_latex

