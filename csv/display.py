from scipy.misc import imsave
import cv2
import numpy as np
import pylab as plt
from skimage import morphology
import os
import pandas as pd


if __name__ == '__main__':
    index=442
    df=pd.read_csv("%04d.csv"%index)
    x=df["X"]
    y=df["Y"]
    plt.xlim(640)
    plt.ylim(640)
    plt.plot(x,y)
    plt.show()