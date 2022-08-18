import itertools
import numpy as np
from .logger import log

def xor_lists(a, b):
    assert len(a) == len(b)
    return [x ^ y for x,y in zip(a,b)]

def arr_map(arr, fcn):
    """
    arr is a bit-planed numpy array

    returns arr with fcn applied to each pixel in arr
        where pixel is defined in iterate_pixels
    """
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i,j] = fcn(arr[i,j])
    return arr

def pbc_to_cgc(arr):
    
    log.critical('Graying...')
    def pbc_to_cgc_mapper(planes):
        new_planes = []
        for i in range(planes.shape[1]):
            if i == 0:
                new_planes.append(planes[:, i].tolist())
            else:
                new_planes.append(xor_lists(planes[:, i], planes[:, i-1]))
        return np.array(new_planes).transpose()
    return arr_map(arr, pbc_to_cgc_mapper)

def cgc_to_pbc(arr):
    log.critical('Ungraying...')
    def cgc_to_pbc_mapper(planes):
        new_planes = []
        for i in range(planes.shape[1]):
            if i == 0:
                new_planes.append(planes[:, i].tolist())
            else:
                new_planes.append(xor_lists(planes[:, i], new_planes[i-1]))
        return np.array(new_planes).transpose()
    return arr_map(arr, cgc_to_pbc_mapper)

class BitPlane:
    def __init__(self, arr, gray=False):
        self.arr = arr
        self.gray = gray

    def bin_strs_to_decimal(self, vals):
        return int(''.join([str(x) for x in vals]), 2)

    def decimal_to_bin_strs(self, val, nbits):
        return [int(x) for x in bin(val)[2:].zfill(nbits)[:nbits]]

    def slice(self, nbits):
        log.critical('Slicing...')
        basearr = [self.decimal_to_bin_strs(i, nbits) for i in self.arr.reshape(-1)]
        tmparr = np.reshape(basearr, self.arr.shape + (nbits,))
        if self.gray:
            tmparr = pbc_to_cgc(tmparr)
        assert tmparr.shape == self.arr.shape + (nbits,)
        return tmparr

    def stack(self):
        tmparr = self.arr
        if self.gray:
            tmparr = cgc_to_pbc(tmparr)
        def iterate_all_but_last_dim(arr):
            all_inds = [range(dim_size) for dim_size in arr.shape]
            for ind in itertools.product(*all_inds[:-1]):
                yield ind
        log.critical('Stacking...')
        tmparr = np.reshape([self.bin_strs_to_decimal(tmparr[ind]) for ind in iterate_all_but_last_dim(tmparr)], tmparr.shape[:-1])
        assert tmparr.shape == self.arr.shape[:-1]
        return tmparr
