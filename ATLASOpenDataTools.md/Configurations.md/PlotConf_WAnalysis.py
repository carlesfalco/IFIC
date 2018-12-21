config = {
"Luminosity": 3200,
"InputDirectory": "results",

"Histograms" : {
    "WtMass"          : {},
    "etmiss"          : {},
    "lep_pt"          : {},
    "lep_eta"         : {"y_margin" : 0.6},
    "lep_E"           : {},
    "lep_phi"         : {"y_margin" : 0.6},
    "lep_charge"      : {"y_margin" : 0.6},
    "lep_type"        : {},
    "lep_ptconerel30" : {},
    "lep_etconerel20" : {},
    "lep_z0"          : {},
    "lep_d0"          : {},
    "n_jets"          : {},
    "jet_pt"          : {},
    "jet_m"           : {},
    "jet_jvt"         : {"y_margin" : 0.3},
    "jet_eta"         : {"y_margin" : 0.3},
    "jet_MV2c10"      : {}, 
    "jet_phi"         : {"y_margin" : 0.6},
    "vxp_z"           : {},
    "pvxp_n"          : {},
},

"Paintables": {
    "Stack": {
        "Order": ["Diboson", "W", "Z", "stop", "ttbar"],
        "Processes" : {                
            "Diboson" : {
                "Color"         : "#fa7921",
                "Contributions" : ["WWlvlv", "WWlvqq", "WZlvll", "WZlvvv", "WZqqll", "WZlvqq", "ZZllll", "ZZvvll", "ZZqqll"]},
                                            
            "W": {              
                "Color"         : "#e55934",
                "Contributions" : ["Wenu0_70JetsBVeto", "Wenu0_70WithB", "Wenu0_70NoJetsBVeto", "Wenu70_140JetsBVeto", "Wenu70_140WithB", "Wenu70_140NoJetsBVeto", "Wenu140_280JetsBVeto", "Wenu140_280WithB", "Wenu140_280NoJetsBVeto", "Wenu280_500JetsBVeto", "Wenu280_500NoJetsBVeto", "Wmunu0_70JetsBVeto", "Wmunu0_70WithB", "Wmunu0_70NoJetsBVeto", "Wmunu70_140JetsBVeto", "Wmunu70_140WithB", "Wmunu70_140NoJetsBVeto", "Wmunu140_280JetsBVeto", "Wmunu140_280WithB", "Wmunu140_280NoJetsBVeto", "Wmunu280_500JetsBVeto", "Wmunu280_500NoJetsBVeto", "Wtaunu0_70JetsBVeto", "Wtaunu0_70WithB", "Wtaunu0_70NoJetsBVeto", "Wtaunu70_140JetsBVeto", "Wtaunu70_140WithB", "Wtaunu70_140NoJetsBVeto", "Wtaunu140_280JetsBVeto", "Wtaunu140_280WithB", "Wtaunu140_280NoJetsBVeto"]},
                                
            "Z": {              
                "Color"         : "#086788",
                "Contributions" : ["Zee", "Zmumu", "Ztautau"]},
                  
            "stop": {
                "Color"         : "#fde74c",
                "Contributions" : ["stop_tchan_top", "stop_tchan_antitop", "stop_schan_top", "stop_schan_antitop", "stop_wtchan_top", "stop_wtchan_antitop"]},
            
            "ttbar": {
                "Color"         : "#9bc53d",
                "Contributions" : ["ttbar_lep"]}
        }
    },

    "data" : {
        "Contributions": ["data_276262", "data_276329", "data_276336", "data_276416", "data_276511", "data_276689", "data_276790", "data_276952", "data_276954", "data_278880", "data_278912", "data_278968", "data_279169", "data_279259", "data_279279", "data_279284", "data_279345", "data_279515", "data_279598", "data_279685", "data_279813", "data_279867", "data_279928", "data_279932", "data_279984", "data_280231", "data_280273", "data_280319", "data_280368", "data_280423", "data_280464", "data_280500", "data_280520", "data_280614", "data_280673", "data_280753", "data_280853", "data_280862", "data_280950", "data_280977", "data_281070", "data_281074", "data_281075", "data_281317", "data_281385", "data_281411", "data_282625", "data_282631", "data_282712", "data_282784", "data_282992", "data_283074", "data_283155", "data_283270", "data_283429", "data_283608", "data_283780", "data_284006", "data_284154", "data_284213", "data_284285", "data_284420", "data_284427", "data_284484"]}
},

"Depictions": {
    "Order": ["Main", "Data/MC"],
    "Definitions" : {
        "Data/MC": {
            "type"       : "Agreement",
            "Paintables" : ["data", "Stack"]
        },
        
        "Main": {
            "type"      : "Main",
            "Paintables": ["Stack", "data"]
        },
    }
},
}
