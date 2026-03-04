import statistics
import sys
import csv
import pandas as pd
import numpy as np
import statistics as st
import scipy.stats as stats
import math

def inputHandler(csvfile):
    df = pd.read_csv(csvfile)
    column_name = df.columns[1]
    trt_name = df.columns[0]

    return df, column_name, trt_name

def getMSE(df, column_name, trt_name, ):
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

    MSerror = df_error / df_error

    return MSerror

def getCutoff(csvfile, alpha):
    df, column_name, trt_name = inputHandler(csvfile)
    N = df[column_name].size
    t = df[trt_name].unique().size

    df_error = N-t
    MSerror= getMSE(df, column_name, trt_name)

    t_crit = stats.t.ppf(1-(alpha/2), N-t)

    cutoff = t_crit * math.sqrt(MSerror * (2/t))
    print(cutoff)


if __name__ == '__main__':
    csvfile = sys.argv[1]
    getCutoff(csvfile, 0.05)

