from ROOT import *

f=TFile.Open("output_mc.root","read")
t=f.Get("AK4PFCHS/t")
var=["PUJetId_fullDiscriminant",
"beta","betaClassic","betaStar","betaStarClassic",
"DRweighted",
"dRMatch",
"dZ",
"fRing0","fRing1","fRing2","fRing3","jetR","jetRchg","axisMajor","axisMinor","nCh","nNeutrals","nTot","ptD","pull",
]
for e in t:
  string="pt "+str(e.p4[0].Pt())+", eta "+str(e.p4[0].Eta())
  for v in var:
    string+=", "+v+" "+str(getattr(e,v)[0])
  print string
