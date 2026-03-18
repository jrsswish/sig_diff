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
    b= df[block_name].unique().size
    t= df[trt_name].unique().size
    N = df[response].size
    print(b, t)
    blkmeans = df.groupby(block_name)[response].mean()
    s2_blkmean = blkmeans.var()
    print(s2_blkmean)

    SSblock = t*(b-1)*s2_blkmean
    print(SSblock)

    trtmeans = df.groupby(trt_name)[response].mean()
    s2_trtmean = trtmeans.var()
    print(s2_trtmean)

    SStrt = b*(t-1)*s2_trtmean
    print(SStrt)

    s2_all = df[response].var()
    print(s2_all)

    SStotal = (N-1)*s2_all
    print(SStotal)


if __name__ == '__main__':
    csvfile = sys.argv[1]
    print(getMSE(csvfile))
    