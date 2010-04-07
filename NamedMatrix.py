import numpy as np


class NamedMatrixError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NamedMatrix:
    """
    """
    nullvalue=float('inf')
    
    def __init__(self,matrix,rownames=[],colnames=[], dtype='float32'):
        self.dtype = dtype
        self.matrix = matrix
        self.rownames = rownames
        self.colnames = colnames
        

def readfromfile(filename, separator='\t', header=True, rownames=True, comment='#', skip=0, nullvalue="NA", dtype='float32'):
    data = []
    rnames = []
    cnames = []
    startcol=0
    matrix=[]
    if rownames:
        startcol=1
    nullvalue=str(nullvalue)
    lnum=0
    nc = None
    for line in open(filename, 'r'):
        lnum=lnum+1
        if line[0] != '#' and lnum > skip:
            fields = line.strip().split(separator)
            if header and lnum == skip+1:
                cnames = fields[1:]
                continue
            if rownames:
                rnames.append(fields[0])
            row = map(lambda x: float(x) if x != nullvalue else float('inf'), fields[startcol:])
            if (nc != None and len(row) != nc):
                raise NamedMatrixError( "In NamedMatrix.readfromfile: \nInvalid number of columns at row: "+str(lnum)+ " file: "+filename)
            nc = len(row)
            data.append(row)
    try:
        matrix = np.array(np.cast[dtype](data))
    except Exception, (enum, estr):
        raise NamedMatrixError( "In NamedMatrix.readfromfile: \nCould not cast read data to numpy array!\n Check the data dimensions in file: "+filename+".\nTraceback:\n"+str(estr))
     
    nr = len(matrix)
    if not rownames:
        rnames = map(lambda x: "r"+str(x+1), range(nr))
    if not header:
        cnames = map(lambda x: "c"+str(x+1), range(nc))

    if (len(rnames) != nr or not(nr > 0)):
        raise NamedMatrixError("In NamedMatrix.readfromfile: \nInvalid number of rownames! Expected: "+str(nr)+" Found: "+str(len(rnames)))
    if (len(cnames) != nc):
        raise NamedMatrixError("In NamedMatrix.readfromfile: \nInvalid number of colnames! Expected: "+str(nc)+" Found: "+str(len(cnames)))
    rnames = np.array(rnames)
    cnames = np.array(cnames)
    return NamedMatrix(matrix, rnames, cnames)

