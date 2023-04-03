#ifndef PileUpScraper_h
#define PileUpScraper_h
#include <stdio.h>     
#include <stdlib.h> 
#include <time.h> 
 
#include "AnalyzerAllSteps.h"
using namespace edm;
using namespace std; 
class PileUpScraper : public edm::EDAnalyzer
 {
  public:
    explicit PileUpScraper(edm::ParameterSet const& cfg);
    virtual ~PileUpScraper();
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:

    bool m_runningOnData; 

    virtual void beginJob();
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
    virtual void endJob();
    
    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    //initialization of the different trees
    void Init_PV();

    edm::Service<TFileService> m_fs;

    //the collections 
    edm::InputTag m_offlinePVTag;

    edm::EDGetTokenT<vector<reco::Vertex>> m_offlinePVToken;
   
    //the trees in the ntuples
    TTree* _tree_PV;   

    //definition of variables which should go to _tree_PV
    std::vector<int> _nGoodPVPOG;
    std::vector<float> _goodPVzPOG;

    };

#endif

