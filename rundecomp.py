import NamedMatrix
import NamedMatrixHDF5
import sys
import numpy as np
import snpdecomp as snp
from rpy2.robjects import r
import rpy2.robjects as ro
import rpy2.robjects.numpy2ri
import rpy2.rpy_classic as rpy
import h5py

try:
    filename = sys.argv[1]
    projectname = sys.argv[2]
except Exception:
    print "USAGE:\npython rundecomp.py matrixfile projectname"


print "Filename: " + filename + "\nProject: " + projectname

mat = NamedMatrix.readfromfile(filename,nullvalue="-1",header=True, rownames=True,separator='\t',skip=0)

NamedMatrixHDF5.writeNamedMatrix(mat, projectname, "/freqs",overwrite=True)

sigfn = lambda x: str(",".join(map(lambda y: str(y), (x != float('inf'))*1)))

setnames = np.apply_along_axis(sigfn,1,mat.matrix)
unq_subs = np.unique(setnames)
colfn = lambda x: np.array(map(lambda y: y!=str(0), x.split(",")))
cols = map(colfn,unq_subs)

h5 = h5py.File(projectname)
h5.create_group("subsets")
hndl = h5["/subsets"]
hndl.create_dataset("names",data=unq_subs)
hndl.create_dataset("columns",data=cols)

r('''
        runPCA_sub <- function(sname, matr, setnames) {
            subs = which(setnames==sname)
            submat = matr[subs,]
            if (length(subs)==1){
                return(0)
            }
            cols = which(is.finite(submat[1,]))
            submat = submat[,cols]
            pcs = prcomp(t(submat))
            pctile = apply(pcs$rotation,2,function(x){rank(abs(x),ties.method="first")})/length(subs)
            scaled = t(apply(pctile,1,function(x){x*pcs$sdev}))
            sdevscore = apply(pcs$rotation,1,sd)
            pcs[["rankscore"]]=scaled
            pcs[["sdevscore"]]=sdevscore
            pcs[["rownums"]]=subs
            return(pcs)
        }

        ''')
runpcasub = r['runPCA_sub']

h5.create_group("pca")
hndl = h5["/pca"]

for i,s in enumerate(unq_subs):
    if np.sum(cols[i])<=1:
        print "unsavory: " + s
        continue
    pca = runpcasub(s, mat.matrix, setnames)
    if pca[0] == 0:
        print "useless: " + s
        continue
    try:
        hndl.create_group(s)
        shndl=hndl[s]
        shndl.create_dataset("sdev",data=pca[0])
        shndl.create_dataset("loadings",data=pca[1])
        shndl.create_dataset("center",data=pca[2])
        shndl.create_dataset("scale",data=pca[3])
        shndl.create_dataset("components",data=pca[4])
        shndl.create_dataset("rankscore",data=pca[5])
        shndl.create_dataset("sdevscore",data=pca[6])
        shndl.create_dataset("rownums",data=pca[7])
    except:
        print pca
        print s


h5.close()
