
#include "SexaQAnalysis/AnalyzerAllSteps/src/AnalyzerAllSteps.cc"
#include "SexaQAnalysis/Skimming/plugins/FiducialCuts.h"


FiducialCuts::FiducialCuts(edm::ParameterSet const& pset):
  lambdaCollectionTag_(pset.getParameter<edm::InputTag>("lambdaCollection")),
  kshortCollectionTag_(pset.getParameter<edm::InputTag>("kshortCollection")),
  //genCollectionTag_   (pset.getParameter<edm::InputTag>("genCollection")),
  bsCollectionTag_    (pset.getParameter<edm::InputTag>("beamspot")),
  PVCollectionTag_    (pset.getParameter<edm::InputTag>("offlinePV")),
  //isData_       (pset.getParameter<bool>  ("isData")),
  //doFiducialCuts_(pset.getParameter<bool>("doFiducialCuts")),
  minNrLambda_  (pset.getParameter<unsigned int>("minNrLambda")),
  minNrKshort_  (pset.getParameter<unsigned int>("minNrKshort")),
  minPtLambda_  (pset.getParameter<double>("minPtLambda")),
  minPtKshort_  (pset.getParameter<double>("minPtKshort")),
  maxEtaLambda_ (pset.getParameter<double>("maxEtaLambda")),
  maxEtaKshort_ (pset.getParameter<double>("maxEtaKshort")),
  minMassLambda_(pset.getParameter<double>("minMassLambda")),
  minMassKshort_(pset.getParameter<double>("minMassKshort")),
  maxMassLambda_(pset.getParameter<double>("maxMassLambda")),
  maxMassKshort_(pset.getParameter<double>("maxMassKshort")),
  //checkLambdaDaughters_(pset.getParameter<bool>("checkLambdaDaughters")),
//Fiducial cuts
  maxVzDecayLambda_(pset.getParameter<double>("maxVzDecayLambda")),
  maxVzDecayKshort_(pset.getParameter<double>("maxVzDecayKshort")),
  maxLxyDecayLambda_(pset.getParameter<double>("maxLxyDecayLambda")),
  maxLxyDecayKshort_(pset.getParameter<double>("maxLxyDecayKshort")),
  minPTLambdaDau0_(pset.getParameter<double>("minPTLambdaDau0")),
  minPTLambdaDau1_(pset.getParameter<double>("minPTLambdaDau1")),
  minPTKshortDau0_(pset.getParameter<double>("minPTKshortDau0")),
  minPTKshortDau1_(pset.getParameter<double>("minPTKshortDau1")),
  maxPzLambdaDau0_(pset.getParameter<double>("maxPzLambdaDau0")),
  maxPzLambdaDau1_(pset.getParameter<double>("maxPzLambdaDau1")),
  maxPzKshortDau0_(pset.getParameter<double>("maxPzKshortDau0")),
  maxPzKshortDau1_(pset.getParameter<double>("maxPzKshortDau1")),
  minD0xyBeamspotLambdaDau0_(pset.getParameter<double>("minD0xyBeamspotLambdaDau0")),
  minD0xyBeamspotLambdaDau1_(pset.getParameter<double>("minD0xyBeamspotLambdaDau1")),
  minD0xyBeamspotKshortDau0_(pset.getParameter<double>("minD0xyBeamspotKshortDau0")),
  minD0xyBeamspotKshortDau1_(pset.getParameter<double>("minD0xyBeamspotKshortDau1")),
  maxD0xyBeamspotLambdaDau0_(pset.getParameter<double>("maxD0xyBeamspotLambdaDau0")),
  maxD0xyBeamspotLambdaDau1_(pset.getParameter<double>("maxD0xyBeamspotLambdaDau1")),
  maxD0xyBeamspotKshortDau0_(pset.getParameter<double>("maxD0xyBeamspotKshortDau0")),
  maxD0xyBeamspotKshortDau1_(pset.getParameter<double>("maxD0xyBeamspotKshortDau1")),
  maxDzMinPVLambdaDau0_(pset.getParameter<double>("maxDzMinPVLambdaDau0")),
  maxDzMinPVLambdaDau1_(pset.getParameter<double>("maxDzMinPVLambdaDau1")),
  maxDzMinPVKshortDau0_(pset.getParameter<double>("maxDzMinPVKshortDau0")),
  maxDzMinPVKshortDau1_(pset.getParameter<double>("maxDzMinPVKshortDau1")),
  prescaleFalse_(pset.getParameter<unsigned int>("prescaleFalse"))
{
  lambdaCollectionToken_ = consumes<std::vector<reco::VertexCompositeCandidate> >(lambdaCollectionTag_);
  kshortCollectionToken_ = consumes<std::vector<reco::VertexCompositeCandidate> >(kshortCollectionTag_);
  //genCollectionToken_    = consumes<std::vector<reco::GenParticle> >             (genCollectionTag_);
  bsCollectionToken_    = consumes<reco::BeamSpot>                               (bsCollectionTag_);
  PVCollectionToken_    = consumes<std::vector<reco::Vertex> >                   (PVCollectionTag_);
  nreject_ = 0;
  produces<reco::CandidatePtrVector>("kshort");
  produces<reco::CandidatePtrVector>("lambda");
}


