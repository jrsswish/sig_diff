import pandas as pd
import numpy as np
import sys
from natsort import index_natsorted, natsorted


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
    k = df.groupby(block_name).count().values[1][1]
    r = df.groupby(trt_name).count().values[1][1]
    lambda_value = r*(k-1)/(t-1)

    # this will contain all of the avg of blocks that contain trt[i]
    avg_list = [0]*t
    Q_list = [0]*t
    trt_list = df[trt_name].unique().tolist()
    trt_list =natsorted(trt_list)
    blk_list = df[block_name].unique().tolist()
    blk_list = natsorted(blk_list)
    block_avgs = df.groupby(block_name)[response].mean()

    # takes the value of index
    index_val = block_avgs.index.tolist()
    # sort the index so that ex: blk10 will be last instead of 2nd
    new_index = natsorted(index_val)
    # change the index of the block avgs
    block_avgs = block_avgs.reindex(new_index)

    trt_avgs = df.groupby(trt_name)[response].mean()
    print(trt_avgs)
    for i in range(N):
        trt_i = df[trt_name].values[i]
        # print(trt_i)
        # take the index of trt
        trt_idx = trt_list.index(trt_i)

        blk_i = df[block_name].values[i]
        blk_idx = blk_list.index(blk_i)
        # trt1 idx = 0, trt2 idx = 1 .. ect
        # if idx of trt_i is 0 then the avg_list[0] will be added by block avg of trt[i]
        avg_list[trt_idx] = avg_list[trt_idx] + block_avgs.values[blk_idx]

    # print(avg_list)
    avg_list = avg_list/r
    print(avg_list)

    for i in range(t):
        Q_i = r*(trt_avgs.values[i] - avg_list[i])
        Q_list[i] = Q_i

    Q_list_squared = [Q_list[i]**2 for i in range(len(Q_list))]
    SStrt = (k/(lambda_value*t)) * (sum(Q_list_squared))
if __name__ == '__main__':
    csvfile = sys.argv[1]
    print(Significant_finder_BIBD(csvfile))
    