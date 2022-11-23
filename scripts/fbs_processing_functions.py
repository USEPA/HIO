# -*- coding: utf-8 -*-
"""
Functions to further process FBS collapsed files
"""
import logging
import re
from flowsa.flowbyfunctions import aggregator
from flowsa.dataclean import replace_NoneType_with_empty_cells, replace_strings_with_NoneType

def convert_fbsc_to_disagg_env(fbsc):
    """
    Convert a given collapsed flowbysector (fbs) to a useeior disagggregation env (env) file
    Validates that values are present in all required fields
    fbs collapsed spec:
    https://github.com/USEPA/flowsa/blob/master/format%20specs/FlowBySector.md#flow-by-sector-collapsed-format
    env spec:
    https://github.com/USEPA/useeior/blob/master/format_specs/ModelCustomization.md#disaggregated-table-format
    convert fbsc to env
    :param fbsc: a flow-by-sector collapsed formatted dataframe
    :return: an env formatted dataframe with SatelliteTable col as None
    """
    dis_env_cols = {'Flowable': True,
                    'Context': False,
                    'FlowUUID': False,
                    'Sector': True,
                    'Location': True,
                    'FlowAmount': True,
                    'Unit': True,
                    'DistributionType': False,
                    'Min': False,
                    'Max': False,
                    'DataReliability': False,
                    'TemporalCorrelation': False,
                    'GeographicalCorrelation': False,
                    'TechnologicalCorrelation': False,
                    'DataCollection': False,
                    'Year': True,
                    'MetaSources': False,
                    'SatelliteTable': False}
    required_fields = [key for (key, value) in dis_env_cols.items() if value == True]
    # a Satellite table field needs to be added, checking that it doesn't exist
    if 'SatelliteTable' not in fbsc.columns:
        fbsc['SatelliteTable'] = None
    try:
        env = fbsc[dis_env_cols.keys()]
        recs_missing_values = env[required_fields].isnull().sum()
        if sum(recs_missing_values) > 0:
            logging.error("Records are missing required values. Number of missing values by required field " + str(
                recs_missing_values))
        return env
    except KeyError:
        logging.error("FBS missing some fields expected in env file.")

def get_last_letter(s):
    """
    grab last character from end of a string
    :param s:
    :return: single character
    """
    try:
        letter = re.findall("([A-Z])$", s)[0]
        return letter
    except IndexError:
        return None

def replace_last_letter(s):
    try:
        loc =  re.search("([A-Z])$", s).start()
        s = s[:loc] + 'X'
        return s
    except AttributeError:
        return s

def remove_last_letter(s):
    try:
        loc =  re.search("([A-Z])$", s).start()
        s = s[:loc]
        return s
    except AttributeError:
        return s


def agg_fbsc_by_material(fbsc, model_material_codes):
    """
    Will identify material-specific sectors (ending in a material code) that are not part of the selected
    set of codes, change them into 'X' for other and aggregate the flows together and return them
    :param fbsc: a flow-by-sector collapsed formatted dataframe
    :param model_materials: a list of materials found in the materials reference list
    :return: fbsc
    """
    # Get codes for selected materials and put them in a temporary mat_code column for wrangling
    fbsc['mat_code'] = fbsc['Sector'].apply(get_last_letter)
    #Set mat_code to 'X' when not in the provided list
    fbsc.loc[(~fbsc['mat_code'].isin(model_material_codes) &
             fbsc['mat_code'].notnull()),'mat_code'] = 'X'
    # Now use that mat_code to replace the original code for sectors with this X
    fbsc.loc[fbsc['mat_code']=='X','Sector'] = fbsc.loc[fbsc['mat_code']=='X','Sector'].apply(replace_last_letter)
    # Drop the temp mat_code col
    fbsc = fbsc.drop(columns='mat_code')

    # Aggregate the new sectors using the flowsa aggregator function. Remove flowamount first
    groupbycols = fbsc.columns.drop("FlowAmount")
    fbsc = aggregator(fbsc, groupbycols)

    return fbsc

def replace_FlowAmount_w_FlowRatio(env):
    env = replace_NoneType_with_empty_cells(env).reset_index(drop=True)
    # env.loc[:,'NAICS'] = env.loc[:,'Sector'].apply(remove_last_letter)
    env.loc[:,'NAICS'] = env.loc[:,'Sector'].str[0:6]
    groupbycols = ['Flowable', 'Context','Location','Unit','Year', 'NAICS']
    denom_df = env.assign(Denominator=env.groupby(
        groupbycols)['FlowAmount'].transform('sum'))
    env = env.merge(denom_df,how='left')
    env.loc[:, 'FlowRatio'] = env['FlowAmount'] / env['Denominator']
    env = env.drop(columns=['FlowAmount','NAICS','Denominator'])
    env = replace_strings_with_NoneType(env)
    return env
