library(devtools)
devtools::load_all("../../useeior")
library(logging)
addHandler(writeToFile,file="build_and_save_REF_and_HIO_models.log")

parentmodelmeta <- list("USEEIOv2.0.2-walrus"= c("USEEIOv2.0.2-walrus"),
                        "USEEIO-REI-Reference" = c("USEEIO-REI-Reference","REI_WIO")
                    )

HIOmodelmeta <- list("USEEIO-WARM"= c("USEEIO-WARM", "WARMv15"),
                  "USEEIO-Waste-Disagg"= c("USEEIO-Waste-Disagg","LandfillingDisaggregation","562OTHDisaggregation",
                                          "WasteCombustorsDisaggregation","MRFsDisaggregation"),
                  "USEEIO-REI"= c("USEEIO-REI","REI_WIO"),
                  "USEEIO-WIO-Disagg"= c("USEEIO-WIO-Disagg","DisaggWIOConcrete","LandfillingDisaggregation",
                                         "562OTHDisaggregation", "WasteCombustorsDisaggregation", "MRFsDisaggregation")
                  )

saveModels <- function (v,meta) {
   for (i in 1:length(v)) {
    name <- names(meta)[i]
    cpaths <- c()
    for (cfg in meta[i]) {
      cpaths <- append(cpaths,paste0(cfg,".yml"))
    }
    loginfo(paste("Attempting to build",name))
    model <- buildModel(name, configpaths=file.path(cpaths))
    savename <- paste0(prefix,v[i])
    saveRDS(model,paste0(savename,".rds"))  
    loginfo(paste("Saved",name,"as",savename,"to .rds"))
  }
} 

v <- c("USEEIO","REI")
prefix <- "REF-"
saveModels(v,parentmodelmeta)


v <- c(1:4)
prefix <- "HIO-"
saveModels(v,HIOmodelmeta)



 

