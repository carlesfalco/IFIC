import AnalysisHelpers as AH
import ROOT
import Analysis

#======================================================================
        
class TTbarAnalysis(Analysis.Analysis):
  """Semileptonic TTbarAnalysis loosely based on the ATLAS analyses of top pair events where 
  one W boson decays to leptons and one decays to hadrons.
  """
  def __init__(self, store):
    super(TTbarAnalysis, self).__init__(store)
  
  def initialize(self):
      self.hist_WtMass      =  self.addStandardHistogram("WtMass")
      self.hist_TopMassRecbefore      =  self.addStandardHistogram("TopMassRecbefore")
      self.hist_WtMassRecbefore      =  self.addStandardHistogram("WtMassRecbefore")
      self.hist_WtMassRec      =  self.addStandardHistogram("WtMassRec")

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
      self.hist_jetspt      =  self.addStandardHistogram("jet_pt")       
      self.hist_jetm        =  self.addStandardHistogram("jet_m")        
      self.hist_jetJVT      =  self.addStandardHistogram("jet_jvt")      
      self.hist_jeteta      =  self.addStandardHistogram("jet_eta")      
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
      if not len(goodJets) >= 4: return False
      self.countEvent("Jets", weight)

      # apply the b-tagging requirement using the MV2c10 algorithm at 80% efficiency
      btags = sum([1 for jet in goodJets if jet.mv2c10() > 0.7892])
      if not (btags >= 2): return False
      self.countEvent("btags", weight)

      # apply a cut on the transverse mass of the W boson decaying to leptons
      if not (AH.WTransverseMass(leadlepton, etmiss) > 30.0): return False

      #Chossing pt
      ptmax2 = goodJets[0].pt()
      ptmax3 = -999
      jetsrec=[goodJets[0],goodJets[0],goodJets[0]]
      jetsrec2=[goodJets[0],goodJets[0]]
      for i in range(0,len(goodJets)-1):
        for j in range(i+1,len(goodJets)-1):
          for k in range(j+1,len(goodJets)-1):
            if ( ( goodJets[i].tlv() + goodJets[j].tlv() + goodJets[k].tlv() ).Pt() > ptmax3 ):
              ptmax3 = ( goodJets[i].tlv() + goodJets[j].tlv() + goodJets[k].tlv() ).Pt()
              jetsrec =[goodJets[i],goodJets[j],goodJets[k]]
      for l in range(0,2):
        for m in range(l+1,2):
          if ( ( jetsrec[l].tlv()+jetsrec[m].tlv() ).Pt()>ptmax2 ):
              ptmax2 =  ( jetsrec[l].tlv()+jetsrec[m].tlv() ).Pt()
              jetsrec2 = [jetsrec[l],jetsrec[m]]
      wrec = jetsrec2[0].tlv()+jetsrec2[1].tlv()
      toprec = jetsrec[0].tlv()+jetsrec[1].tlv()+jetsrec[2].tlv()
      self.hist_TopMassRecbefore.Fill(toprec.M(),weight)
      self.hist_WtMassRecbefore.Fill(wrec.M(),weight)

      #Applying cut
      if (wrec.M()-10<70 or wrec.M()+10>90):
        return False
      self.hist_WtMassRec.Fill(wrec.M(),weight)
      # Histograms detailing event information
      self.hist_vxp_z.Fill(eventinfo.primaryVertexPosition(), weight)
      self.hist_pvxp_n.Fill(eventinfo.numberOfVertices(), weight)

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
