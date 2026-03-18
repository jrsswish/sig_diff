import pandas as pd
import numpy as np
import sys


def inputHandler(csvfile):
    # For this code we will assume block is in first column and trt is in second column
    df = pd.read_csv(csvfile)
    block_name = df.columns[0]
    trt_name = df.columns[1]
    response = df.columns[2]
    return df, block_name, trt_name, response


def getMSE(csvfile):
    df, block_name, trt_name, response = inputHandler(csvfile)
    b= df[block_name].size
    t= df[trt_name].size
    means = df.groupby(block_name)[response].mean()
    print(means)


    # SSblock = t(b-1)

if __name__ == '__main__':
    csvfile = sys.argv[1]
    print(getMSE(csvfile))
    