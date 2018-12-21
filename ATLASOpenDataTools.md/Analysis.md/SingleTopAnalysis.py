import AnalysisHelpers as AH
import ROOT
import Analysis

#======================================================================
        
class SingleTopAnalysis(Analysis.Analysis):
  """Semileptonic SingleTopAnalysis loosely based on the ATLAS analyses of top pair events where 
  one W boson decays to leptons and one decays to hadrons.
  """
  def __init__(self, store):
    super(SingleTopAnalysis, self).__init__(store)
  
  def initialize(self):
      self.hist_WtMass      =  self.addStandardHistogram("WtMass")
      self.hist_SingleTopMass  =  self.addStandardHistogram("SingleTopMass")
      self.hist_SingleTopMassbefore  =  self.addStandardHistogram("SingleTopMassbefore")

      self.hist_leptn       =  self.addStandardHistogram("lep_n")
      self.hist_leptpt      =  self.addStandardHistogram("lep_pt")
      self.hist_lepteta     =  self.addStandardHistogram("lep_eta")
      self.hist_leptE       =  self.addStandardHistogram("lep_E")
      self.hist_leptphi     =  self.addStandardHistogram("lep_phi")
      self.hist_leptch      =  self.addStandardHistogram("lep_charge")
      self.hist_leptID      =  self.addStandardHistogram("lep_type")
      self.hist_leptptc     =  self.addStandardHistogram("lep_ptconerel30")
      self.hist_leptetc     =  self.addStandardHistogram("lep_etconerel20")
      self.hist_lepz0       =  self.addStandardHistogram("lep_z0")
      self.hist_lepd0       =  self.addStandardHistogram("lep_d0")

      self.hist_njets       =  self.addStandardHistogram("n_jets")  
      self.hist_njetsbefore       =  self.addStandardHistogram("n_jetsbefore")
      self.hist_jetspt      =  self.addStandardHistogram("jet_pt")       
      self.hist_jetm        =  self.addStandardHistogram("jet_m")        
      self.hist_jetJVT      =  self.addStandardHistogram("jet_jvt")      
      self.hist_jeteta      =  self.addStandardHistogram("jet_eta")
      self.hist_deltaeta      =  self.addStandardHistogram("delta_eta") 
      self.hist_leta      =  self.addStandardHistogram("jet_leta")
      self.hist_ht      =  self.addStandardHistogram("ht") 
      self.hist_deltaetabefore      =  self.addStandardHistogram("delta_etabefore") 
      self.hist_letabefore      =  self.addStandardHistogram("jet_letabefore")
      self.hist_htbefore      =  self.addStandardHistogram("htbefore")    
      self.hist_jetmv2c10   =  self.addStandardHistogram("jet_MV2c10")     
      self.hist_jetphi      =  self.addStandardHistogram("jet_phi")

      self.hist_etmiss      = self.addStandardHistogram("etmiss")
      self.hist_vxp_z       = self.addStandardHistogram("vxp_z")
      self.hist_pvxp_n      = self.addStandardHistogram("pvxp_n")
  
  
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1
      self.countEvent("all", weight)

      # apply standard event based selection
      if not AH.StandardEventCuts(eventinfo): return False
      self.countEvent("EventCuts", weight)

      # neutrinos are expected, so cut on missing transverse momentum
      etmiss = self.Store.getEtMiss()
      if not (etmiss.et() > 30.0): return False
      self.countEvent("MET", weight)
      
      # one good lepton from one of the W boson decays is expected, so require exactly one good lepton
      goodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), AH.isGoodLepton, lambda p: p.pt())
      if not (len(goodLeptons) == 1): return False
      self.countEvent("1 Lepton", weight)

      leadlepton = goodLeptons[0]
      
      # two jets from one of the W boson decays as well as two b-jets from the top pair decays are expected
      goodJets = AH.selectAndSortContainer(self.Store.getJets(), AH.isGoodJet, lambda p: p.pt())
      if not len(goodJets) == 2: return False
      self.countEvent("Jets", weight)

      leadjet = goodJets[0]

      # apply the b-tagging requirement using the MV2c10 algorithm at 80% efficiency
      btags = sum([1 for jet in goodJets if jet.mv2c10() > 0.7892])
      if not (btags == 1): return False
      self.countEvent("btags", weight)


      for jet in goodJets:
        if jet.mv2c10()>0.7892:
          bjet = jet
        else: lightjet = jet

      # apply a cut on the transverse mass of the W boson decaying to leptons
      if not (AH.WTransverseMass(leadlepton, etmiss) > 50.0): return False

      Pi = 3.1416
      leptoniso = leadlepton.pt() / ( 1 - ((Pi - abs(leadlepton.tlv().DeltaPhi(leadjet.tlv())) )/(Pi-1) ))
     # if not ( leptoniso > 40.0 ): return False

      # calculate top mass
      mtop = AH.SingleTopMassSebas(leadlepton,etmiss,bjet)
      #if mtop>0 :  
      self.hist_SingleTopMassbefore.Fill(mtop, weight)

      # New parameters
      deltaeta = abs(bjet.eta()-lightjet.eta())
      ht = leadlepton.pt()+lightjet.pt()+bjet.pt()+etmiss.et()

      # Histograms before cuts
      self.hist_njetsbefore.Fill(len(goodJets), weight)
      self.hist_letabefore.Fill(lightjet.eta(), weight)
      self.hist_deltaetabefore.Fill(deltaeta, weight)
      self.hist_htbefore.Fill(ht,weight)

      #3. 130 < mtop < 200
      if not ( 150 < mtop and  mtop < 220 ):
        return False
      self.hist_SingleTopMass.Fill(mtop, weight)
      
      #1. abs(eta)>1.7
      if not ( abs(lightjet.eta()) > 1.5 ):
        return False
      self.hist_leta.Fill(lightjet.eta(), weight)

      #2. delta > 1.5
      if not ( deltaeta > 1.5):
        return False
      self.hist_deltaeta.Fill(deltaeta, weight)

      #4. ht > 195
      if not ( ht > 195):
        return False
      self.hist_ht.Fill(ht,weight)  

      # Histograms detailing event information
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)

      #Extra histograms
    

      # histograms for the W boson properties
      self.hist_WtMass.Fill(AH.WTransverseMass(leadlepton, etmiss), weight)

      # histograms for missing et
      self.hist_etmiss.Fill(etmiss.et(),weight)  

      # histograms detailing lepton information
      self.hist_leptn.Fill(len(goodLeptons), weight)
      self.hist_leptpt.Fill(leadlepton.pt(), weight)
      self.hist_lepteta.Fill(leadlepton.eta(), weight)
      self.hist_leptE.Fill(leadlepton.e(), weight)
      self.hist_leptphi.Fill(leadlepton.phi(), weight)
      self.hist_leptch.Fill(leadlepton.charge(), weight)
      self.hist_leptID.Fill(leadlepton.pdgId(), weight)
      self.hist_lepz0.Fill(leadlepton.z0(), weight)
      self.hist_lepd0.Fill(leadlepton.d0(), weight)      
      self.hist_leptptc.Fill(leadlepton.isoptconerel30(), weight)
      self.hist_leptetc.Fill(leadlepton.isoetconerel20(), weight)
      
      # histograms detailing jet information
      self.hist_njets.Fill(len(goodJets), weight)
      [self.hist_jetm.Fill(jet.m(), weight) for jet in goodJets]
      [self.hist_jetspt.Fill(jet.pt(), weight) for jet in goodJets]
      [self.hist_jetJVT.Fill(jet.jvt(), weight) for jet in goodJets]
      [self.hist_jeteta.Fill(jet.eta(), weight) for jet in goodJets]
      [self.hist_jetmv2c10.Fill(jet.mv2c10(), weight) for jet in goodJets] 
      [self.hist_jetphi.Fill(jet.phi(), weight) for jet in goodJets]
      return True

  def finalize(self):
      pass
