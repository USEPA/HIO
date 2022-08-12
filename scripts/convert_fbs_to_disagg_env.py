# -*- coding: utf-8 -*-
"""
Convert a given collapsed flowbysector (fbs) to a useeior disagggregation env (env) file
Validates that values are present in all required fields
fbs collapsed spec: https://github.com/USEPA/flowsa/blob/master/format%20specs/FlowBySector.md#flow-by-sector-collapsed-format
env spec: https://github.com/USEPA/useeior/blob/master/format_specs/ModelCustomization.md#disaggregated-table-format
"""
import flowsa
import logging

fbs_name = "Mixed_WARM_national_2018"
env_name = "Mixed_WARM_national_2018_Env.csv"

MODULEPATH = './'

#Dictionary of fields present. True fields are required.
dis_env_cols = {'Flowable':True,
                'Context':False,
                'FlowUUID':False,
                'Sector': True,
                'Location':True,
                'FlowAmount':True,
                'Unit': True,
                'DistributionType': False,
                'Min': False,
                'Max': False,
                'DataReliability':False,
                'TemporalCorrelation':False,
                'GeographicalCorrelation':False,
                'TechnologicalCorrelation':False,
                'DataCollection':False,
                'Year':True,
                'MetaSources':False}

if __name__ == '__main__':

    fbs = flowsa.collapse_FlowBySector(fbs_name)

    required_fields = [key for (key,value) in dis_env_cols.items() if value == True]
    try:
       env = fbs[dis_env_cols.keys()]
       recs_missing_values = env[required_fields].isnull().sum()
       if sum(recs_missing_values) > 0:
           logging.error("Records are missing required values. Number of missing values by required field " + str(recs_missing_values))
       else:
       path = f"{MODULEPATH}useeior/disaggspecs/"
       env.to_csv(path+env_name, index=False)
       logging.info(env_name + " written to useeior/disaggspecs")
    except KeyError:
       logging.error("FBS missing some fields expected in env file.")
