import NamedMatrix
import NamedMatrixHDF5
import sys
import numpy as np
import snpdecomp as snp
try:
    filename = sys.argv[1]
    projectname = sys.argv[2]
except Exception:
    print "USAGE:\npython rundecomp.py matrixfile projectname"


print "Filename: " + filename + "\nProject: " + projectname

mat = NamedMatrixHDF5.readfromfile(projectname,"/freqs",filename,separator="\t",header=True,rownames=True,nullvalue="-1")

print mat.matrix[0,0:]

matdecomp = 

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