bool FiducialCuts::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
{
  auto kshorts = std::make_unique<reco::CandidatePtrVector>();
  auto lambdas = std::make_unique<reco::CandidatePtrVector>();

  // select on reco lambdas and kaons
  //if (isData_) {
    // read out lambdas
    edm::Handle<std::vector<reco::VertexCompositeCandidate> > h_lambda;
    iEvent.getByToken(lambdaCollectionToken_, h_lambda);
    if(!h_lambda.isValid()) {
      std::cout << "Missing collection during Fiducial Cuts: " << lambdaCollectionTag_ << " ... skip entry !" << std::endl;
      return false;
    }
    // read out kaons
    edm::Handle<std::vector<reco::VertexCompositeCandidate> > h_kshort;
    iEvent.getByToken(kshortCollectionToken_ , h_kshort);
    if(!h_kshort.isValid()) {
      std::cout << "Missing collection during Fiducial Cuts: " << kshortCollectionTag_ << " ... skip entry !" << std::endl;
      return false;
    }
    // beamspot
    edm::Handle<reco::BeamSpot> h_bs;
    iEvent.getByToken(bsCollectionToken_ , h_bs);
    if(!h_bs.isValid()) {
      std::cout << "Missing collection during Fiducial Cuts: " << bsCollectionTag_ << " ... skip entry !" << std::endl;
      return false;
    }
    TVector3 beamspot(h_bs->x0(),h_bs->y0(),h_bs->z0());
    // beamspot
    edm::Handle<std::vector<reco::Vertex>> h_offlinePV;
    iEvent.getByToken(PVCollectionToken_ , h_offlinePV);
    if(!h_offlinePV.isValid()) {
      std::cout << "Missing collection during Fiducial Cuts: " << PVCollectionTag_ << " ... skip entry !" << std::endl;
      return false;
    }
    // select the lambdas passing kinematic cuts
    for (unsigned int l = 0; l < h_lambda->size(); ++l) {
      const reco::VertexCompositeCandidate* Lambda_l = &h_lambda->at(l);
      if (Lambda_l->pt()       > minPtLambda_   &&
          fabs(Lambda_l->eta()) < maxEtaLambda_ &&
          Lambda_l->mass()     > minMassLambda_ &&
          Lambda_l->mass()     < maxMassLambda_) {
    //Fiducial cuts on the Lambda
        bool LambdaPassedFiducial = false;
        //if(doFiducialCuts_){
            TVector3 LambdaCreationVertex(Lambda_l->vx(),Lambda_l->vy(),Lambda_l->vz());
            TVector3 LambdaMomentum(Lambda_l->px(),Lambda_l->py(),Lambda_l->pz());
            if ( 
                 (fabs(LambdaCreationVertex.Z() - beamspot.Z()) <= maxVzDecayLambda_)
              && (AnalyzerAllSteps::lxy(beamspot,LambdaCreationVertex) <= maxLxyDecayLambda_)
              && (Lambda_l->numberOfDaughters() >= 2 )
                ) {
    //Fiducial cuts on Lambda Daughters
                TVector3 Lambda_daughter0Momentum(Lambda_l->daughter(0)->px(),Lambda_l->daughter(0)->py(),Lambda_l->daughter(0)->pz());
                TVector3 Lambda_daughter1Momentum(Lambda_l->daughter(1)->px(),Lambda_l->daughter(1)->py(),Lambda_l->daughter(1)->pz());
                TVector3 Lambda_daughter0CreationVertex(Lambda_l->daughter(0)->vx(),Lambda_l->daughter(0)->vy(),Lambda_l->daughter(0)->vz());
                TVector3 Lambda_daughter1CreationVertex(Lambda_l->daughter(1)->vx(),Lambda_l->daughter(1)->vy(),Lambda_l->daughter(1)->vz());
                TVector3 bestPVdzLambda = AnalyzerAllSteps::dz_line_point_min(LambdaCreationVertex, LambdaMomentum, h_offlinePV);
                if ( 
                     (Lambda_l->daughter(0)->pt() >= minPTLambdaDau0_ )
                  && (Lambda_l->daughter(1)->pt() >= minPTLambdaDau1_ )
                  && (fabs(Lambda_l->daughter(0)->pz()) <= maxPzLambdaDau0_ )
                  && (fabs(Lambda_l->daughter(1)->pz()) <= maxPzLambdaDau1_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Lambda_daughter0CreationVertex, Lambda_daughter0Momentum, beamspot) >= minD0xyBeamspotLambdaDau0_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Lambda_daughter1CreationVertex, Lambda_daughter1Momentum, beamspot) >= minD0xyBeamspotLambdaDau1_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Lambda_daughter0CreationVertex, Lambda_daughter0Momentum, beamspot) <= maxD0xyBeamspotLambdaDau0_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Lambda_daughter1CreationVertex, Lambda_daughter1Momentum, beamspot) <= maxD0xyBeamspotLambdaDau1_ )
                  && (fabs(AnalyzerAllSteps::dz_line_point(Lambda_daughter0CreationVertex, Lambda_daughter0Momentum, bestPVdzLambda)) <= maxDzMinPVLambdaDau0_ )
                  && (fabs(AnalyzerAllSteps::dz_line_point(Lambda_daughter1CreationVertex, Lambda_daughter1Momentum, bestPVdzLambda)) <= maxDzMinPVLambdaDau1_ )
                    ) {
                    LambdaPassedFiducial = true;
                }
            }
        //} else {
        //    LambdaPassedFiducial = true;
        //}
        if (LambdaPassedFiducial) {
            edm::Ptr<reco::VertexCompositeCandidate> lptr(h_lambda,l);
            lambdas->push_back(std::move(lptr));
        } 
        //else{
        //std::cout<< "Lambda failed Fiducial cuts" << std::endl;
        //}
      }
    }

    // select the kshorts passing kinematic cuts and non-overlapping with lambdas
    for (unsigned int k = 0; k < h_kshort->size(); ++k) {
      const reco::VertexCompositeCandidate* Kshort_k = &h_kshort->at(k);
      if (Kshort_k->pt()       > minPtKshort_   &&
          fabs(Kshort_k->eta()) < maxEtaKshort_ &&
          Kshort_k->mass()     > minMassKshort_ &&
          Kshort_k->mass()     < maxMassKshort_) {
        bool KsPassedFiducial = false;
    //Fiducial cuts on Kshort
        //if(doFiducialCuts_){
            TVector3 KshortCreationVertex(Kshort_k->vx(),Kshort_k->vy(),Kshort_k->vz());
            TVector3 KshortMomentum(Kshort_k->px(),Kshort_k->py(),Kshort_k->pz());
            if ( 
                 (fabs(KshortCreationVertex.Z() - beamspot.Z()) <= maxVzDecayKshort_)
              && (AnalyzerAllSteps::lxy(beamspot,KshortCreationVertex) <= maxLxyDecayKshort_)
              //&& (Kshort_k->numberOfDaughters() >= 2 )
                ) {
    //Fiducial cuts on Kshort Daughters
                TVector3 Kshort_daughter0Momentum(Kshort_k->daughter(0)->px(),Kshort_k->daughter(0)->py(),Kshort_k->daughter(0)->pz());
                TVector3 Kshort_daughter1Momentum(Kshort_k->daughter(1)->px(),Kshort_k->daughter(1)->py(),Kshort_k->daughter(1)->pz());
                TVector3 Kshort_daughter0CreationVertex(Kshort_k->daughter(0)->vx(),Kshort_k->daughter(0)->vy(),Kshort_k->daughter(0)->vz());
                TVector3 Kshort_daughter1CreationVertex(Kshort_k->daughter(1)->vx(),Kshort_k->daughter(1)->vy(),Kshort_k->daughter(1)->vz());
                TVector3 bestPVdzKshort = AnalyzerAllSteps::dz_line_point_min(KshortCreationVertex, KshortMomentum, h_offlinePV);
                if ( 
                     (Kshort_k->daughter(0)->pt() >= minPTKshortDau0_ )
                  && (Kshort_k->daughter(1)->pt() >= minPTKshortDau1_ )
                  && (fabs(Kshort_k->daughter(0)->pz()) <= maxPzKshortDau0_ )
                  && (fabs(Kshort_k->daughter(1)->pz()) <= maxPzKshortDau1_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Kshort_daughter0CreationVertex, Kshort_daughter0Momentum, beamspot) >= minD0xyBeamspotKshortDau0_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Kshort_daughter1CreationVertex, Kshort_daughter1Momentum, beamspot) >= minD0xyBeamspotKshortDau1_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Kshort_daughter0CreationVertex, Kshort_daughter0Momentum, beamspot) <= maxD0xyBeamspotKshortDau0_ )
                  && (AnalyzerAllSteps::dxy_signed_line_point(Kshort_daughter1CreationVertex, Kshort_daughter1Momentum, beamspot) <= maxD0xyBeamspotKshortDau1_ )
                  && (fabs(AnalyzerAllSteps::dz_line_point(Kshort_daughter0CreationVertex, Kshort_daughter0Momentum, bestPVdzKshort)) <= maxDzMinPVKshortDau0_ )
                  && (fabs(AnalyzerAllSteps::dz_line_point(Kshort_daughter1CreationVertex, Kshort_daughter1Momentum, bestPVdzKshort)) <= maxDzMinPVKshortDau1_ )
                    ) {
                    KsPassedFiducial = true;
                }
            }
        //} else {
        //    KsPassedFiducial = true;
        //}
        if (KsPassedFiducial) {
            edm::Ptr<reco::VertexCompositeCandidate> kptr(h_kshort,k);
	    // check for overlaps with the lambdas, and keep the lambda in case
            bool overlap = false;
            for (auto lptr : *lambdas) {
              for (unsigned int li = 0; li < lptr->numberOfDaughters() && !overlap; ++li) {
                for (unsigned int ki = 0; ki < kptr->numberOfDaughters() && !overlap; ++ki) {
	          if (lptr->daughter(li)->px() == kptr->daughter(ki)->px() &&
	              lptr->daughter(li)->py() == kptr->daughter(ki)->py() &&
	              lptr->daughter(li)->pz() == kptr->daughter(ki)->pz()) {
                    overlap = true;
	          }
	        }
              }
              if (overlap){
	    	 //std::cout << "LambdaKshortFilter: OVERLAP FOUND" << std::endl;
	    	 break;
	      }	
            }
            if (!overlap) kshorts->push_back(std::move(kptr));
      //  kshorts->push_back(std::move(kptr));
        }
        //else{
        //std::cout<< "Kshort failed Fiducial cuts" << std::endl;
        //}
      }
    }


  // if not data, then select on gen particles
  //} else {

