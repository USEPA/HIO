# Requires working directory to be this file directory 
# useeior source files must be at the same level as HIO
# All model Data Commons dataset dependencies must be in local cache if not 
# available on Data Commons

library(devtools)
devtools::load_all("../../useeior")
# devtools::load_all("../../../../useeior_dev/useeior")

path_save <- "../../WARM-USEEIOdocs/data/"
library(logging)
addHandler(writeToFile, file=paste0(path_save, "build_and_save_REF_and_HIO_models.log"))

parentmodelmeta <- list(
  "USEEIOv2.0.2-walrus" = c("USEEIOv2.0.2-walrus"),  # 2018 FBS files needed
  "USEEIO-REI-Reference" = c("USEEIO-REI-Reference", 
                             "REI_WIO"))

HIOmodelmeta <- list(
  "USEEIO-WARM"= c("USEEIO-WARM", 
                   "WARMv15"),
  "USEEIO-Waste-Disagg" = c("USEEIO-Waste-Disagg",
                           "LandfillingDisaggregation",
                           "562OTHDisaggregation",
                           "WasteCombustorsDisaggregation",
                           "MRFsDisaggregation"),
  "USEEIO-REI" = c("USEEIO-REI",
                  "REI_WIO"),
  "USEEIO-WIO-Disagg" = c("USEEIO-WIO-Disagg",
                         "DisaggWIOConcrete",
                         "DisaggWIOFoodWaste",
                         "LandfillingDisaggregation",
                         "562OTHDisaggregation",
                         "WasteCombustorsDisaggregation",
                         "MRFsDisaggregation"))

saveModels <- function (v, meta, prefix, path_save) {
   for (i in 1:length(v)) {
    name <- names(meta)[i]
    cpaths <- c()
    for (cfg in meta[i]) {
      cpaths <- append(cpaths, paste0(cfg, ".yml"))
    }
    loginfo(paste("Attempting to build", name))
    model <- buildModel(name, configpaths=file.path(cpaths))
    name_save <- paste0(prefix, v[i])
    saveRDS(model, paste0(path_save, name_save, ".rds"))  
    loginfo(paste("Saved", name, "as", name_save, "to .rds"))
  }
} 

v <- c("USEEIO","REI")
prefix <- "REF-"
saveModels(v, parentmodelmeta, prefix, path_save)

v <- c(1:4)
prefix <- "HIO-"
saveModels(v, HIOmodelmeta, prefix, path_save)
