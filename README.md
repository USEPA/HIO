<!-- badges: start -->
[![DOI](https://zenodo.org/badge/520644769.svg)](https://zenodo.org/badge/latestdoi/520644769)
<!-- badges: end -->

# HIO - Hybrid Input-Output models
This repository contains code to build a collection of waste-oriented hybrid input-output (HIO) models from selected USEPA waste generation and impact models, including [WARM](https://epa.gov/warm), [USEEIO](https://www.epa.gov/land-research/us-environmentally-extended-input-output-useeio-models), and models underlying the [Facts and Figures (FF)](https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling), [Recycling Economic Information (REI) report](https://www.epa.gov/smm/recycling-economic-information-rei-report), [CDDPath method](https://cfpub.epa.gov/si/si_public_record_Report.cfm?dirEntryId=344639&Lab=NRMRL) and the [Wasted Food Report (WFR)](https://www.epa.gov/system/files/documents/2023-03/2019%20Wasted%20Food%20Report_508_opt_ec.pdf).

The HIO models, and related reference USEEIO and REI can be assembled and used using [_useeior_](https://github.com/USEPA/useeior).
The files needed for this are found in the [useeior](/useeior) folder.

This HIO models rely on a series of sector attribution models build with [FLOWSA](https://github.com/USEPA/flowsa). Code to reproduce the flow-by-sector output from those models can be found in [flowsa](/flowsa). Code for other sector attribution models used is built into FLOWSA.

Some impact methods, including a method that replicates that in the WARM model, are used in the HIO models. Code for running those models that uses the [LCIA Formatter](https://github.com/USEPA/lciaformatter) can be found in [lciafmt](lciafmt).

Data and correspondence files used in any step are found in [data](/data). Scripts that draw WARM model data from WARMer, as well as other scripts for further processing data or model output for use in HIO models are found in [scripts](/scripts).

# Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use. EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.