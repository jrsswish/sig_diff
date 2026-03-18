import pandas as pd
import numpy as np
import sys


def inputHandler(csvfile):
    df = pd.read_csv(csvfile)
    return df


def getMSE(csvfile):
    df = inputHandler(csvfile)
