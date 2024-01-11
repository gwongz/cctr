"""Constants used in the cctr python script"""

import os

SCRIPT_PATH = os.environ.get("SCRIPT_PATH")
SOURCE = os.environ.get("SOURCE")
DESTINATION = os.environ.get("DESTINATION")
# default to substitution mode
MODE = os.environ.get("MODE", "3")
