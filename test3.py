import numpy as np


def loopifyArr(arr: np.ndarray):
    for si in range(len(arr.shape)): arr = np.concatenate((arr, np.expand_dims(arr.take(0, si), si)), axis=si)
    return arr


ar = np.random.random((2, 3, 4))
ar = loopifyArr(ar)
print(ar)
