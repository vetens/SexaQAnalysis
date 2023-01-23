#include "../interface/AnalyzerAllSteps.h"
//#include <iostream>

//3D openingsangle between two vectors
double AnalyzerAllSteps::openings_angle(reco::Candidate::Vector momentum1, reco::Candidate::Vector momentum2){
  double opening_angle = TMath::ACos((momentum1.Dot(momentum2))/(pow(momentum1.Mag2()*momentum2.Mag2(),0.5)));
  return opening_angle;
}

double AnalyzerAllSteps::deltaR(double phi1, double eta1, double phi2, double eta2){
	double deltaPhi = reco::deltaPhi(phi1,phi2);
	double deltaEta = eta1-eta2;
	return pow(deltaPhi*deltaPhi+deltaEta*deltaEta,0.5);
}

//2D distance in xy
double AnalyzerAllSteps::lxy(TVector3 v1, TVector3 v2){
	double x1 = v1.X();
	double x2 = v2.X();
	double y1 = v1.Y();
	double y2 = v2.Y();
	return sqrt(pow(x1-x2,2)+pow(y1-y2,2));
}

//3D distance
double AnalyzerAllSteps::lxyz(TVector3 v1, TVector3 v2){
	double x1 = v1.X();
	double x2 = v2.X();
	double y1 = v1.Y();
	double y2 = v2.Y();
	double z1 = v1.Z();
	double z2 = v2.Z();
	return sqrt(pow(x1-x2,2)+pow(y1-y2,2)+pow(z1-z2,2));
}


//point of closest approach vector between a point (Point) and a line (Point_line;Vector_along_line)
TVector3 AnalyzerAllSteps::PCA_line_point(TVector3 Point_line, TVector3 Vector_along_line, TVector3 Point){
   //first move the vector along the line to the starting point of Point_line
   double normalise = sqrt(Vector_along_line.X()*Vector_along_line.X()+Vector_along_line.Y()*Vector_along_line.Y()+Vector_along_line.Z()*Vector_along_line.Z());
   TVector3 n(Vector_along_line.X()/normalise,Vector_along_line.Y()/normalise,Vector_along_line.Z()/normalise);
   TVector3 a = Point_line;
   TVector3 p = Point;

   //see https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line (Vector formulation)
   TVector3 vector_PCA = (a-p)-((a-p)*n)*n;
   return vector_PCA ;
}

//return the PCA vector in xy between point and line
TVector3 AnalyzerAllSteps::vec_dxy_line_point(TVector3 Point_line_in, TVector3 Vector_along_line_in, TVector3 Point_in){
  //looking at XY, so put the Z component to 0 first
  TVector3 Point_line(Point_line_in.X(),Point_line_in.Y(),0.);
  TVector3 Vector_along_line(Vector_along_line_in.X(), Vector_along_line_in.Y(),0.);
  TVector3 Point(Point_in.X(), Point_in.Y(), 0.);
  
  TVector3 shortest_distance = PCA_line_point(Point_line,  Vector_along_line, Point);
  return shortest_distance;
	
}

//return shortest distance between point and vector in xy. The sign is given by the dot product of the vector connecting the PCA to the refernece point and the direction of the vector under study
double AnalyzerAllSteps::dxy_signed_line_point(TVector3 Point_line_in, TVector3 Vector_along_line_in, TVector3 Point_in){
  TVector3 shortest_distance = vec_dxy_line_point(Point_line_in,Vector_along_line_in,Point_in);
  double dxy_signed_line_point = sqrt(shortest_distance.X()*shortest_distance.X()+shortest_distance.Y()*shortest_distance.Y());

  //looking at XY, so put the Z component to 0 first
  TVector3 Point_line(Point_line_in.X(),Point_line_in.Y(),0.);
  TVector3 Vector_along_line(Vector_along_line_in.X(), Vector_along_line_in.Y(),0.);
  TVector3 Point(Point_in.X(), Point_in.Y(), 0.);

  TVector3 displacement = Point_line - Point; 
  if(displacement*Vector_along_line<0)dxy_signed_line_point = -dxy_signed_line_point;

  return dxy_signed_line_point;
}

//same as dxy_signed_line_point, but now in 3D
double AnalyzerAllSteps::dxyz_signed_line_point(TVector3 Point_line_in, TVector3 Vector_along_line_in, TVector3 Point_in){
  TVector3 shortest_distance = PCA_line_point(Point_line_in,  Vector_along_line_in, Point_in);
  double dxyz_signed_line_point = sqrt(shortest_distance.X()*shortest_distance.X()+shortest_distance.Y()*shortest_distance.Y()+shortest_distance.Z()*shortest_distance.Z());

  TVector3 displacement = Point_line_in - Point_in; 
  if(displacement*Vector_along_line_in<0)dxyz_signed_line_point = -dxyz_signed_line_point;

  return dxyz_signed_line_point;
	
}

