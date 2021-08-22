
import os

###################################
# Some Filesystem related constants
###################################
ROOT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "botTrading")
ROOT_PATH_CHART = os.path.join(os.path.expanduser("~"), "Desktop", "botTrading", "chart")

# Sleep Constants
SLEEP_INTERIM_SEC = 0.01
SLEEP_REEVAL_SECS = (5 * 60)  # Re-Evaluate scrips every -> 60 Mins or 1 Hr

# Re-Evaluation
NUM_OF_REEVALS = 5