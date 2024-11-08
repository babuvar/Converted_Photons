#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import glob
import numpy as np

sub_type=''
#sub_type='GMC'
#sub_type='Data'



files=glob.glob('/group/belle2/dataprod/MC/MC13b/release-04-01-00/DB00000758/proc10/batch9/uubar/mdst/*.root')
split_files = np.array_split(files, 100)
split_files = np.asarray(split_files)
InputSet=str(split_files[50]).strip('[]').replace("\n ", ",").replace("'", "")
lst = InputSet.split(",")
print(lst)

#InputSet=list(split_files[50])
#InputSet=str(InputSet)
#InputSet.replace(" ", "")
#print(InputSet)
#print(type(InputSet))





#---------------------------------------------------------------
#-------------------    Generic-MC-12 JOBS   -------------------
#---------------------------------------------------------------
if sub_type == 'GMC':

        n_splits = 10

        #types=['ccbar', 'charged', 'ddbar', 'mixed', 'ssbar', 'taupair', 'uubar']
        types=['uubar']

        for typ in types:

                files=glob.glob('/group/belle2/dataprod/MC/MC13b/release-04-01-00/DB00000758/proc10/batch9/%s/mdst/*.root'%typ)
                split_files = np.array_split(files, n_splits)
                split_files = np.asarray(split_files)

                for i in range(n_splits):
                        #InputSet=list(split_files[i])
                        InputSet=str(split_files[i])
                        print(InputSet)
                        filename='gmc13b_%s_%s'%(typ,i)
                        print("==================================================================")
                        #print(InputSet)
                        os.system('bsub -q l -oo log/GMC/%s.log  basf2 -l INFO reco_congam.py GMC  %s  root/GMC/%s.root ' %(filename,InputSet,filename))


#---------------------------------------------------------------
#-------------------    Generic-MC-12 JOBS   -------------------
#---------------------------------------------------------------












