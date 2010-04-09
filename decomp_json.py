#!/usr/bin/env python2.6
import sys
import cgi
import warnings
import cgitb
import snpdecomp
import simplejson as json
    
def print_return():
    print "Content-Type: application/json\n"
    form = cgi.FieldStorage()
    try:
        rsid = form["rsid"].value 
    except:
        rsid="rs4807"
    dataset="exonic.hapmap.h5"
    data = snpdecomp.MatrixDecompHDF5(dataset)
    rows = data.getRSidRows(rsid)
    result={}
    errmsg=None
    try:
        if rows != None:
            result["populations"]=data.getPopulations().tolist()
            result["subsetname"]=data.getSubsetName(rsid)
            result["frequencies"]=data.getFreqByIndex(rows).tolist()
            result["loadings"]=data.getLoadingsByIndex(rows).tolist()
            result["sdev"]=data.getSdevsByIndex(rows).tolist()
            result["rownames"]=data.getRownames(rows).tolist()
            result["rankscores"]=data.getRankScoresByIndex(rows).tolist()
    except Exception:
        errmsg = str("Uhoh!")
        raise
    
    retval={ "error":errmsg,
             "result":result}
    
    print json.dumps(retval)
print_return()