//uncertainty on lxy
double AnalyzerAllSteps::std_dev_lxy(double vx, double vy, double vx_var, double vy_var, double bx_x, double bx_y, double bx_x_var, double bx_y_var){

        double lxy_std_dev_nominator = pow(vx-bx_x,2)*(vx_var+bx_x_var) + pow(vy-bx_y,2)*(vy_var+bx_y_var);
        double lxy_std_dev_denominator = pow(vx-bx_x,2) + pow(vy-bx_y,2);
        double lxy_b_std_dev = sqrt(lxy_std_dev_nominator/lxy_std_dev_denominator);
        return lxy_b_std_dev;

}

//function to return the cos of the angle between the momentum of the particle and it's displacement vector. This is for a V0 particle, so you need the V0 to decay to get it's decay vertex
double AnalyzerAllSteps::XYpointingAngle(const reco::Candidate  * particle, TVector3 beamspot){
      double angleXY = -2;
      if(particle->numberOfDaughters() == 2){
	      TVector3 decayVertexParticle(particle->daughter(0)->vx(),particle->daughter(0)->vy(),particle->daughter(0)->vz());	 
	      double dx = decayVertexParticle.X()-beamspot.X();
	      double dy = decayVertexParticle.Y()-beamspot.Y();
	      double px = particle->px();
	      double py = particle->py();
	      angleXY = (dx*px+dy*py)/(sqrt(dx*dx+dy*dy)*sqrt(px*px+py*py));
      }
      return angleXY;
	
}

double AnalyzerAllSteps::CosOpeningsAngle(TVector3 vec1, TVector3 vec2){
  double nom = vec1.X()*vec2.X()+vec1.Y()*vec2.Y()+vec1.Z()*vec2.Z();
  double denom = sqrt(vec1.X()*vec1.X()+vec1.Y()*vec1.Y()+vec1.Z()*vec1.Z())*sqrt(vec2.X()*vec2.X()+vec2.Y()*vec2.Y()+vec2.Z()*vec2.Z());
  return nom/denom;
}

//longitudinal impact parameter between a vector (Point_line_in;Vector_along_line_in) and a reference point (Point_in)
double AnalyzerAllSteps::dz_line_point(TVector3 Point_line_in, TVector3 Vector_along_line_in, TVector3 Point_in){
  Double_t vz = Point_line_in.Z();
  Double_t vx = Point_line_in.X();
  Double_t vy = Point_line_in.Y();
  Double_t px = Vector_along_line_in.X();
  Double_t py = Vector_along_line_in.Y();
  Double_t pz = Vector_along_line_in.Z(); 
  Double_t pt = sqrt(px*px+py*py);
  //from: https://github.com/cms-sw/cmssw/blob/master/DataFormats/TrackReco/interface/TrackBase.h#L764-L767
  return (vz - Point_in.Z()) - ((vx - Point_in.X()) * px + (vy - Point_in.Y()) * py) / pt * pz / pt;
             
}

//use the dz_line_point function here to look for the valid PV in h_offlinePV which minimises the dz
TVector3 AnalyzerAllSteps::dz_line_point_min(TVector3 Point_line_in, TVector3 Vector_along_line_in, edm::Handle<vector<reco::Vertex>> h_offlinePV){

	TVector3 bestPV;
	double dzmin = 999.;

	for(unsigned int i = 0; i < h_offlinePV->size(); ++i){
		//select only PV with certain quality cuts like it needs enough tracks pointing to it
		//if(h_offlinePV->at(i).isValid() && h_offlinePV->at(i).tracksSize() >= 4){
		double r = sqrt(h_offlinePV->at(i).x()*h_offlinePV->at(i).x()+h_offlinePV->at(i).y()*h_offlinePV->at(i).y());
                if(h_offlinePV->at(i).ndof() > 4 && abs(h_offlinePV->at(i).z()) < 24 && r < 2){
			TVector3 PV(h_offlinePV->at(i).x(),h_offlinePV->at(i).y(),h_offlinePV->at(i).z());
			double dz  = AnalyzerAllSteps::dz_line_point(Point_line_in,Vector_along_line_in,PV);
			if(abs(dz) < abs(dzmin)) {dzmin = dz; bestPV =  PV;}
		}
	}

	return bestPV;

}

double AnalyzerAllSteps::sgn(double input){
  double output = 1;
  if(input < 0.) output = -1;
  return output;
}

