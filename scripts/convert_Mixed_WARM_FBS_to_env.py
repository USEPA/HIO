# -*- coding: utf-8 -*-
"""
Converts the flowsa 'Mixed_WARM_national_2018' FBS into the environmental data input file for selected USEEIO
models
"""

import flowsa
from scripts.fbs_processing_functions import convert_fbsc_to_disagg_env, agg_fbsc_by_material
import pandas as pd
import yaml
import os
import logging

fbs_name = "Mixed_WARM_national_2018"
env_name = "Mixed_WARM_national_2018_Env.csv"
disagg_path = os.path.realpath('useeior/disaggspecs/')

model_material_codes = ['F','C']  # from Materials reference file

fbsc = flowsa.collapse_FlowBySector(fbs_name)

sat_mapping_file = 'data/mapping_warm_flowables_to_satellite_table.yml'
with open(sat_mapping_file, 'r') as file:
    sat_mappings = yaml.safe_load(file)
sat_map_df = pd.DataFrame(data={'Flowable':sat_mappings.keys(), 'SatelliteTable':sat_mappings.values()})

fbsc = pd.merge(fbsc,sat_map_df,on='Flowable',how='left')


fbsc.query()

fbsc = agg_fbsc_by_material(fbsc, model_material_codes)

env = convert_fbsc_to_disagg_env(fbsc)

env.to_csv(disagg_path + env_name, index=False)
logging.info(env_name + " written to " + disagg_path)


