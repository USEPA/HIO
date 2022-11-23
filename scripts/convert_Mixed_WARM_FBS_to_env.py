# -*- coding: utf-8 -*-
"""
Converts the flowsa 'Mixed_WARM_national_2018' FBS into the environmental data input file for selected USEEIO
models
"""

import flowsa
from scripts.fbs_processing_functions import convert_fbsc_to_disagg_env, agg_fbsc_by_material, \
    replace_FlowAmount_w_FlowRatio, remove_last_letter, get_last_letter
import pandas as pd
import yaml
import os

use_FlowRatio = True

fbs_name = "Mixed_WARM_national_2018_v1.2.4_ba21923"

env_name = "Mixed_WARM_national_2018_Env"
if use_FlowRatio:
    env_name = env_name + "_Ratios"

disagg_path = os.path.realpath('useeior/')

model_material_codes = ['F', 'C']  # from Materials reference file

# Get flow by sector in fbs collapsed format
fbsc = flowsa.collapse_FlowBySector(fbs_name)

# Add satellite tables for each flow
sat_mapping_file = os.path.realpath('data/mapping_warm_flowables_to_satellite_table.yml')
with open(sat_mapping_file, 'r') as file:
    sat_mappings = yaml.safe_load(file)
sat_map_df = pd.DataFrame(data={'Flowable': sat_mappings.keys(), 'SatelliteTable': sat_mappings.values()})
fbsc = pd.merge(fbsc, sat_map_df, on='Flowable', how='left')

# Change location from a FIPS code to US
fbsc['Location'].replace({'00000': 'US'}, inplace=True)

# Aggregate flows for material sectors not in material_model_codes into an other set
fbsc = agg_fbsc_by_material(fbsc, model_material_codes)

env = convert_fbsc_to_disagg_env(fbsc)

if use_FlowRatio:
    env = replace_FlowAmount_w_FlowRatio(env)

# Split into separate dfs by pathway and write them out.
# Use waste_naics to get the pathways
#env.loc[:,'NAICS'] = env.loc[:,'Sector'].apply(str.substr)
env.loc[:,'NAICS'] = env.loc[:,'Sector'].str[0:6]

# For "Other" sectors, ensure they are at 6 digit only
env.loc[(env['Sector'].apply(get_last_letter) == 'X')
        ,'Sector'] = env['NAICS'] + 'X'

# join with waste naics to verify grouping by 6-digit waste naics
waste_naics = pd.read_csv("data/waste_naics.csv",dtype={"Parent":str})
waste_naics = (waste_naics
               .drop(columns=["Subnaics","NAICS","Management Pathway"])
               .drop_duplicates())
env = pd.merge(env,waste_naics,how='left',left_on='NAICS',right_on='Parent')
grouped_env_by_NAICS = env.groupby('Parent')

for name, df in grouped_env_by_NAICS.__iter__():
    NAICS_6 = df['Parent'].iloc[0]
    df.drop(columns=["Parent","NAICS"],inplace=True)
    env_file = os.path.join(disagg_path, env_name + "_" + NAICS_6 + ".csv")
    df = df.sort_values(by=['SatelliteTable','FlowUUID'])
    df.to_csv(env_file, index=False)
    print(env_file + " written.")

 

