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

mat = NamedMatrix.readfromfile(filename,nullvalue="-1")

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
            return(prcomp(t(submat)))
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
        shndl.create_dataset("components",data=pca[4])
    except:
        print pca
        print s


h5.close()

#blah = matdecomp.apply_over_subsets(snp.runPCA,"/freqs/test",True)
#mat = NamedMatrix.readfromfile(filename,separator="\t",header=True,rownames=True,nullvalue="-1")


## To test creat HDF5 files
#indir =  '/Users/krokodil/samples/mSeq_cors/m/txt'
#outdir = '/Users/krokodil/samples/mSeq_cors/m/hdf5'
#wf.allToHDF5(indir, outdir)

#### To test by Row
#base1 = 'mirna_shift_filt'
#searchstring1='hcmv-miR-US4'
#base2 = 'gene_qnorm_all'
#searchstring = 'A_23_P87351'
#dirin='/Users/krokodil/samples/mSeq_cors/m/hdf5'
#dirout='/Users/krokodil/samples/mSeq_cors/m/hdf5'
#rc.cor_by_row_matrix(dirin, dirout, base2, searchstring,  method='spearman')

#results = rc.cor_by_row_R(dirin, dirout, base1, searchstring1, method='spearman')
#print(results)
#rc.cor_by_row_between_datasets_R(dirin, dirout, base1, base2, searchstring)


###### To test by Col
#base = 'mirna_shift_filt'
#searchstring='MICMA015T'

base = 'gene_qnorm_all'
searchstring = 'MICMA015T'

#dirin='/Users/krokodil/samples/mSeq_cors/m/hdf5'
#dirout='/Users/krokodil/samples/mSeq_cors/m/hdf5'
#
#cc.cor_by_col_R(dirin,dirout, base, searchstring, method='spearman')


## To test creat HDF5 files
#indir =  '/home/vlad/Util/website/gtest/cor/txt'
#outdir = '/home/vlad/Util/website/gtest/cor/hdf5'
#wf.allToHDF5(indir, outdir)

#### To test by Row
base1 = 'mirna_shift_filt'
searchstring='hcmv-miR-US4'
base2 = 'gene_qnorm_all'
#searchstring = 'A_23_P87351'
dirin='/home/vlad/Util/website/gtest/cor/hdf5'
dirout='/home/vlad/Util/website/gtest/cor/out'
#rc.cor_by_row_R(dirin, dirout, base2, searchstring, method='spearman')



##### To test in R
# m2<-read.table(file='/Users/krokodil/samples/mSeq_cors/m/gene_qnorm_all.tsz', header=TRUE, sep='\t')
# m1<-read.table(file='/Users/krokodil/samples/mSeq_cors/m/mirna_shift_filt.tsv', header=TRUE, sep='\t')

