#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json

#sub_type='GMC'
sub_type='Data'






#---------------------------------------------------------------
#-------------------    Generic-MC-12 JOBS   -------------------
#---------------------------------------------------------------
if sub_type == 'GMC':

	types=['ccbar', 'charged', 'ddbar', 'mixed', 'ssbar', 'taupair', 'uubar']

	for i in range(20):
	#for i in range(1):
		for typ in types:

			filename='gmc12_%s_%s'%(i,typ)
			os.system('bsub -q s -oo log/GMC/%s.log  basf2 -l INFO reco_congam.py GMC  %s %s root/GMC/%s.root ' %(filename,i,typ,filename))


#---------------------------------------------------------------
#-------------------    Generic-MC-12 JOBS   -------------------
#---------------------------------------------------------------









#---------------------------------------------------------------
#-------------------    Real Data   ----------------------------
#---------------------------------------------------------------


if sub_type == 'Data':
	
	run_list = json.load(open("goodData_runlist.json"))
	for exp, val in run_list.items():
		for energy, runlist in run_list[exp].items():
			for run in runlist:
				filename='data_%s_%s_%s'%(exp,energy,run)
				input_dir='/group/belle2/dataprod/Data/release-03-02-02/DB00000654/proc9/%s/%s/%s/all/mdst/sub00/'%(exp,energy,run)
				os.system('bsub -q l -oo log/Data/%s.log  basf2 -l INFO reco_congam.py Data  %s  root/Data/%s.root ' %(filename,input_dir,filename))


#---------------------------------------------------------------
#-------------------    Real Data   ----------------------------
#---------------------------------------------------------------











'''
#Testing
run_list = json.load(open("goodData_runlist.json"))
exp='e0008'
energy='Scan'
for run in run_list[exp][energy]:
	filename='data_%s_%s_%s'%(exp,energy,run)
        input_dir='/group/belle2/dataprod/Data/release-03-02-02/DB00000654/proc9/%s/%s/%s/all/mdst/sub00/'%(exp,energy,run)
	os.system('bsub -q l -oo log/Data/%s.log  basf2 -l INFO reco_congam.py Data  %s  root/Data/%s.root ' %(filename,input_dir,filename))
'''






