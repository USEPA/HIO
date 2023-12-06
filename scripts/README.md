# Scripts

Scripts for general data conversion, formatting to use data between models

[convert_Mixed_WARM_FBS_to_env.py](convert_Mixed_WARM_FBS_to_env.py) converts the Mixed WARM FBS dataset produced by [run_Mixed_WARM_national_2018.py](../flowsa/run_Mixed_WARM_national_2018.py) in a series of environmental ratio files beginning wih 'Mixed_WARM_FBS' found in [model disaggspecs](../useeior/disaggspecs) that are used in the disaggregation process for some HIO models.

[create_waste_disagg_ratios.py](create_waste_disagg_ratios.py) uses the Waste_national_2018 FBS dataset produced by [run_Waste_national_2018.py](../flowsa/run_Waste_national_2018.py) to make the Make and Use disaggregation input files (those ending in _Make and _Use) found in [model disaggspecs](../useeior/disaggspecs) that are used in the disaggregation process for some HIO models.

[fbs_processing_functions.py](fbs_processing_functions.py) is a set of commons functions used by the above py scripts.

[get_WARMer_inputs.py](get_WARMer_inputs.py) uses the WARMer package to write out the B matrix data from the WARM model and stores it as [WARMv15_env.csv](../data/WARMv15_env.csv), and it prepares a hybridization [technical and environmental ratios](../useeior/hybridizationspecs) (the files ending in _env and _tech) for use in the integrated hybrid model.

[parse_REI_env_data.py](parse_REI_env_data.py) and [parse_REI_source_data.py](parse_REI_source_data.py) respectively parse the data extracted from the 2020 EPA Recycling Economic Information model, found in [data/REI_sourcedata](../data/REI_sourcedata) and convert them into a format for construction waste input-output models in useeior. Outputof the ..source_data.py are written to [WIOspecs](/useeior/WIOspecs) and output of ..env_data.py are stored by EPA on the Data Commons and are automatically downloaded during useeior model construction of HIO models using these data files.