# import ROOT in batch mode                                                                                                                                                                                                                  
import sys                                                                                                                                                                                                                                   
oldargv = sys.argv[:]                                                                                                                                                                                                                        
sys.argv = [ '-b-' ]                                                                                                                                                                                                                         
import ROOT                                                                                                                                                                                                                                                                    
ROOT.gROOT.SetBatch(True)                                                                                                                                                                                                                                                      
sys.argv = oldargv                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                               
# load FWLite C++ libraries                                                                                                                                                                                                                                                    
ROOT.gSystem.Load("libFWCoreFWLite.so");                                                                                                                                                                                                                                       
ROOT.gSystem.Load("libDataFormatsFWLite.so");                                                                                                                                                                                                                                  
ROOT.AutoLibraryLoader.enable()                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                               
# load FWlite python libraries                                                                                                                                                                                                                                                 
from DataFormats.FWLite import Handle, Events                                                                                                                                                                                                                                  
from PhysicsTools.HeppyCore.utils.deltar import deltaR
                                                                                                                                                                                                                                                                               
jets, jetLabel = Handle("std::vector<pat::Jet>"), "updatedJets"                                                                                                                                                                                                                
pujetids, pujetidLabel = Handle("edm::ValueMap<StoredPileupJetIdentifier>"), "pileupJetIdUpdated"                                                                                                                                                                                                                
pujetidDiscriminant, pujetidDiscriminantLabel = Handle("edm::ValueMap<float>") , "pileupJetIdUpdated:fullDiscriminant"                                                                                                                                                                                                                                                                                                                                          
pujetidFullId, pujetidFullIdLabel = Handle("edm::ValueMap<int>") , "pileupJetIdUpdated:fullId"                                                                                                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                         
# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)                                                                                                                                                                                                                                                                                               
events = Events("file:patTupleUpdatedFromMiniAOD.root")

Pt2030_Tight   = (0.09,-0.37,-0.24,-0.21)
Pt3050_Tight   = (0.52,-0.19,-0.06,-0.03)
Pt2030_Medium  = (-0.58,-0.52,-0.40,-0.36)
Pt3050_Medium  = (-0.20,-0.39,-0.24,-0.19)
Pt2030_Loose   = (-0.96,-0.62,-0.53,-0.49)
Pt3050_Loose   = (-0.93,-0.52,-0.39,-0.31)   

for bins,ptmin,ptmax in [(Pt2030_Tight,20,30),
(Pt3050_Tight,30,50),
(Pt2030_Medium,20,30),
(Pt3050_Medium,30,50),
(Pt2030_Loose,20,30),
(Pt3050_Loose,30,50),
]:
  print bins,ptmin,ptmax

  efficiencies=[0,0,0,0]
  fakerates=[0,0,0,0]
  numrealjets=[0,0,0,0]
  numpujets=[0,0,0,0]

  for iev,event in enumerate(events):                                                                                                                                                                                                                                                                                                                                                         
    #if iev >= 10: break                                                                                                                                                                                                                                                                                                                                                                     
    event.getByLabel(jetLabel, jets)                                                                                                                                                                                                                                                                                                                                                        
    event.getByLabel(pujetidLabel, pujetids)                                                                                                                                                                                                                                                                                                                                                        
    event.getByLabel(pujetidDiscriminantLabel, pujetidDiscriminant)                                                                                                                                                                                                                                                                                                                                                        
    event.getByLabel(pujetidFullIdLabel, pujetidFullId)                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                            
    #print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                            
    # Jets (standard AK4)
    for i,j in enumerate(jets.product()):
        if j.pt() < 20: continue

        #print "jet %3d: pt %5.1f (raw pt %5.1f, matched-calojet pt %5.1f), eta %+4.2f, pileup mva disc %+.2f" % (
        #    i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.userFloat("caloJetMap:pt"), j.eta(), j.userFloat("pileupJetIdUpdated:fullDiscriminant"))
        #string=""
	#string+="MVA=%.3f, " % (pujetidDiscriminant.product().get(i))
	#variables=['RMS', 'beta', 'betaClassic', 'betaStar', 'betaStarClassic', 'dR2Mean', 'dRMatch', 'dRMean', 'dZ', 'frac01', 'frac02', 'frac03', 'frac04', 'frac05', 'frac06', 'frac07', 'jetEta', 'jetPt', 'jetR', 'jetRchg', 'majW', 'minW', 'nCharged', 'nNeutrals', 'nParticles', 'nTrueInt', 'nvtx', 'ptD', 'pull', 'rho']
	#for var in variables:
	#  string+=var+"=%.3f, " % (getattr(pujetids.product().get(i),var)())
	#print string
	#print pujetidFullId.product().get(i)

        try: pdgId=j.genParton().pdgId()
        except: pdgId=0
        try: genJetMatch=deltaR(j.genJet().eta(),j.genJet().phi(),j.eta(),j.phi())<0.2
        except: genJetMatch=0
        try: genPuJetMatch=deltaR(j.genJet().eta(),j.genJet().phi(),j.eta(),j.phi())>0.5
        except: genPuJetMatch=1
	#print pdgId, genJetMatch, genPuJetMatch
	if genJetMatch:
	    if j.pt()>=ptmin and j.pt()<ptmax:
	      if abs(j.eta())<=2.5:
                 numrealjets[0]+=1
	         efficiencies[0]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[0])
	      if abs(j.eta())>2.5 and abs(j.eta())<=2.75:
                 numrealjets[1]+=1
	         efficiencies[1]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[1])
	      if abs(j.eta())>2.75 and abs(j.eta())<=3:
                 numrealjets[2]+=1
	         efficiencies[2]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[2])
	      if abs(j.eta())>3 and abs(j.eta())<=5:
                 numrealjets[3]+=1
	         efficiencies[3]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[3])
	if genPuJetMatch:
	    print genPuJetMatch
	    if j.pt()>=ptmin and j.pt()<ptmax:
	      if abs(j.eta())<=2.5:
                 numpujets[0]+=1
	         fakerates[0]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[0])
	      if abs(j.eta())>2.5 and abs(j.eta())<=2.75:
                 numpujets[1]+=1
	         fakerates[1]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[1])
	      if abs(j.eta())>2.75 and abs(j.eta())<=3:
                 numpujets[2]+=1
	         fakerates[2]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[2])
	      if abs(j.eta())>3 and abs(j.eta())<=5:
                 numpujets[3]+=1
	         fakerates[3]+=(j.userFloat("pileupJetIdUpdated:fullDiscriminant")>bins[3])

  for bin in range(len(bins)):
    print bin, numrealjets[bin], numpujets[bin]
    efficiencies[bin]/=numrealjets[bin]
    fakerates[bin]/=numpujets[bin]

  print efficiencies
  print fakerates

