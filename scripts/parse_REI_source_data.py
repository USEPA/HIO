# -*- coding: utf-8 -*-
"""
Script to generate input data from REI files
"""


import pandas as pd
import os

path = os.path.dirname(__file__)
source_path = os.path.realpath(os.path.dirname(path) + '/data/REI_sourcedata')
out_path = os.path.realpath(os.path.dirname(path) + '/useeior/WIOspecs')

def fix_floats(df):
    df['Amount'] = df['Amount'].fillna('-')
    df = df[~df['Amount'].str.contains('-')]
    df = df.reset_index(drop=True)
    df['Amount'] = (df['Amount'].str.replace(',','')
                    .astype('float'))
    return df

## Make Intersection
make_int = pd.read_csv(f"{source_path}/REI_makeintersection.csv",
                       #skiprows=2
                       #dtype='float'
                       )
make_int = (make_int
            .drop(columns=make_int.columns[1]) # Drop names
            .drop([0]) # Drop names
            .rename(columns={'Unnamed: 0':"IndustryCode"})
            .melt(id_vars='IndustryCode', var_name='CommodityCode',
                  value_name='Amount')
            )
make_int = fix_floats(make_int)
make_int['Unit'] = 'MT'
make_int['WIO Section'] = 'V22'
make_int['Note'] = 'Make of Waste Treatment Commodities by Waste Treatment Industries'


## Use Intersection
use_int = pd.read_csv(f"{source_path}/REI_useintersection.csv",
                      header=2)
use_int = (use_int
           .drop(columns=use_int.columns[[1,2]]) # Drop names
           .drop([0]) # Drop blanks
           .rename(columns={'Unnamed: 0':"CommodityCode"})
           .melt(id_vars='CommodityCode', var_name='IndustryCode',
                 value_name='Amount')
           )
use_int = fix_floats(use_int)
use_int['Unit'] = 'USD'
# Where recyclable code >= 9 (Gleaned product), change units to MT
use_int.loc[use_int['CommodityCode'].str[-2:].astype('int') >= 9, 'Unit'] = 'MT'
use_int['WIO Section'] = 'U22'
use_int['Note'] = 'Use of Waste Treatment Commodity by Waste Treatment Industry'


## Make columns --> added as Use rows
make_col = pd.read_csv(f"{source_path}/REI_makecol.csv",
                       header=1, nrows=405,
                       )
make_col = (make_col
            .drop(columns=make_col.columns[[1]]) # Drop names
            .rename(columns={'Unnamed: 0':"IndustryCode"})
            .melt(id_vars='IndustryCode', var_name='CommodityCode',
                  value_name='Amount')
            )
make_col = fix_floats(make_col)
make_col['Unit'] = 'USD'
# Where recyclable code >= 9 (Gleaned product), change units to MT
make_col.loc[make_col['CommodityCode'].str[-2:].astype('int') >= 9, 'Unit'] = 'MT'
make_col['WIO Section'] = 'W41'
make_col['Note'] = 'Waste Gen by IO Industries - Analogous to value in Column in REI Make table'


## Use Columns
use_col = pd.read_csv(f"{source_path}/REI_usecol.csv",
                      header=1
                      )
use_col = (use_col
           .drop(columns=use_col.columns[[1]]) # Drop names
           .rename(columns={'Unnamed: 0':"CommodityCode"})
           .melt(id_vars='CommodityCode', var_name='IndustryCode',
                 value_name='Amount')
           )
use_col = fix_floats(use_col)
use_col['Unit'] = 'USD'
use_col['WIO Section'] = 'U12'
use_col['Note'] = 'Use of IO Commodity by Waste Treat Industry'

## Use Rows
use_row = pd.read_csv(f"{source_path}/REI_userow.csv",
                      header=1
                      )
use_row = (use_row
           .drop(columns=use_row.columns[[1]]) # Drop names
           .rename(columns={'Unnamed: 0':"IndustryCode"})
           .melt(id_vars='IndustryCode', var_name='CommodityCode',
                 value_name='Amount')
           )
use_row = fix_floats(use_row)
use_row['Unit'] = 'MT' # all recycled commodities in metric tons
use_row['WIO Section'] = 'U21'
use_row['Note'] = 'Use of Waste Treatment Commodity by IO Industry'

## Prepare final files
use = pd.concat([make_col, use_int, use_col, use_row], ignore_index=True)

## Add Waste generation by treatment data on diagonal
waste_gen = use.groupby(['CommodityCode']).sum().reset_index()
waste_gen = waste_gen[waste_gen['CommodityCode'].str[:2] == "RB"]
waste_gen['IndustryCode'] = waste_gen['CommodityCode'].apply(lambda x: f"WT00{x[4:6]}")
waste_gen['Unit'] = ''
waste_gen['WIO Section'] = 'W34'
waste_gen['Note'] = 'Waste generation by Treatment by Waste Generation by Mass'

make = pd.concat([make_int, waste_gen], ignore_index=True)

## Add location
for col in ['IndustryCode', 'CommodityCode']:
    use[col] = use[col].apply(lambda x: f"{x}/US")
    make[col] = make[col].apply(lambda x: f"{x}/US")

make.to_csv(f'{out_path}/REI_make_full.csv', index=False)
use.to_csv(f'{out_path}/REI_use_full.csv', index=False)

