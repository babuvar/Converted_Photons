#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json



#---------------------------------------------------------------
#-------------------    Real Data   ----------------------------
#---------------------------------------------------------------


runlist_buc9  = os.listdir( '/group/belle2/dataprod/Data/PromptReco/bucket9/e0012/4S/GoodRuns' )
runlist_buc10 = os.listdir( '/group/belle2/dataprod/Data/PromptReco/bucket10/e0012/4S/GoodRuns')
runlist_buc11 = os.listdir( '/group/belle2/dataprod/Data/PromptReco/bucket11/e0012/4S/GoodRuns')
runlist_buc12 = os.listdir( '/group/belle2/dataprod/Data/PromptReco/bucket12/e0012/4S_offres/GoodRuns')
runlist_buc13 = os.listdir( '/group/belle2/dataprod/Data/PromptReco/bucket13/e0012/4S/GoodRuns')


buckets = {
            "bucket9" : { "energy"    : "4S",
                          "runlist"   : runlist_buc9,
                          "globalTag" : "data_reprocessing_prompt"},

	    "bucket10" : { "energy"    : "4S",
			  "runlist"   : runlist_buc10,
                          "globalTag" : "data_reprocessing_prompt"},

            "bucket11" : { "energy"    : "4S",
                          "runlist"   : runlist_buc11,
                          "globalTag" : "data_reprocessing_prompt"},

            "bucket12" : { "energy"    : "4S_offres",
                          "runlist"   : runlist_buc12,
                          "globalTag" : "data_reprocessing_prompt_bucket12_baseline"},

            "bucket13" : { "energy"    : "4S",
                          "runlist"   : runlist_buc13,
                          "globalTag" : "data_reprocessing_prompt"}
}

exp='e0012'; 

for bucket, specs in buckets.items():

	energy    = specs['energy']
	runlist   = specs['runlist']
	globalTag = specs['globalTag']

	for run in runlist:
	
		filename='data_%s_%s_%s'%(exp,energy,run)
		input_dir='/group/belle2/dataprod/Data/PromptReco/%s/%s/%s/%s/skim/hlt_hadron/mdst/sub00/'%(bucket,exp,energy,run)

		os.system('bsub -q l -oo log/Data_2020/%s.log  basf2 -l INFO reco_congam.py Data  %s  root/Data_2020/%s.root %s' %(filename, input_dir, filename, globalTag))
		#os.system('bsub -q s -oo log/Data_2020/%s.log  basf2 -l INFO reco_congam.py Data  %s  root/Data_2020/%s.root %s' %(filename, input_dir, filename, globalTag))

#---------------------------------------------------------------
#-------------------    Real Data   ----------------------------
#---------------------------------------------------------------











