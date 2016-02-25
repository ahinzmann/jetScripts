# This configuration is an example that recalibrates the slimmedJets from MiniAOD
# and adds a new userfloat "oldJetMass" to it

import FWCore.ParameterSet.Config as cms

process = cms.Process("PATUPDATE")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(["/store/relval/CMSSW_7_6_2/RelValZMM_13/MINIAODSIM/PU25ns_76X_mcRun2_asymptotic_v12-v1/00000/C86BA73E-D09C-E511-AD68-002590596468.root"])
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

from CondCore.DBCommon.CondDBSetup_cfi import *
import os
era = "Fall15_25nsV2_MC"
dBFile = era+".db"
print "\nUsing private SQLite file", dBFile, "\n"
process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
    		connect = cms.string( "sqlite_file:"+dBFile ),
    		toGet =  cms.VPSet(
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PF"),
    				label= cms.untracked.string("AK4PF")
    				),
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFchs"),
    				label= cms.untracked.string("AK4PFchs")
    				),
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK4PFPuppi"),
    				label= cms.untracked.string("AK4PFPuppi")
    				),
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PF"),
    				label= cms.untracked.string("AK8PF")
    				),
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PFchs"),
    				label= cms.untracked.string("AK8PFchs")
    				),
    			cms.PSet(
    				record = cms.string("JetCorrectionsRecord"),
    				tag = cms.string("JetCorrectorParametersCollection_"+era+"_AK8PFPuppi"),
    				label= cms.untracked.string("AK8PFPuppi")
    				),
    			)
    		)

process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')

process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetId.jets=cms.InputTag("slimmedJets")
process.pileupJetId.inputIsCorrected=True
process.pileupJetId.applyJec=True
process.pileupJetId.vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")
print process.pileupJetId.dumpConfig()

process.p = cms.Path(process.pileupJetId)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("patTuplePuIdFromMiniAOD.root"),
    outputCommands = cms.untracked.vstring('keep *')
    )

process.endpath = cms.EndPath(process.out)

