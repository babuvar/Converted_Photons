#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import basf2 as b2
from basf2 import *
import sys
import modularAnalysis as ma
import json
import glob
import vertex as vtx
import variables.collections as vc
import variables.utils as vu
from variables import variables
import stdCharged as sc
import stdV0s as sv
import stdPhotons as sp

#General
reco_path = b2.create_path()


#Get job-parameters
data_kind=str(sys.argv[1])

if data_kind == 'GMC':

	#Input files
	files_str=sys.argv[2]
	files = files_str.split(",")
	outputBelle2ROOTFile=str(sys.argv[3])
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
var_dict = json.load(open("variables_pi0.json"))

tuple_vars = []

for key, val in var_dict['congam_vars'].items():
        #ma.variables.addAlias('%s' % key, '%s' % val)
        variables.addAlias('%s' % key, '%s' % val)
        tuple_vars += ['%s' % key]

#cuts
#cuts='e1_firstSVDLayer == 3 and e2_firstSVDLayer == 3 '
cuts_gam='e1_mom > 0.3 and e2_mom > 0.3 and e1_PID > 0.4 and e2_PID > 0.4'
cuts_pi0='M > 0.08 and M < 0.18'
#cuts2='InvM < 0.5 and Rho > 0.8' 
#cuts2='gam_isSignal == 1'
#cuts2='gam_isSignal != 1'


#cuts1='e1_mom > 0.3 and e2_mom > 0.3'     

#sv.stdKshorts(path=reco_path)
#sc.stdK('loose', path=reco_path)
sp.stdPhotons(path=reco_path)
ma.applyCuts('gamma:loose', 'E > 0.15', path=reco_path)
ma.fillConvertedPhotonsList('gamma:conv -> e+:loose e-:loose', 'daughter(0,p) > 0.3 and daughter(1,p) > 0.3' , path=reco_path) 


ma.copyParticles('gamma:kfit', 'gamma:conv', path=reco_path)
ma.copyParticles('gamma:kfitwmc', 'gamma:conv', path=reco_path)


vtx.kFit(list_name='gamma:kfit', conf_level=0.01, fit_type='vertex', daughtersUpdate=False, path=reco_path)
vtx.kFit(list_name='gamma:kfitwmc', conf_level=0.01, fit_type='massvertex', daughtersUpdate=False, path=reco_path)




ma.reconstructDecay('pi0:reg -> gamma:loose gamma:conv', cuts_pi0, path=reco_path)
ma.matchMCTruth('pi0:reg', path=reco_path)
ma.variablesToNtuple('pi0:reg', tuple_vars, filename=outputBelle2ROOTFile, treename = 'dalitz', path=reco_path)


ma.reconstructDecay('pi0:kfit -> gamma:loose gamma:kfit', cuts_pi0, path=reco_path)
ma.matchMCTruth('pi0:kfit', path=reco_path)
ma.variablesToNtuple('pi0:kfit', tuple_vars, filename=outputBelle2ROOTFile, treename = 'dalitz_kfit', path=reco_path)

ma.reconstructDecay('pi0:kfitwmc -> gamma:loose gamma:kfitwmc', cuts_pi0, path=reco_path)
ma.matchMCTruth('pi0:kfitwmc', path=reco_path)
ma.variablesToNtuple('pi0:kfitwmc', tuple_vars, filename=outputBelle2ROOTFile, treename = 'dalitz_kfitwmc', path=reco_path)



#make duplicates
#ma.copyParticles('gamma:treefit', 'gamma:conv', path=reco_path)
#ma.copyParticles('gamma:kfit', 'gamma:conv', path=reco_path)
#ma.copyParticles('gamma:rave', 'gamma:conv', path=reco_path)


#vertexing
#ma.vertexTree('gamma:treefit', 0.01, ipConstraint=False, path=reco_path)
#ma.vertexRave('gamma:rave', conf_level=0.01, path=reco_path, silence_warning=True)
#ma.vertexKFit('gamma:kfit', conf_level=0.01, path=reco_path)


#cuts
#ma.applyCuts('gamma:treefit', cuts2, path=reco_path)
#ma.applyCuts('gamma:rave', cuts2, path=reco_path)
#ma.applyCuts('gamma:kfit', cuts2, path=reco_path)

#ma.applyCuts('gamma:rave', cut="delR > -0.15 and delR < 0.15 and delZ > -0.05 and delZ < 0.05 and vtx_rho > 0.8", path=reco_path)

#save trees
#ma.variablesToNtuple('gamma:treefit', tuple_vars, filename=outputBelle2ROOTFile, treename = 'treefit', path=reco_path)
#ma.variablesToNtuple('gamma:rave', tuple_vars, filename=outputBelle2ROOTFile, treename = 'rave', path=reco_path)
#ma.variablesToNtuple('gamma:kfit', tuple_vars, filename=outputBelle2ROOTFile, treename = 'kfit', path=reco_path)


#Without BASF2-vertexing
#ma.applyCuts('gamma:conv', cuts2, path=reco_path)
#ma.variablesToNtuple('gamma:conv', tuple_vars, filename=outputBelle2ROOTFile, treename = 'conv', path=reco_path)

# progress
progress = b2.register_module('Progress')
reco_path.add_module(progress)
b2.process(path=reco_path)
#b2.process(path=reco_path, max_event=500)

# Print call statistics
print(b2.statistics)




