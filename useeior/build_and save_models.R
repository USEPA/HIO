


#library(useeior)

library(devtools)
devtools::load_all("../../useeior")

modelmeta <- list("USEEIOv2.0.2-walrus"= c("USEEIOv2.0.2-walrus"),
                  "USEEIO-WARM"= c("USEEIO-WARM", "WARMv15"),
                  "USEEIO-Waste-Disagg"= c("USEEIO-Waste-Disagg","LandfillingDisaggregation","562OTHDisaggregation",
                                          "WasteCombustorsDisaggregation","MRFsDisaggregation"),
                  "USEEIO-REI"= c("USEEIO-REI","REI_WIO"),
                  "USEEIO-WIO-Disagg"= c("USEEIO-WIO-Disagg","DisaggWIOConcrete","LandfillingDisaggregation",
                                         "562OTHDisaggregation","WasteCombustorsDisaggregation","MRFsDisaggregation")
                  )

for (name in names(modelmeta)) {
  cpaths <- c()
  for (cfg in modelmeta[[name]] ) {
    cpaths <- append(cpaths,paste0(cfg,".yml"))
  }
  model <- buildModel(name, configpaths=file.path(cpaths))
  saveRDS(model,paste0(useeio_ref_name,".rds"))  
}