//return a certain integer when the gen particle under consideration has certain daughters
int AnalyzerAllSteps::getDaughterParticlesTypes(const reco::Candidate * genParticle){
        int pdgIdDaug0 = genParticle->daughter(0)->pdgId();
        int pdgIdDaug1 = genParticle->daughter(1)->pdgId();
        int returnCode = -1;
        if(abs(pdgIdDaug0) == AnalyzerAllSteps::pdgIdPosPion && abs(pdgIdDaug1) == AnalyzerAllSteps::pdgIdPosPion)returnCode = 1;//this is the correct decay mode for Ks to be RECO
        else if((pdgIdDaug0 == AnalyzerAllSteps::pdgIdAntiProton && pdgIdDaug1 == AnalyzerAllSteps::pdgIdPosPion) || (pdgIdDaug1 == AnalyzerAllSteps::pdgIdAntiProton && pdgIdDaug0 == AnalyzerAllSteps::pdgIdPosPion))returnCode = 2;//this is the correct decay mode for an antiLambda to get RECO
        else if((pdgIdDaug0 == AnalyzerAllSteps::pdgIdKs && pdgIdDaug1 == AnalyzerAllSteps::pdgIdAntiLambda) ||(pdgIdDaug1 == AnalyzerAllSteps::pdgIdKs && pdgIdDaug0 == AnalyzerAllSteps::pdgIdAntiLambda)) returnCode = 3;//this is the correct decay mode for an antiS

        return returnCode;

}

//return certain ints as codes for the track's trackquality
int AnalyzerAllSteps::trackQualityAsInt(const reco::Track *track){
    int myquality = -99;
    if(track->quality(reco::TrackBase::undefQuality))myquality = -1;
    if(track->quality(reco::TrackBase::loose))myquality = 0;
    if(track->quality(reco::TrackBase::tight))myquality = 1;
    if(track->quality(reco::TrackBase::highPurity))myquality = 2;
    if(track->quality(reco::TrackBase::confirmed))myquality=3;
    if(track->quality(reco::TrackBase::goodIterative))myquality=4;
    if(track->quality(reco::TrackBase::looseSetWithPV))myquality=5;
    if(track->quality(reco::TrackBase::highPuritySetWithPV))myquality=6;
    if(track->quality(reco::TrackBase::discarded))myquality=7;
    if(track->quality(reco::TrackBase::qualitySize))myquality=8;
    return myquality;
}

//check for a certain TrackingParticle if this TrackingParticle is a final state particle in an Sbar event. To do this you need to go through the TrackingParticle collection and try to find production vertices overlapping with decay vertices
std::vector<double> AnalyzerAllSteps::isTpGrandDaughterAntiS(TrackingParticleCollection const & TPColl, const TrackingParticle& tp){

 std::vector<double> returnVector; //this vector contains as first element the number defined at the bottom of this function which tells which kind of track this is and as second number the eta of this antiS
 returnVector.push_back(0.);
 returnVector.push_back(999.);
  

 bool tpIsGrandDaughterAntiS = false;
 string daughter = "none";
 string granddaughter = "none";
 if(abs(tp.pdgId()) == 211 || tp.pdgId() == - 2212){//found a charged pion or antiproton

        double granddaughterVx = tp.vx();double granddaughterVy = tp.vy();double granddaughterVz = tp.vz();

        for(size_t j=0; j<TPColl.size(); ++j) {//now find the daughters which have a decay vertex = the production vertex of the granddaughters
                if(tpIsGrandDaughterAntiS)continue;//can skip it was already found in a previous loop
                const TrackingParticle& tp_daughter = TPColl[j];

                if(abs(tp_daughter.pdgId()) == 310 || tp_daughter.pdgId() == -3122){//daughter has to be a Ks or Lambda

                        tv_iterator tp_daughter_firstDecayVertex = tp_daughter.decayVertices_begin();
                        double daughterdecayVx = (**tp_daughter_firstDecayVertex).position().X(); double daughterdecayVy = (**tp_daughter_firstDecayVertex).position().Y(); double daughterdecayVz = (**tp_daughter_firstDecayVertex).position().Z();

                        if(granddaughterVx == daughterdecayVx && granddaughterVy == daughterdecayVy && granddaughterVz == daughterdecayVz){//daughter decay vertex has to match the granddaughter creation vertex
                                for(size_t k=0; k<TPColl.size(); ++k) {//loop to find the antiS
                                        if(tpIsGrandDaughterAntiS)continue;//can skip it was already found in a previous loop
                                        const TrackingParticle& tp_S = TPColl[k];
                                        if(tp_S.pdgId() == -1020000020){//found the S
                                                tv_iterator tp_S_firstDecayVertex = tp_S.decayVertices_begin();
                                                double SdecayVx = (**tp_S_firstDecayVertex).position().X(); double SdecayVy = (**tp_S_firstDecayVertex).position().Y();double SdecayVz = (**tp_S_firstDecayVertex).position().Z();
                                                if(tp_daughter.vx() == SdecayVx && tp_daughter.vy() == SdecayVy && tp_daughter.vz() == SdecayVz){
                                                        tpIsGrandDaughterAntiS = true;
							if(abs(tp.pdgId()) == 211) granddaughter = "pion";
							else if(tp.pdgId() == -2212) granddaughter = "antiproton";

							if(abs(tp_daughter.pdgId()) == 310) daughter = "Ks";
							else if(tp_daughter.pdgId() == -3122) daughter = "AntiLambda";
							
							returnVector[1] = tp_S.eta();
                                                }
                                        }//end if antiS
                                }//end loop over the tp to find the antiS
                        }//end check if granddaughter vertex matches the the daughter decay vertex      
                }//end check for pdgId daughter
        }//end loop over tp to find daughters
   }//end check of granddaughter pdgId

 if(tpIsGrandDaughterAntiS && daughter == "Ks" && granddaughter == "pion") returnVector[0] = 1.;
 else if(tpIsGrandDaughterAntiS && daughter == "AntiLambda" && granddaughter == "pion") returnVector[0] = 2.;
 else if(tpIsGrandDaughterAntiS && daughter == "AntiLambda" && granddaughter == "antiproton") returnVector[0] = 3.;
 else returnVector[0] = 0;
 
 return returnVector;

}

