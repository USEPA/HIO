# get_WARMer_inputs.py (HIO)
"""
Uses WARMer to write out a complete table of WARM B matrix flows for flowsa, and tables of
selected A and corresponding B matrix flows for a specified useeior model
"""
import pandas as pd
from pathlib import Path
from warmer import olca_warm_matrix_io

modulepath = Path(__file__).parent
file_stub = f'{olca_warm_matrix_io.warm_version}'

## FBS input
writepath = modulepath.parent/'data'
df_a, df_b = olca_warm_matrix_io.get_exchanges(opt_controls=['electricity', 'forest', 'fertilizer'])
df_b.to_csv(writepath / f'{file_stub}_env.csv', index=False)


model_name = 'm1'
writepath = modulepath.parent / 'useeior/hybridizationspecs/'
readpath =  modulepath.parent / 'data'
model_processes = pd.read_csv(readpath / 'EEIO-IH_waste_processes.csv')
df_mapping = pd.read_csv(readpath / 'WARM-to-USEEIO_processmapping.csv')

df_a, df_b = olca_warm_matrix_io.get_exchanges(df_subset_fg=model_processes, opt_mixer=None,
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
