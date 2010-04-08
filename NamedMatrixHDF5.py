import h5py
import os
import numpy as np
import NamedMatrix as nm

class NamedMatrixHDF5(nm.NamedMatrix):
    def __init__(self,hdf5file,url):
        self.file=hdf5file
        self.url=url
        self.unlock()
    def getinitvars(self):
        self.colnames = self.hndl['colnames']
        self.rownames = self.hndl['rownames']
        self.matrix = self.hndl['matrix'] 
    def lock(self):
        self.h5.close()
    def unlock(self):
        self.h5 = h5py.File(self.file)
        self.hndl = self.h5[self.url]
        self.getinitvars()    
        

def readfromfile(hdf5file, url, *args, **kwargs):
    mat = nm.readfromfile(*args, **kwargs)
    nmat = writeNamedMatrix( mat, hdf5file, url, overwrite=True)
    return nmat

def writeNamedMatrix( matrix, hdf5file, groupurl, overwrite=True):
    print "groupurl: " + groupurl
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