//weight factor for the fact that Sbar with higher eta have a larger pathlength through the beampipe
double AnalyzerAllSteps::EventWeightingFactor(double thetaAntiS){
	return 1/TMath::Sin(thetaAntiS);
}

//extract the reweighing factor for Multi-to-Single Sbar kinematic reweighting
std::vector<double> AnalyzerAllSteps::MC_M2SReweighingFactor(double MC_etaAntiS, edm::FileInPath filePath_To_M2SReweigh){
 //       std::cout << "Getting Reweighting factor for Eta of: " << MC_etaAntiS << std::endl;
	double eta_map_prev = -999.;
	double weight_map_prev = 0.;
	double err_map_prev = 0.;
        std::vector<double> returnWeight; //this vector contains as first element the weight, and second element the error in the weight
        //Initialize weight and error
        returnWeight.push_back(1.0);
        returnWeight.push_back(0.0);

        std::string EtaMapFilePath = filePath_To_M2SReweigh.fullPath();
        std::ifstream configFile(EtaMapFilePath.c_str());
        std::string line;
  //      std::cout << "variables initialized " << std::endl;
	
        while(getline(configFile, line))
        {
            line.erase(0, line.find_first_not_of(" \t")); // Remove leading whitespace
            if ( line.length() == 0 || line.at(0) == '#') {continue;} //Skip comments and blank lines
            double eta_map;
            double weight_map;
            double err_map;
            std::stringstream lineStream(line);
            lineStream >> eta_map >> weight_map >> err_map;
   //         std::cout << "checking eta: " << eta_map << ", with weight: " << weight_map << std::endl;
            if ( eta_map > MC_etaAntiS) {
		returnWeight[0] = weight_map;
		returnWeight[1] = err_map;
		if(abs(eta_map_prev-MC_etaAntiS) < abs(eta_map-MC_etaAntiS)) {
                    returnWeight[0] = weight_map_prev;
                    returnWeight[1] = err_map_prev;
                    }
    //            std::cout << "best match found! eta: " << eta_map << ", weight: " << returnWeight[0] << "+/-" << returnWeight[1] << std::endl;
		break;	
                }
	    eta_map_prev = eta_map;
	    weight_map_prev = weight_map;   
	    err_map_prev = err_map;   
        }
     //   std::cout << "loop closed" << std::endl;
   	return returnWeight;
    }

//extract the reweighing factor for PV distribution. 
double AnalyzerAllSteps::PUReweighingFactor(int MC_nPV, double MC_PV_vz, edm::FileInPath filePath){
	double PVz_map_prev = -999.;
	double weight_map_prev = 0.;
	double return_weight = 0.;

        std::string PUMapFilePath = filePath.fullPath();
        std::ifstream configFile(PUMapFilePath.c_str());
        std::string line;
	
        while(getline(configFile, line))
        {
            line.erase(0, line.find_first_not_of(" \t")); // Remove leading whitespace
            if ( line.length() == 0 || line.at(0) == '#') {continue;} //Skip comments and blank lines
            int nPV_map;
            double PVz_map;
            double weight_map;
            std::stringstream lineStream(line);
            lineStream >> nPV_map >> PVz_map >> weight_map;
            if ( nPV_map != MC_nPV) {continue;}
            if ( PVz_map > MC_PV_vz) {
		return_weight = weight_map;
		if(abs(PVz_map_prev-MC_PV_vz) < abs(PVz_map-MC_PV_vz)) return_weight = weight_map_prev;
		break;	
                }
	    PVz_map_prev = PVz_map;
	    weight_map_prev = weight_map;   
        }
   	return return_weight;
    }
