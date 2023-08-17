


def add_midrule_over(row_name : list, latex_string):
    """adds a midrule over the rows into the latex string"""
    for i in range(0, len(row_name)):
        row_name[i] = '\n' + row_name[i] + ' &'
        latex_string = latex_string.replace(row_name[i], "\n\\midrule" + row_name[i])
    return latex_string

def make_column_header(names_1, names_2):
    return "\multicolumn{1}{p{1.8cm}}{\\raggedleft %s \\\\  ----  \\\\ %s}" % (names_1, names_2)

def add_header(names_for_headers, latex_string_diff, self=False):
    header_string = " " # one space for the upper left corner
    for i in range(0, len(names_for_headers)):
        for j in range(0, i):
            header_string += '& ' + make_column_header(names_for_headers[i], names_for_headers[j])
    header_string = "\n\\toprule\n" + header_string
    header_string += "\\\\\n\\midrule\n"
    latex_string_diff = latex_string_diff.replace("\n\\toprule\n\\midrule\n", header_string)
    return latex_string_diff

def make_latex_table_pvalues_reject_fail(df, caption, label, precision=6):
    latex_string = df.to_latex(header=True, float_format=f"%.{precision}f", index=True)
    # multiline header
    # latex_string = add_header(names_for_headers, latex_string)
    # line over reject and fail
    latex_string = add_midrule_over(['reject'], latex_string)
    # caption
    latex_string += caption
    # label
    latex_string += label
    return latex_string

def save_latex_table(latex_string_self, folder, error_type, test_name, postfix=""):
    with open(folder + test_name +"_"+ error_type +"_"+ postfix + ".tex", "w") as f:
            f.write(latex_string_self)
            f.close()