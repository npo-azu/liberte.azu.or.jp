#----------------------------------------------------------           
# Import
#----------------------------------------------------------
# Standard library
import os
import distutils.util

# Additional library

# Original library
import lib.log

# Other module


#----------------------------------------------------------           
# Get env
#----------------------------------------------------------
MICROCMS_ID = os.getenv('MICROCMS_ID', None)
MICROCMS_KEY = os.getenv('MICROCMS_KEY', None)
MICROCMS_API_PAGES = os.getenv('MICROCMS_API_PAGES', None)
MICROCMS_API_CONFIG = os.getenv('MICROCMS_API_CONFIG', None)
MICROCMS_API_STUDY = os.getenv('MICROCMS_API_STUDY', None)
DEBUG = os.getenv('DEBUG', 'false')

#----------------------------------------------------------           
# Cast
#----------------------------------------------------------
DEBUG = distutils.util.strtobool(DEBUG)

#----------------------------------------------------------           
# Validation
#----------------------------------------------------------
if None in (MICROCMS_ID, MICROCMS_KEY, MICROCMS_API_PAGES, MICROCMS_API_CONFIG, MICROCMS_API_STUDY):
    raise Exception('microcms envs were not set,')
