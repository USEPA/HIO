"""
Generates CDD concrete national 2014 flow-by-sector model and saves it to local cache
along with the validation log
See the notes on 'CDD_concrete_national_2014.yaml' for requirements
"""

import os
import flowsa

# directory and file paths
DIRPATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
fbsMethodPath = f"{DIRPATH}"

# Run an FBS method not included in the flowsa repo
method = 'CDD_concrete_national_2014'
flowsa.flowbysector.main(method=method, fbsconfigpath=fbsMethodPath,
                         download_FBAs_if_missing=True)
fbs = flowsa.getFlowBySector(method)

