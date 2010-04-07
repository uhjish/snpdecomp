import h5py
import os
import numpy as np
import NamedMatrix as nm

class NamedMatrixHDF5(nm.NamedMatrix):
    def __init__(self,hdf5file,url):
        self.file=hdf5file
        self.url=url
        self.h5 = h5py.File(self.file,'r')
        self.getinitvars()    
    def getinitvars(self):
        hndl = self.h5[self.url]
        self.colnames = hndl['colnames']
        self.rownames = hndl['rownames']
        self.matrix = hndl['matrix'] 
    def __del__(self):
        self.h5.close()
            


def readfromfile(hdf5file, url, *args, **kwargs):
    mat = nm.readfromfile(*args, **kwargs)
    nmat = writeNamedMatrix( mat, hdf5file, url, overwrite=True)
    return nmat

def writeNamedMatrix( matrix, hdf5file, groupurl, overwrite=False):
    f = h5py.File(hdf5file, 'w')
    try:
        grp = f[groupurl]
        del grp
    except:
        if (not overwrite):
            raise NamedMatrixError( "In NamedMatrixHDF5.writeNamedMatrix: \n"+hdf5file+":"+groupurl+" exists and overwriting not allowed! ")
        else:
            pass

    f.create_group(groupurl)    
    grp = f[groupurl]


    grp.create_dataset('rownames',data=matrix.rownames)
    grp.create_dataset('colnames',data=matrix.colnames)
    grp.create_dataset('matrix',data=matrix.matrix)

    return NamedMatrixHDF5(hdf5file,groupurl)

