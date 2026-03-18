import statistics
import sys
import csv
import pandas as pd
import numpy as np
import statistics as st
import scipy.stats as stats
import math
import tabulate as tb

def inputHandler(csvfile):
    df = pd.read_csv(csvfile)
    column_name = df.columns[1]
    trt_name = df.columns[0]

    return df, column_name, trt_name

def getMSE(df, column_name, trt_name):
    s2_all = st.variance(df[column_name])
    N = df[column_name].size
    SStotal = (N - 1) * s2_all

    t = df[trt_name].unique().size
    SSerror = 0

    for i in range(t):
        n = df[trt_name].value_counts().values[i]
        s2_trti= df.groupby(trt_name)[column_name].var().values[i]
        SSerror += (n-1) * s2_trti

    SStrt = SStotal - SSerror

    df_error = N-t

    MSerror = SSerror / df_error

    return MSerror

def getCutoff(csvfile, alpha):
    df, column_name, trt_name = inputHandler(csvfile)
    N = df[column_name].size
    t = df[trt_name].unique().size


    df_error = N-t
    c = (t*(t-1))/(2)

    alpha_prime = alpha/c

    MSerror= getMSE(df, column_name, trt_name)

    t_crit = stats.t.ppf(q=1-(alpha_prime/2), df=df_error)
    cutoff = t_crit * math.sqrt(MSerror * (2/t))

    return cutoff

def significantFinder(csvfile, alpha):
    df, column_name, trt_name = inputHandler(csvfile)
    N = df[column_name].size
    t = df[trt_name].unique().size

    cutoff_value = getCutoff(csvfile, alpha)

    trt_meansi = df.groupby(trt_name).mean()
    sig_diff = []
    data = []
    header = []



    for i in range(t):
        row = []
        if i == 0:
            header.append('')

        header.append(trt_meansi.index[i])
        row.append(trt_meansi.index[i])
        for j in range(t):
            if j < i:
                row.append('X')
                continue
            if trt_meansi.index[i] == trt_meansi.index[j]:
                row.append('X')
                continue
            else:
                sig_value = trt_meansi.values[i] - trt_meansi.values[j]
                if abs(sig_value) > cutoff_value:
                    sig_diff.append(trt_meansi.index[i] + "-" + trt_meansi.index[j])
                    row.append(sig_value)
                else:
                    row.append(sig_value)
        data.append(row)

    table = tb.tabulate(data, headers=header,tablefmt="grid")
    print(table)

    print("Therefore the pairwise significance difference are:", sig_diff)
if __name__ == '__main__':
    csvfile = sys.argv[1]
    significantFinder(csvfile, 0.05)

