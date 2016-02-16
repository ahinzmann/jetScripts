# This configuration is an example that recalibrates the slimmedJets from MiniAOD
# and adds a new userfloat "oldJetMass" to it

import FWCore.ParameterSet.Config as cms

process = cms.Process("PATUPDATE")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(["dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/mc/RunIIFall15MiniAODv2/WprimeToWhToWhadhbb_narrow_M-1000_13TeV-madgraph/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/8EE77064-42B8-E511-8BA1-003048895D40.root"])
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")
process.pileupJetId.jets=cms.InputTag("slimmedJets")
process.pileupJetId.inputIsCorrected=True
process.pileupJetId.applyJec=False
process.pileupJetId.vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")

process.p = cms.Path(process.pileupJetId)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("patTupleUpdated.root"),
    outputCommands = cms.untracked.vstring('keep *')
    )

process.endpath = cms.EndPath(process.out)

