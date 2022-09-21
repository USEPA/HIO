# -*- coding: utf-8 -*-
"""
Creates mass-based ratios of waste flows from the Waste_national_2018 fbs
for use as disaggregation input files
"""
import os
import pandas as pd

import flowsa

path = os.path.dirname(__file__)
disagg_path = os.path.dirname(path) + '/useeior/'

waste = flowsa.getFlowBySector('Waste_national_2018_v1.2.4_89d7292')

commodities = ['food', 'concrete']
sectors = ['562219', # AD/Compost
           '562213', # Combustion
           '562212', # Landfill
           '562920', # Recycling
           ]
waste['Sector6'] = waste['SectorConsumedBy'].str[0:6]
waste = waste[waste['Sector6'].isin(sectors)]
waste.loc[~waste['Flowable'].isin(commodities), 'Flowable'] = 'Other'
waste.loc[~waste['Flowable'].isin(commodities), 'Sector'] = waste['Sector6'] + 'X'
waste.loc[waste['Flowable'].isin(commodities), 'Sector'] = waste['SectorConsumedBy']

waste_total = waste.drop(columns=['SectorProducedBy','SectorConsumedBy'])
waste_total = (waste.groupby(['Flowable','Sector','Sector6',
                              'MetaSources', 'Year'])
               .agg({'FlowAmount': 'sum'})
               .reset_index())
waste_total['Pct'] = round(waste_total['FlowAmount'] /
                      waste_total.groupby(['Sector6'])
                      .FlowAmount.transform('sum'), 5)
waste_total = waste_total.sort_values(by=['Sector6','Sector'])
# waste_total.to_csv('waste_total_disagg.csv', index=False)

# Drop MetaSources and Year
waste_total = (waste_total
               .drop(columns=['MetaSources', 'Year'])
               .groupby(['Flowable','Sector','Sector6'])
               .agg({'Pct': 'sum', 'FlowAmount': 'sum'})
               .reset_index())
waste_total['Pct'] = round(waste_total['Pct'], 5)

## Convert into disaggregation files
sector_label_dict = { # NACIS, USEEIO, Name
    '562219': ('562OTH', '562OTH'),
    '562212': ('562212', 'Landfilling'),
    '562920': ('562920', 'MRFs'),
    '562213': ('562213', 'WasteCombustors'),
    }
waste_total['USEEIO'] = waste_total['Sector6'].map(sector_label_dict)
waste_total[['USEEIO', 'Name']] = pd.DataFrame(
    waste_total['USEEIO'].tolist(), index=waste_total.index)
grouping = waste_total.groupby('Name')


make_cols = {'USEEIO': 'IndustryCode',
             'Sector': 'CommodityCode',
             'Pct': 'PercentMake',
             }

use_cols = {'USEEIO': 'IndustryCode',
            'Sector': 'CommodityCode',
            'Pct': 'PercentUsed',
            }

for name, df in grouping.__iter__():
    # Create Make File
    file = f'{disagg_path}{name}Disaggregation_Make.csv'
    make = df.rename(columns=make_cols)
    make = make[make_cols.values()]
    make['IndustryCode'] = make['IndustryCode'] + '/US'
    make['CommodityCode'] = make['CommodityCode'] + '/US'
    make['Note'] = 'Default allocation, commodity output'
    make.to_csv(file, index=False)

    # Create Use file
    file = f'{disagg_path}{name}Disaggregation_Use.csv'
    use = df.rename(columns=use_cols)
    use = use[use_cols.values()]
    use['IndustryCode'] = use['IndustryCode'] + '/US'
    use['CommodityCode'] = use['CommodityCode'] + '/US'
    use['Note'] = 'Use row sum, commodity output'
    use2 = use.copy()
    use2 = use2.rename(columns={'IndustryCode': 'CommodityCode',
                                'CommodityCode': 'IndustryCode'})
    use2['Note'] = 'Use column sum, industry output'
    use = pd.concat([use, use2], ignore_index=True)
    use.to_csv(file, index=False)

## Assess imputed price
output_dict = { # USEEIO, USD
    '562OTH': 8399222951.2,
    '562212': 7212631574.94,
    '562920': 5944579212.1127,
    '562213': 4490811640,
    }
waste_qty = (waste_total
             .groupby('USEEIO')
             .agg({'FlowAmount': 'sum'})
             .reset_index())
waste_qty['Value'] = waste_qty['USEEIO'].map(output_dict)
waste_qty['Price'] = round(waste_qty['Value'] / waste_qty['FlowAmount'],5)
print(waste_qty[['USEEIO','Price']])
