# write_FBS_activityset_WARM.py (scripts)
# !/usr/bin/env python3
# coding=utf-8
"""
Write the csv called on in flowbysectormethods yaml files
for the EPA_WARMer FBA
"""

import os
import numpy as np
import pandas as pd
import flowsa
# from flowsa.settings import flowbysectoractivitysetspath
from pathlib import Path
import re

filedir = Path(__file__)
flowsadir = filedir.parent.parent.absolute()
warm_datapath = f"{flowsadir}/WARMv15_env.csv"

if __name__ == '__main__':
    df_import = pd.read_csv(warm_datapath)

    df = (df_import[['ProcessName']]
          .drop_duplicates()
          .reset_index(drop=True)
          .rename(columns={"ProcessName": "name"}))

    # add note with materials
    df['note'] = df['name'].apply(
        lambda x: re.search('of (.*)', x).group(1))
    df['note'] = df['note'].apply(
        lambda x: x.split(';', 1)[0])
    df['activity_set'] = ''

    # order dataframe
    df = (df[['activity_set', 'name', 'note']]
          .sort_values(['note', 'name'])
          .reset_index(drop=True))

    # assign activity sets
    actset_dict = {'Aluminum Cans': 'aluminum',
                   'Asphalt Concrete': 'asphalt pavement',
                   'Asphalt Shingles': 'asphalt shingles',
                   'Carpet': 'carpet',
                   'Concrete': 'concrete',
                   'Dimensional Lumber': 'wood',
                   'Food Waste': 'food',
                   'Glass': 'glass',
                   'Mixed Metals': 'metal',
                   'Mixed MSW': 'other',
                   'Mixed MSW (Energy)': 'other',
                   'Mixed Paper (general)': 'paper',
                   'Mixed Plastics': 'plastic',
                   'Yard Trimmings': 'yard trimmings'}
    df['activity_set'] = df['note'].map(actset_dict).fillna('')

    df.to_csv(f'{flowsadir}/flowbysectoractivitysets/WARM_activitysets.csv',
              index=False)
