# -*- coding: utf-8 -*-
"""
Script to generate totals-by-sector (flow-by-sector) formatted files from REI primary factor data.
One provides all primary factors flows using REI native nomenclature;
another provides just recycling sector primary factors flows using FEDEFL nomenclature.
"""

import pandas as pd
import numpy as np
import os

path = os.path.dirname(__file__)
source_path = os.path.realpath(os.path.dirname(path) + '/data/REI_sourcedata')
out_path = os.path.realpath(os.path.dirname(path) + '/useeior')

df = pd.read_csv(source_path + '/REI_primaryfactors.csv', header=1)
df = (df.rename(columns={'Unnamed: 0': 'Sector', 'Unnamed: 1': 'SectorName'})
      .melt(id_vars=['Sector', 'SectorName'], var_name='Flowable',
            value_name='FlowAmount')
      )

df['Unit'] = np.where(df['Flowable'] == 'Employment',
                      'p', '1000 USD')

df['Year'] = 2012
df['Context'] = ''
df[['DataReliability', 'TemporalCorrelation', 'GeographicalCorrelation', 
    'TechnologicalCorrelation', 'DataCollection']] = 5
df['Location'] = 'US'
df['MetaSources'] = 'REI 2020'

col_order = ['Sector',
            'SectorName',
            'Flowable',
            'Year',
            'FlowAmount',
            'DataReliability',
            'TemporalCorrelation',
            'GeographicalCorrelation',
            'TechnologicalCorrelation',
            'DataCollection',
            'Location',
            'Context',
            'Unit',
            'MetaSources']

df = df[col_order]

df.to_csv(f'{out_path}/REI_primaryfactors_TBS.csv', index=False)

df1 = df.query('Sector.str.startswith("RS")', engine='python')

# Map REI flows to FEDEFL flows
mapping = {"Wage":"Compensation of employees",
           "Employment":"Jobs",
           "Tax": "Taxes on production and imports, less subsidies"
           }

df1['Flowable'] = df1['Flowable'].replace(mapping)

df1.to_csv(f'{out_path}/REI_primaryfactors_waste_TBS.csv', index=False)