//    // read out genparticles
//    edm::Handle<std::vector<reco::GenParticle> > h_genparts;
//    iEvent.getByToken(genCollectionToken_, h_genparts);
//    if(!h_genparts.isValid()) {
//      std::cout << "Missing collection : " << genCollectionTag_ << " ... skip entry !" << std::endl;
//      return false;
//    }
//
//    // find lambdas and kshorts
//    for (unsigned int p = 0; p < h_genparts->size(); ++p) {
//      if (fabs(h_genparts->at(p).pdgId()) == 3122 //&&
//          //fabs(h_genparts->at(p).eta()) < maxEtaLambda_ &&
//	  /*h_genparts->at(p).pt() > minPtLambda_*/) {
//        // check the decay to be to a (anti)proton (and a pion) -> need Geant collected genparticles to do that
//        if (checkLambdaDaughters_) { // make sure to collect geant genparticles first
//          if (!h_genparts->at(p).daughter(0) || !h_genparts->at(p).daughter(1)) {
//            continue;
//          }
//          if (fabs(h_genparts->at(p).daughter(0)->pdgId()) != 2212 &&
//              fabs(h_genparts->at(p).daughter(1)->pdgId()) != 2212) continue;
//        }
//        edm::Ptr<reco::GenParticle> lptr(h_genparts,p);
//        lambdas->push_back(std::move(lptr));
//      }
//      if ((fabs(h_genparts->at(p).pdgId()) == 310) //&&
//          fabs(h_genparts->at(p).eta()) < maxEtaKshort_ &&
//	  h_genparts->at(p).pt() > minPtKshort_) {
//	edm::Ptr<reco::GenParticle> kptr(h_genparts,p);
//        kshorts->push_back(std::move(kptr));
//      }
//    }
//
//
//  }

  // get the vector sizes before they disappear when putting in the event
  unsigned int nl = lambdas->size(), nk = kshorts->size();

  iEvent.put(std::move(lambdas),"lambda");
  iEvent.put(std::move(kshorts),"kshort");

  // throw away events on data without sufficient lambdas or kshorts
  if (nl < minNrLambda_ || nk < minNrKshort_) {
    ++nreject_;
    return (prescaleFalse_ ? !(nreject_ % prescaleFalse_) : false);
  }
  // if we reach here there's a sufficient number of good lambdas and kshorts
  //std::cout << "Fiducial cuts Passed" << std::endl;
 

   return true;

}


#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(FiducialCuts);
