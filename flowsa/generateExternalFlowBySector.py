"""
Example setup to generate a Flow-By-Sector dataset using an FBS method file
not included in the flowsa repo. FLOWSA will also look for external FBS
activity sets and activity to sector mapping files. Calling an external FBS
method file requires a specific directory setup. Any external activity sets
must be in a subdirectory labeled "flowbysectoractivitysets" in the same
directory as the FBS method yaml. Similarly, any mapping files must be in a
subdirectory labled "activitytosectormapping."
"""

# comment in to install flowsa, can modify branch or version
# import subprocess
# import sys
# subprocess.check_call([sys.executable, "-m", "pip", "install",
#                        "git+https://github.com/USEPA/flowsa.git@develop#"
#                        "egg=flowsa"])


import os
import flowsa

# directory and file paths
DIRPATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
fbsMethodPath = f"{DIRPATH}"

# Run an FBS method not included in the flowsa repo
method = 'Mixed_WARM_national_2018'
flowsa.flowbysector.main(method=method, fbsconfigpath=fbsMethodPath,
                         download_FBAs_if_missing=True)
fbs = flowsa.getFlowBySector(method)
