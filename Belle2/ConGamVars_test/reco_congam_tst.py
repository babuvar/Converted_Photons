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
from variables import variables as vm

#General
path = b2.create_path()


#Get job-parameters
data_kind=str(sys.argv[1])

if data_kind == 'GMC':

	#Input files
	files_str=sys.argv[2]
	files = files_str.split(",")
	outputBelle2ROOTFile=str(sys.argv[3])
	globalTag = 'MC'

#root input
ma.inputMdstList(environmentType='default', filelist=files, path=path)

#reconstruction
vm.addAlias('cpDR','convertedPhotonDelR(0,1)')
vm.addAlias('cpDZ','convertedPhotonDelZ(0,1)')
vm.addAlias('cpDTL','convertedPhotonDelTanLambda(0,1)')
vm.addAlias('cpX','convertedPhotonX(0,1)')
vm.addAlias('cpY','convertedPhotonY(0,1)')
vm.addAlias('cpZ','convertedPhotonZ(0,1)')
vm.addAlias('cpRho','convertedPhotonRho(0,1)')
vm.addAlias('cpM','convertedPhotonInvariantMass(0,1)')
vm.addAlias('cpPx','convertedPhotonPx(0,1)')
vm.addAlias('cpPy','convertedPhotonPy(0,1)')
vm.addAlias('cpPz','convertedPhotonPz(0,1)')

vm.addAlias('mcX','daughter(0,mcProductionVertexX)')
vm.addAlias('mcY','daughter(0,mcProductionVertexY)')
vm.addAlias('mcZ','daughter(0,mcProductionVertexZ)')


#tuple variables
tuple_vars = ['cpDR', 'cpDZ', 'cpDTL', 'cpX', 'cpY', 'cpZ', 'cpRho', 'cpM', 'cpPx', 'cpPy', 'cpPz', 'isSignal', 'isSignalAcceptBremsPhotons', 'isSignalAcceptMissing', 'isSignalAcceptMissingGamma', 'mcX', 'mcY','mcZ','mcPX', 'mcPY', 'mcPZ']


ma.fillParticleList("e+:loose", cut="p > 0.3", path=path)
ma.reconstructDecay('gamma:conv -> e+:loose e-:loose', cut='cpM < 0.2 and cpDR > -0.15 and cpDR < 0.15 and cpDZ > -0.05 and cpDZ < 0.05', path=path)
ma.matchMCTruth('gamma:conv', path=path)
ma.variablesToNtuple('gamma:conv', tuple_vars, filename=outputBelle2ROOTFile, treename = 'photonVars', path=path)


# progress
progress = b2.register_module('Progress')
path.add_module(progress)
b2.process(path=path, max_event=80000)

# Print call statistics
print(b2.statistics)





