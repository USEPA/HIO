Build and calculate the WARM Integrated Hybrid Model with Food and
Concrete waste management processes

Load useeior, define model and paths to specs, build model

``` r
library(useeior) #must be useeior >= 1.4 with hybrid capabilities

# Build model from specs
configpaths <- file.path(c("useeior/modelspecs/USEEIO-WARM.yml", "useeior/hybridizationspecs/WARMv15.yml"))
modelname <- "USEEIO-WARM"
model <- buildModel(modelname, configpaths)
```

    ## 2023-12-02 17:21:56 INFO::Begin model initialization...
    ## 2023-12-02 17:21:57 INFO::Initializing IO tables...
    ## 2023-12-02 17:21:57 INFO::Initializing Gross Output tables...
    ## 2023-12-02 17:22:00 INFO::Initializing Chain Price Index tables...
    ## 2023-12-02 17:22:01 INFO::Loading hybridization specification file for WARMv15...
    ## 2023-12-02 17:22:01 INFO::Initializing model satellite tables...
    ## 2023-12-02 17:22:01 INFO::Loading Greenhouse Gases flows from DataCommons...
    ## 2023-12-02 17:22:03 INFO::Loading Employment flows from DataCommons...
    ## 2023-12-02 17:22:04 INFO::Generating Value Added flows...
    ## 2023-12-02 17:22:04 INFO::No duplicate flows exist across satellite tables.
    ## 2023-12-02 17:22:04 INFO::Initializing model indicators...
    ## 2023-12-02 17:22:04 INFO::Getting WARM GHG indicator from DataCommons...
    ## 2023-12-02 17:22:04 INFO::Loading demand vectors ...
    ## 2023-12-02 17:22:04 INFO::Loading US CompleteProduction demand vector...
    ## 2023-12-02 17:22:04 INFO::Loading US DomesticProduction demand vector...
    ## 2023-12-02 17:22:04 INFO::Loading US CompleteConsumption demand vector...
    ## 2023-12-02 17:22:04 INFO::Loading US DomesticConsumption demand vector...
    ## 2023-12-02 17:22:05 INFO::Building commodity-by-commodity A matrix (direct requirements)...
    ## 2023-12-02 17:22:05 INFO::Building commodity-by-commodity A_d matrix (domestic direct requirements)...
    ## 2023-12-02 17:22:05 INFO::Hybridizing model for A matrix...
    ## 2023-12-02 17:22:05 INFO::Hybridizing model for A matrix...
    ## 2023-12-02 17:22:05 INFO::Calculating L matrix (total requirements)...
    ## 2023-12-02 17:22:05 INFO::Calculating L_d matrix (domestic total requirements)...
    ## 2023-12-02 17:22:05 INFO::Building B matrix (direct emissions and resource use per dollar)...
    ## 2023-12-02 17:22:06 INFO::Hybridizing model for B matrix...
    ## 2023-12-02 17:22:06 INFO::Building C matrix (characterization factors for model indicators)...
    ## 2023-12-02 17:22:06 INFO::Calculating D matrix (direct environmental impacts per dollar)...
    ## 2023-12-02 17:22:06 INFO::Calculating M matrix (total emissions and resource use per dollar)...
    ## 2023-12-02 17:22:06 INFO::Calculating M_d matrix (total emissions and resource use per dollar from domestic activity)...
    ## 2023-12-02 17:22:06 INFO::Calculating N matrix (total environmental impacts per dollar)...
    ## 2023-12-02 17:22:06 INFO::Calculating N_d matrix (total environmental impacts per dollar from domestic activity)...
    ## 2023-12-02 17:22:06 INFO::Calculating Rho matrix (price year ratio)...
    ## 2023-12-02 17:22:06 INFO::Calculating Phi matrix (producer over purchaser price ratio)...
    ## 2023-12-02 17:22:06 INFO::Model build complete.

Run and view validation results

``` r
printValidationResults(model)
```

    ## [1] "Validate that commodity output can be recalculated (within 1%) with the model total requirements matrix (L) and demand vector (y) for US production"
    ## [1] "Number of sectors passing: 403"
    ## [1] "Number of sectors failing: 2"
    ## [1] "Sectors failing: S00402/US, S00300/US"
    ## [1] "Validate that commodity output can be recalculated (within 1%) with model total domestic requirements matrix (L_d) and model demand (y) for US production"
    ## [1] "Number of sectors passing: 403"
    ## [1] "Number of sectors failing: 2"
    ## [1] "Sectors failing: S00402/US, S00300/US"
    ## [1] "Validate that flow totals by commodity (E_c) can be recalculated (within 1%) using the model satellite matrix (B), market shares matrix (V_n), total requirements matrix (L), and demand vector (y) for US production"
    ## [1] "Number of flow totals by commodity passing: 8100"
    ## [1] "Number of flow totals by commodity failing: 0"
    ## [1] "Validate that flow totals by commodity (E_c) can be recalculated (within 1%) using the model satellite matrix (B), market shares matrix (V_n), total domestic requirements matrix (L_d), and demand vector (y) for US production"
    ## [1] "Number of flow totals by commodity passing: 8100"
    ## [1] "Number of flow totals by commodity failing: 0"
    ## [1] "Sectors with flow totals failing: "
    ## [1] "Validate that commodity output are properly transformed to industry output via MarketShare"
    ## [1] "Number of flow totals by commodity passing: 403"
    ## [1] "Number of flow totals by commodity failing: 2"
    ## [1] "Sectors with flow totals failing: S00402/US, S00300/US"
    ## [1] "Validate that commodity output equals to domestic use plus production demand"
    ## [1] "Number of flow totals by commodity passing: 404"
    ## [1] "Number of flow totals by commodity failing: 1"
    ## [1] "Sectors with flow totals failing: S00300/US"

