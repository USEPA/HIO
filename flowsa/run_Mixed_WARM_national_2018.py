"""
Generates Mixed WARM national 2018 flow-by-sector model and saves it to local cache
along with the validation log
See the notes on 'Mixed_WARM_national_2018.yaml' for requirements
"""

import os
import flowsa

# directory and file paths
DIRPATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
fbsMethodPath = f"{DIRPATH}"

# Run an FBS method not included in the flowsa repo
method = 'Mixed_WARM_national_2018'
flowsa.flowbysector.main(method=method, fbsconfigpath=fbsMethodPath,
                         download_FBAs_if_missing=True)

