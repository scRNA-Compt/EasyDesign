import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
WORK_SPACE = str(root_dir) + os.sep

WORK_OUT_DIR = '/data/easyDesign/output/'   # default work out dir
SERVER_PORT = 8001                          # default server port