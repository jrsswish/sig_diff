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

def Significant_finder_BIBD(csvfile):
    df, block_name, trt_name, response = inputHandler(csvfile)
    MSE = getMSE(csvfile)
    b= df[block_name].unique().size
    t= df[trt_name].unique().size
    N = df[response].size
    r = df.groupby(block_name).count().values[1][1]
    k = df.groupby(trt_name).count().values[1][1]
    lambda_value = r*(k-1)/(t-1)
    sum_list = [0]*t
    trt_list = df[trt_name].unique().tolist()
    trt_list.sort()
    print(trt_list)

    block_avgs = df.groupby(block_name)[response].mean()

    for i in range(N):
        trt_i = df[trt_name].values[i]
        # print(trt_i)
        # take the index
        idx = trt_list.index(trt_i)
        # print(index)
        sum_list[idx] = sum_list[idx] + block_avgs.values[idx]











if __name__ == '__main__':
    csvfile = sys.argv[1]
    print(Significant_finder_BIBD(csvfile))
    