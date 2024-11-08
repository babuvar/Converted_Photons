#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

import glob
import numpy as np

sub_type='GMC'
#sub_type='Data'






#---------------------------------------------------------------
#-------------------    Generic-MC-13 JOBS   -------------------
#---------------------------------------------------------------

if sub_type == 'GMC':

        n_splits = 20
        #n_splits = 100
        #n_splits = 2

        types=['ccbar', 'charged', 'ddbar', 'mixed', 'ssbar', 'taupair', 'uubar']
        #types=['uubar']

for batch in range(10):
#for batch in range(5):
#for batch in range(1):

                for typ in types:

                        files=glob.glob('/group/belle2/dataprod/MC/MC13b/release-04-01-00/DB00000758/proc10/batch%s/%s/mdst/*.root'%(batch,typ))
                        split_files = np.array_split(files, n_splits)
                        split_files = np.asarray(split_files)

                        for i in range(n_splits):
                                InputSet=str(split_files[i]).strip('[]').replace("\n ", ",").replace("'", "")
                                filename='gmc13b_batch%s_%s_%s'%(batch,typ,i)
                                os.system('bsub -q l -oo log/GMC/batch%s/%s.log  basf2 -l INFO reco_congam.py GMC  %s  root/GMC/batch%s/%s.root ' %(batch,filename,InputSet,batch,filename))



#---------------------------------------------------------------
#-------------------    Generic-MC-13 JOBS   -------------------
#---------------------------------------------------------------






