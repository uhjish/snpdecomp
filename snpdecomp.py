import h5py
import numpy as np
from rpy2.robjects import r 
import NamedMatrixHDF5 as nm
import rpy2.robjects.numpy2ri
from sets import Set

class MatrixDecompError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MatrixDecompHDF5:
    def __init__(self, mat, hdf5file, url):
        self.mat=mat
        self.file=hdf5file
        self.url = url
        makesubsets(self)
        self.h5 = h5py.File(self.file,'r')
        loadsubsets(self)
        self.hndl = self.h5[self.url]
        self.groups={}
    def __del__(self):
        self.h5.close()
    def makesubsets(self):
        fw = h5py.File(self.hdf5file, 'w')
        grp = fw[self.url]
        sigfn = lambda x: ",".join(map(lambda y: str(y), (x != mat.nullvalue)*1))
        grp.create_dataset('subsetmaps', data=np.apply_along_axis(sigfn,1,self.mat.matrix))
        fw.close() 
    def loadsubsets(self):
        colfn = lambda x: (x != mat.nullvalue)
        self.subsetmaps = self.hndl['subsetmaps']
        self.subsetcols = {}
        subs = np.unique(subsetmaps,return_index=True)
        for subsid, subsindex in subs:
            self.subsetcols[subsid] = colfn(self.subsetmaps[subsindex,])
    def getsubsetrows(subset):
        return self.mat[ self.subsmap.values == subset, : ]
    def apply_over_subsets(func, groupid, overwrite=False):
        try:
            grp = hndl[groupurl]
            del grp
        except:
            if (not overwrite):
                raise MatrixDecompError( "In MatrixDecompHDF5.apply_over_subsets: \n"+hdf5file+":"+groupurl+" exists and overwriting not allowed! ")
            else:
                pass
        hndl.create_group(groupurl)
        grp = hndl[groupurl]
        self.groups[groupurl]=grp
        return grp

class MatrixDecompPCA:
    def __init__(self, pca_group_handle):
        self.hndl = pca_group_handle
        #[1] "sdev"     "rotation" "center"   "scale"    "x"
        self.sdev = hndl[0]
        self.loadings =  hndl[1]
        self.components = hndl[4]
        
