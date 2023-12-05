# Sector attribution models for material and WARM-based environmental flows for use in HIO models

[Flow-by-sector](https://github.com/USEPA/flowsa#flow-by-sector-fbs-datasets) model specifications and associated datasets custom-built for use in the HIO models found in this repository.

This code is not necessary to execute before creating the HIO models, as EPA has executed it and put the resulting data outputs on the data server that provides these files to the HIO models during the build.

This code requires use of a specific FLOWSA version for proper execution: [v1.3.2](https://github.com/USEPA/flowsa/releases/tag/v1.3.2), that can be installed with pip via:
`pip install git+https://github.com/USEPA/flowsa.git@v1.3.2#egg=flowsa`

This folder contain the records of the code and specification files that are not included in the FLOWSA v1.3.2 release. Other flowsa-produced datasets needed for the HIO models are also acquired from the data server at build time.

|Model|Description|
|---|---|
|CDD_concrete_national_2018||
|Mixed_WARM_national_2018||
|REI_primaryfactors_national_2012||
|Waste_national_2018||

Flow-by-sector models for food waste used in HIO model stored in FLOWSA v1.3.2 include [Food_Waste_national_2018_m1](https://github.com/USEPA/flowsa/blob/9b1bb41b66469dd56e1d9e203f77b2126dfdb9e7/flowsa/methods/flowbysectormethods/Food_Waste_national_2018_m1.yaml),[Food_Waste_national_2018_m2](https://github.com/USEPA/flowsa/blob/9b1bb41b66469dd56e1d9e203f77b2126dfdb9e7/flowsa/methods/flowbysectormethods/Food_Waste_national_2018_m2.yaml), and [REI_waste_national_2012](https://github.com/USEPA/flowsa/blob/9b1bb41b66469dd56e1d9e203f77b2126dfdb9e7/flowsa/methods/flowbysectormethods/REI_waste_national_2012.yaml)