Look at the new waste commodities, which are the only model commodities
with kg as the unit

``` r
df <- model$Commodities
df <- df[df$Unit=="kg",c("Code","Name")]
knitr::kable(df, row.names = FALSE)
```

| Code     | Name                                                                                                          |
|:---------|:--------------------------------------------------------------------------------------------------------------|
| 5622121C | MSW landfilling of Concrete                                                                                   |
| 5622121F | MSW landfilling of Food Waste; National average LFG recovery, typical collection, National average conditions |
| 562213F  | MSW combustion of Food Waste                                                                                  |
| 5622191F | Anaerobic digestion of Food Waste; Dry digestion, Cured                                                       |
| 5622192F | MSW composting of Food Waste                                                                                  |
| 5629201C | MSW recycling of Concrete                                                                                     |

See what indicators are available to calculate results with in the model

``` r
model$Indicators$meta[,c("Name","Code","Unit")]
```

    ##       Name     Code   Unit
    ## 1 WARM GHG GHG-WARM MTCO2e

Calculate a result from the model based on demand of waste treatment.
Use 1000 kg for food waste landfilling First create demand vector,
calculate the model, and print the LCIA final result

``` r
y <- setNames(1000, "5622121F/US")
y <- useeior:::formatDemandVector(y, model$L)
results <- calculateEEIOModel(model, perspective = "FINAL", y)
```

    ## 2023-12-02 17:22:07 INFO::Calculating Final Perspective LCI...
    ## 2023-12-02 17:22:07 INFO::Calculating Final Perspective LCIA...
    ## 2023-12-02 17:22:07 INFO::Result calculation complete.

``` r
lcia <- results[["LCIA_f"]]
lcia["5622121F/US",]
```

    ## [1] 0.5624817

The interpretation of the result is the impact of landfilling 1000 tons
of food waste in the U.S. The unit is the units of the model indicator,
MTCO2e.

See the total of the flows for this result (the life cycle inventory
results)

``` r
lci <- results[["LCI_f"]]
print(lci["5622121F/US",])
```

    ##                       Carbon dioxide/emission/air/kg 
    ##                                        -2.740067e+01 
    ##                       Carbon dioxide/resource/air/kg 
    ##                                         9.573369e+01 
    ##                 Carbon tetrafluoride/emission/air/kg 
    ##                                         1.331949e-07 
    ##                       Compensation of employees//USD 
    ##                                         5.776305e+01 
    ##                         Energy, heat/resource/air/MJ 
    ##                                         0.000000e+00 
    ##                         Gross operating surplus//USD 
    ##                                         1.597046e+00 
    ##                     Hexafluoroethane/emission/air/kg 
    ##                                         3.098714e-08 
    ##                              HFC-125/emission/air/kg 
    ##                                         1.052944e-05 
    ##                             HFC-134a/emission/air/kg 
    ##                                         2.984698e-05 
    ##                             HFC-143a/emission/air/kg 
    ##                                         4.252774e-06 
    ##                               HFC-23/emission/air/kg 
    ##                                         2.697678e-07 
    ##                            HFC-236fa/emission/air/kg 
    ##                                         8.394840e-08 
    ##                               HFC-32/emission/air/kg 
    ##                                         6.100237e-06 
    ##      HFCs and PFCs, unspecified/emission/air/kg CO2e 
    ##                                         1.139220e-02 
    ##                                              Jobs//p 
    ##                                         7.620166e-04 
    ##                              Methane/emission/air/kg 
    ##                                         2.744453e+01 
    ##                 Nitrogen trifluoride/emission/air/kg 
    ##                                         3.988792e-09 
    ##                        Nitrous oxide/emission/air/kg 
    ##                                        -1.672566e-03 
    ##                 Perfluorocyclobutane/emission/air/kg 
    ##                                         1.110136e-09 
    ##                     Perfluoropropane/emission/air/kg 
    ##                                         1.294951e-09 
    ##                  Sulfur hexafluoride/emission/air/kg 
    ##                                        -3.216853e-06 
    ## Taxes on production and imports, less subsidies//USD 
    ##                                         2.052762e+01
