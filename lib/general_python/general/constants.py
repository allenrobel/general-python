#!/usr/bin/env python3
'''
stc_constants.py
Summary: Constants used in Spirent scripts

Description:

Currently, these are used mostly by general_python.general.verify_types.py
'''
OUR_VERSION = 102

class Constants(object):
    def __init__(self):
        self.lib_version = OUR_VERSION
        self.lib_name = "Constants"

        self.na_bool = False
        self.na_str  = 'na'
        self.na_int  = -1

        self.DEFAULT_LOGLEVEL = "INFO"
        self.VALID_LOGLEVELS = ["INFO","WARNING","DEBUG","ERROR","CRITICAL"]
        self.HEX_DIGITS = frozenset('0123456789ABCDEFabcdef')

