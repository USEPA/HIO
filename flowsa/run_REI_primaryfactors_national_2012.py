"""
Generates REI primaryfactors national 2012 flow-by-sector model and saves
it to local cache along with the validation log
"""

import os
import flowsa

# directory and file paths
DIRPATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
fbsMethodPath = f"{DIRPATH}"

# Run an FBS method not included in the flowsa repo
method = 'REI_primaryfactors_national_2012'
flowsa.flowbysector.main(method=method, fbsconfigpath=fbsMethodPath,
                         download_FBAs_if_missing=True)

