import h5py
import numpy as np
from sets import Set

class MatrixDecompHDF5:
    def __init__(self, file):
        self.file=file
        self.h5 = h5py.File(file,"r")
    def __del__(self):
        self.h5.close()
    def getPopulations(self):
        return self.h5["/freqs/colnames"][...]
    def getFreqByIndex(self, index):
        return self.h5["/freqs/matrix"][index,:]
    def getAlleleFrequencies(self, rsid):
        row = self.getrsidRow(rsid)
        if row == None:
            return None
        return self.getFreqByIndex(row)
    def getrsidRow(self, rsid):
        rnames = self.h5["/freqs/rownames"][...]
        idx = 0
        while idx < len(rnames):
            if rnames[idx] == rsid:
                return idx
        return None


        
