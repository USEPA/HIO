# -*- coding: utf-8 -*-
"""
Creates a WARM-based LCIA method

"""

import lciafmt
from lciafmt.util import store_method, collapse_indicators
from warmer.olca_get_results import datapath

filename = datapath/'WARMv15_lcia_methods.csv'

df = lciafmt.get_method(method_id=None, file=filename)

mapped_df = lciafmt.map_flows(df, system='WARM', case_insensitive=True)

mapped_df = collapse_indicators(mapped_df)

store_method(mapped_df, method_id=None, name="WARM")

