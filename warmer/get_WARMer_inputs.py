# get_WARMer_inputs.py (HIO)
"""
Uses WARMer to write out a complete table of WARM B matrix flows for flowsa, and tables of
selected A and corresponding B matrix flows for a specified useeior model
"""
import pandas as pd
from pathlib import Path
from warmer.olca_warm_matrix_io import get_exchanges, warm_version

modulepath = Path(__file__).parent
file_stub = f'{warm_version}'

## FBS input
writepath = modulepath.parent/'flowsa'
df_a, df_b = get_exchanges(opt_controls=['electricity', 'forest', 'fertilizer'])
df_b.to_csv(writepath / f'{file_stub}_env.csv', index=False)


## HIO-1 input
model_name = 'm1'
writepath = modulepath.parent / 'useeior'
model_processes = pd.read_csv(modulepath / 'model_1_processes.csv')
df_mapping = pd.read_csv(modulepath / 'processmapping.csv')

df_a, df_b = get_exchanges(df_subset_fg=model_processes, opt_mixer=None,
                           opt_map='all', df_mapping=df_mapping,
                           opt_controls=['electricity', 'forest', 'fertilizer'])
df_a.to_csv(writepath / f'{file_stub}_{model_name}_tech.csv', index=False)
(df_b.drop(columns='ProcessCategory')
     .query('Amount != 0')  # drop empty exchanges**
     .to_csv(writepath / f'{file_stub}_{model_name}_env.csv', index=False))

    # Of the 14 types of elementary flows in df_b, only 11 remain after
    # removing all-0-valued exchanges. Removed flows include:
        # Ethane, hexafluoro-, HFC-116
        # Methane, tetrafluoro-, R-14
        # Other means of transport (no truck, train or ...)
