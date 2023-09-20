import os.path

from web.options.options import WORK_OUT_DIR

"""Init work out dir"""
if not os.path.exists(WORK_OUT_DIR):
    os.makedirs(WORK_OUT_DIR)