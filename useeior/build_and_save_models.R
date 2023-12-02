# Requires working directory to be the repo directory
# useeior source files must be at the same level as this repo
# All model Data Commons dataset dependencies must be in local cache if not 
# available on Data Commons

library(devtools)
devtools::load_all("../useeior")

path_save <- "output/"
library(logging)
basicConfig(level = 'DEBUG')
log_file <- paste0(path_save, "build_and_save_REF_and_HIO_models.log")
if (file.exists(log_file)){
  file.remove(log_file)
}
addHandler(writeToFile, logger='HIO', file=log_file)

parentmodelmeta <- list(
  "USEEIOv2.0.2-walrus" = c("modelspecs/USEEIOv2.0.2-walrus"),  # 2018 FBS files needed
  "USEEIO-REI-Reference" = c("modelspecs/USEEIO-REI-Reference", 
                             "REI_WIO"))

HIOmodelmeta <- list(
  "USEEIO-WARM"= c("modelspecs/USEEIO-WARM", 
                   "hybridizationspecs/WARMv15"),
  "USEEIO-Waste-Disagg" = c("modelspecs/USEEIO-Waste-Disagg",
                           "disaggspecs/LandfillingDisaggregation",
                           "disaggspecs/562OTHDisaggregation",
                           "disaggspecs/WasteCombustorsDisaggregation",
                           "disaggspecs/MRFsDisaggregation"),
  "USEEIO-REI" = c("modelspecs/USEEIO-REI",
                  "WIOspecs/REI_WIO"),
  "USEEIO-WIO-Disagg" = c("modelspecs/USEEIO-WIO-Disagg",
                         "WIOspecs/DisaggWIOConcrete",
                         "WIOspecs/DisaggWIOFoodWaste",
                         "disaggspecs/LandfillingDisaggregation",
                         "disaggspecs/562OTHDisaggregation",
                         "disaggspecs/WasteCombustorsDisaggregation",
                         "disaggspecs/MRFsDisaggregation"))

saveModels <- function (v, meta, prefix, path_save) {
   for (i in 1:length(v)) {
    name <- names(meta)[i]
    cpaths <- c()
    for (cfg in meta[i]) {
      cpaths <- append(cpaths, paste0("useeior/",cfg, ".yml"))
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

 
