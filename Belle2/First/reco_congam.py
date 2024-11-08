#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import basf2 as b2
from basf2 import *
import modularAnalysis as ma
from b2biiConversion import convertBelleMdstToBelleIIMdst, setupB2BIIDatabase
import json
import glob
import vertex as vtx
import variables.collections as vc
import variables.utils as vu


#General
reco_path = b2.create_path()


#Get job-parameters
data_kind=str(sys.argv[1])

if data_kind == 'GMC':

	file_index=int(sys.argv[2])
	typ=str(sys.argv[3])
	outputBelle2ROOTFile=str(sys.argv[4])
	#Input files
	files=[]
	for i in range((file_index*100),((file_index+1)*100)):
	#for i in range((file_index*10),((file_index+1)*10)):
		files.append('/group/belle2/dataprod/MC/release-03-01-00/DB00000547/MC12b/s00/e1003/4S/r00000/%s/%s_%s.root'%(typ,typ,i))
	globalTag = 'MC'


if data_kind == 'Data':

	input_dir = str(sys.argv[2])
	files=glob.glob('%s/*.root'%input_dir)
	outputBelle2ROOTFile=str(sys.argv[3])	
	globalTag = 'data_reprocessing_proc9' # global tag to use with proc9
	use_central_database(globalTag)



#root input
ma.inputMdstList(environmentType='default', filelist=files, path=reco_path)


# Reconstruction

#variable dictionary
var_dict = json.load(open("variables_congam.json"))
tuple_vars = []

for key, val in var_dict['congam_vars'].items():
        ma.variables.addAlias('%s' % key, '%s' % val)
        tuple_vars += ['%s' % key]

#cuts
#cuts='InvM < 0.3 and X > -3 and X < 3 and Y > -3 and Y < 3 and e1_firstSVDLayer == 3 and e2_firstSVDLayer == 3 and e1_mom > 0.3 and e2_mom > 0.3 and e1_PID > 0.4 and e2_PID > 0.4 '
cuts='InvM < 0.3 and X > -20 and X < 20 and Y > -20 and Y < 20 and e1_mom > 0.3 and e2_mom > 0.3 and e1_PID > 0.4 and e2_PID > 0.4 '
      

# Reconstruct photons that convert to e+e- and do a vertex fit. InvM determined from daughter

ma.fillConvertedPhotonsList('gamma:conv -> e+:loose e-:loose', cuts, path=reco_path) 
ma.matchMCTruth('gamma:conv', path=reco_path)


#make duplicates
ma.copyParticles('gamma:treefit', 'gamma:conv', path=reco_path)
ma.copyParticles('gamma:kfit', 'gamma:conv', path=reco_path)
ma.copyParticles('gamma:rave', 'gamma:conv', path=reco_path)


#vertexing
ma.vertexTree('gamma:treefit', -1.1, ipConstraint=False, path=reco_path)
ma.vertexRave('gamma:rave', conf_level=-1.1, path=reco_path, silence_warning=True)
ma.vertexKFit('gamma:kfit', conf_level=-1.1, path=reco_path)


#cuts
ma.applyCuts('gamma:treefit', cuts, path=reco_path)
ma.applyCuts('gamma:rave', cuts, path=reco_path)
ma.applyCuts('gamma:kfit', cuts, path=reco_path)


#save trees
ma.variablesToNtuple('gamma:treefit', tuple_vars, filename=outputBelle2ROOTFile, treename = 'treefit', path=reco_path)
ma.variablesToNtuple('gamma:rave', tuple_vars, filename=outputBelle2ROOTFile, treename = 'rave', path=reco_path)
ma.variablesToNtuple('gamma:kfit', tuple_vars, filename=outputBelle2ROOTFile, treename = 'kfit', path=reco_path)


# progress
progress = b2.register_module('Progress')
reco_path.add_module(progress)
b2.process(path=reco_path)

# Print call statistics
print(b2.statistics)




