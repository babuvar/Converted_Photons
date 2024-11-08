#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import basf2 as b2
#from basf2 import *
import modularAnalysis as ma
#from modularAnalysis import *
from b2biiConversion import convertBelleMdstToBelleIIMdst, setupB2BIIDatabase
import json
import mdst_tools as mt


#General
os.environ['USE_GRAND_REPROCESS_DATA'] = '1'
reco_path = b2.create_path()

#if len(sys.argv) != 5:
#    sys.exit('Must provide two input parameters: [mc|data] [input_Belle_MDST_file][output_BelleII_ROOT_file].')

#Flag that determines which modes to reconstruct
rec_flag=int(sys.argv[1])
split_flags=list('{0:0b}'.format(rec_flag))

#MC or data?
mc_or_data = sys.argv[2].lower()
isMC = {"mc": True, "data": False}.get(mc_or_data, None)
if isMC is None:
    sys.exit('First parameter must be "mc" or "data" to indicate whether we run on MC or real data')
setupB2BIIDatabase(isMC)

if mc_or_data == 'mc':
        mc_kind=sys.argv[3].lower()
        #Deal with signal-MC
        if mc_kind == 'signal':
                input_dir = sys.argv[4]
                outputBelle2ROOTFile = sys.argv[5]

                inputBelleMDSTFiles=[]
                for filename in os.listdir(input_dir):
                        #if '55' in filename:
                        inputBelleMDSTFiles.append('%s/%s'%(input_dir,filename))
        
        #Deal with generic-MC
        if mc_kind == 'generic':
                expNo = sys.argv[4]
                startRun = sys.argv[5]
                endRun = sys.argv[6]
                eventType = sys.argv[7]
                dataType = sys.argv[8]
                belleLevel = sys.argv[9]
                streamNo = sys.argv[10]
                outputBelle2ROOTFile = sys.argv[11]
                inputBelleMDSTFiles = mt.getBelleMdst_mc(expNo, startRun, endRun, eventType, dataType, belleLevel, streamNo)

#print(outputBelle2ROOTFile)
#print(inputBelleMDSTFiles)



#Convert Belle -> BelleII
convertBelleMdstToBelleIIMdst(inputBelleMDSTFiles, applyHadronBJSkim=True, path=reco_path)



# Reconstruction



#variable dictionary
var_dict = json.load(open("variables_congam.json"))
tuple_vars = []

for key, val in var_dict['congam_vars'].items():
        ma.variables.addAlias('%s' % key, '%s' % val)
        tuple_vars += ['%s' % key]



#FSPs: get all tracks
#ma.fillParticleList('e+:all', '', path=reco_path)

cuts='InvM < 0.3 and X > -20 and X < 20 and Y > -20 and Y < 20 and e1_mom > 0.3 and e2_mom > 0.3 and e1_PID > 0.4 and e2_PID > 0.4'

#Reconstruct D -> pi0 e e 
if int(split_flags[1]) == 1:
        
        # Reconstruct photons that convert to e+e- and do a vertex fit. InvM determined from daughter
        #ma.fillConvertedPhotonsList('gamma:const -> e+:loose e-:loose', 'InvM < 0.3', path=reco_path) 
        #ma.copyList('gamma:doubleconst', 'gamma:const', path=reco_path)
        #ma.vertexTree('gamma:converted', 0.01, ipConstraint=False, massConstraint=[-11 ,11], path=reco_path)
        
        #ma.vertexTree('gamma:const', 0.001, ipConstraint=False, massConstraint=[22], path=reco_path)
        #ma.vertexTree('gamma:doubleconst', 0.001, ipConstraint=False, massConstraint=[22,-11,11], path=reco_path)
        #ma.matchMCTruth('gamma:const', path=reco_path)
        #ma.matchMCTruth('gamma:doubleconst', path=reco_path)
        #ma.variablesToNtuple('gamma:const', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree1', path=reco_path)
        #ma.variablesToNtuple('gamma:doubleconst', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree2', path=reco_path)

        #ma.matchMCTruth('gamma:v0mdst', path=reco_path)
        #ma.vertexTree('gamma:v0mdst', 0.001, ipConstraint=False, massConstraint=[22,-11,11], path=reco_path)
        #ma.variablesToNtuple('gamma:v0mdst', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree1', path=reco_path)



	ma.fillConvertedPhotonsList('gamma:conv -> e+:loose e-:loose', cuts, path=reco_path)
	ma.matchMCTruth('gamma:conv', path=reco_path)

	ma.copyList('gamma:const1', 'gamma:conv', path=reco_path)
	ma.copyList('gamma:const2', 'gamma:conv', path=reco_path)

	ma.vertexTree('gamma:const1', -1.1, ipConstraint=False, path=reco_path)
	ma.vertexTree('gamma:const2', -1.1, ipConstraint=False, massConstraint=[22], path=reco_path)

	ma.variablesToNtuple('gamma:const1', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree1', path=reco_path)
	ma.variablesToNtuple('gamma:const2', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree2', path=reco_path)




'''
	ma.matchMCTruth('gamma:v0mdst', path=reco_path)
	ma.copyList('gamma:noconst', 'gamma:v0mdst', path=reco_path)
	ma.copyList('gamma:1const', 'gamma:v0mdst', path=reco_path)
	ma.copyList('gamma:2const', 'gamma:v0mdst', path=reco_path)
	ma.variablesToNtuple('gamma:noconst', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree1', path=reco_path)
	ma.vertexTree('gamma:1const', 0.001, ipConstraint=False, massConstraint=[22], path=reco_path)
	ma.variablesToNtuple('gamma:1const', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree2', path=reco_path)
	ma.vertexTree('gamma:2const', 0.001, ipConstraint=False, massConstraint=[22,-11,11], path=reco_path)
	ma.variablesToNtuple('gamma:2const', tuple_vars, filename=outputBelle2ROOTFile, treename = 'tree3', path=reco_path)
'''

# progress
progress = b2.register_module('Progress')
reco_path.add_module(progress)
b2.process(path=reco_path)

# Print call statistics
print(b2.statistics)






