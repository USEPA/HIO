# -*- coding: utf-8 -*-
"""
Creates an IPCC AR4-100 LCIAMethod using lciafmt
Writes method and associated metadata file to local cache
"""

import lciafmt
from lciafmt.util import store_method, collapse_indicators

ipcc = lciafmt.get_method("IPCC")

ipcc_AR4_100 = ipcc[ipcc["Indicator"]=="AR4-100"]

ipcc_AR4_100 = lciafmt.map_flows(ipcc_AR4_100,"IPCC")

ipcc_AR4_100 = collapse_indicators(ipcc_AR4_100)

store_method(ipcc_AR4_100,lciafmt.Method.IPCC,name="IPCC_AR4-100")



