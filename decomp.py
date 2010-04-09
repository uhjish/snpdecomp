#!/usr/bin/python2.6
import index
import cgi
import warnings
import cgitb
import snpdecomp

snpscorereq="snpscores"

try:
    dataset="exonic.hapmap.h5"
    data = snpdecomp.MatrixDecompHDF5(dataset)
except Exception, (estr):
    print "Content-Type: text/plain\n"+str(estr) 

def get_index_page():
    idxpg = index.index()
    idxpg.contenttype="Content-Type: text/html\n"
    idxpg.title="SNPDecomp - Main"
    idxpg.availScores=data.getAvailScores()
    idxpg.snpscorereq=snpscorereq
    return idxpg

def get_snpscores_page(scoretype):
    

try:
    form = cgi.FieldStorage()
    page = form["page"].value
    if page == "index":
        print get_index_page()
    if page == "snpscores":
        scoretype = form["scorechooser"].value
        print get_snpscores_page(scoretype)
except Exception, (estr):
    print "Content-Type: text/plain\n"+str(estr) 

