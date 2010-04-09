import h5py
import numpy as np

sigfn = lambda x: str(",".join(map(lambda y: str(y), (x != float('inf'))*1)))

class MatrixDecompHDF5:
    available_scores = ["rankscore","sdevscore"]
    def __init__(self, file):
        self.file=file
        self.h5 = h5py.File(file,"r")
    def __del__(self):
        self.h5.close()
    def getPopulations(self):
        return self.h5["/freqs/colnames"][...]
    def getFreqByIndex(self, index):
        return self.h5["/freqs/matrix"][index,:]
    def getFreqByRSid(self, rsid):
        rows = self.getRSidRows(rsid)
        if rows == []:
            return []
        return self.getFreqByIndex(rows)
    def getSubsetName(self, rsid):
        freqs = self.getFreqByRSid(rsid)
        return map(sigfn, freqs)
    def getSubsetRowNums(self, subset, index):
        path= "/pca/"+subset+"/rownums"
        idx = np.where(self.h5[path][...] == index)
        return idx
    def getLoadingsByIndex(self,index):
        index=np.array(index)
        freqs = self.getFreqByIndex(index)
        subset = sigfn(freqs)
        path= "/pca/"+subset+"/loadings"
        idx = self.getSubsetRowNums(subset,index)
        ldngs = self.h5[path][idx,:]
        return ldngs
    def getScoresByIndex(self,score,index):
        index=np.array(index)
        freqs = self.getFreqByIndex(index)
        subset = sigfn(freqs)
        path= "/pca/"+subset+"/"+score
        idx = self.getSubsetRowNums(subset,index)
        ldngs = self.h5[path][idx,:]
        return ldngs
    def getSdevsByIndex(self,index):
        index=np.array(index)
        freqs = self.getFreqByIndex(index)
        subset = sigfn(freqs)
        path= "/pca/"+subset+"/sdev"
        ldngs = self.h5[path][...]
        return ldngs
    def getRSidRows(self, rsid):
        rnames = self.h5["/freqs/rownames"][...]
        rows= []
        idx = 0
        while idx < len(rnames):
            if rnames[idx].endswith(rsid):
                rows.append(idx)
            idx = idx +1 
        return rows 
    def getRownames(self, rows):
        rnames = self.h5["/freqs/rownames"][...]
        return rnames[rows]
    def getAvailScores(self):
        return self.available_scores
        

        
