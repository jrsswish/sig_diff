import sys
import csv
import pandas as pd
import numpy as np
import statistics as st

def inputHandler(csvfile):
    df = pd.read_csv(csvfile)
    print(df)
    column_name = df.columns[1]
    trt_name = df.columns[0]
    print(trt_name)
    print(column_name)
    return df, column_name, trt_name

def getCutOff(df, column_name, trt_name):
    s2_all = st.variance(df[column_name])
    N = df[column_name].size
    SStotal = (N - 1) * s2_all

    t = df[trt_name].value_counts().size
    SStrt = (t - 1) * s2_all

    SSerror = SStotal - SStrt



if __name__ == '__main__':
    csvfile = sys.argv[1]
    df, column_name, trt_name = inputHandler(csvfile)
    getCutOff(df, column_name, trt_name)