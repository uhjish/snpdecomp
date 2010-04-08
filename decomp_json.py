#!/usr/bin/env python2.6
import sys
import cgi
import warnings
import cgitb
import snpdecomp
    
def print_return():
    print "Content-Type: text/plain\n"
    #form = cgi.FieldStorage()
    #rsid = form["rsid"].value 
    rsid="rs12345"
    dataset="exonic.hapmap.h5"
    data = snpdecomp.MatrixDecompHDF5(dataset) 
    print str(data.getPopulations())
    print str(data.getFreqByIndex(0))

print_return()
