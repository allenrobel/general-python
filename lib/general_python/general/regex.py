"""
Name: regex.py
Description: classes containing compiled commonly-used regexes
"""

import re
from general_python.general.log import Log

OUR_VERSION = 103
ver = "{}".format(OUR_VERSION)

class re_cli(object):
    '''compiled regex for nxos cli
    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        self.log.debug("compiling regex json_pipe")
        self.json_pipe = re.compile('^.*?\|\s*json\s*$')

class re_numeric(object):
    '''compiled regex for numbers
    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        self.log.debug("compiling regex hex")
        self.hex = re.compile('^0x[0-9a-f]+$')

class re_ipv4(object):
    '''compiled regex for ip addresses
    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        self.log.debug("compiling regex ip")
        self.ipv4 = re.compile('^\d+\.\d+\.\d+\.\d+$')

class re_ip(object):
    '''re_ip() is deprecated. use re_ipv4() instead
       compiled regex for ip addresses
       NOTES:
          1. keep re_ip() for backward compatibility until we ID which scripts use it
             new scripts should use class re_ipv4() instead

    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        self.log.debug("compiling regex ip")
        # keep self.ip for backward compatibility until we ID which scripts use it
        # self.ip is decprecated and new scripts should use self.ipv4 instead
        self.ip = re.compile('^\d+\.\d+\.\d+\.\d+$')

class re_json(object):
    '''compiled regex for json
    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        self.log.debug("compiling regex json_dict")
        self.json_dict = re.compile('^\{.*?\}\s*$')
        self.log.debug("compiling regex key_value_hex")
                                     # info_leaf_flood_dst_ptr=0x000007d1
        self.key_value_hex = re.compile('^(\w+)=(0x[0-9a-f]+)')
        self.log.debug("compiling regex key_value_any")
        self.key_value_any = re.compile('^(\w+)=(.*?)$')

class re_vxlan(object):
    '''compiled regex for vxlan
    '''
    def __init__(self,loglevel='INFO'):
        self.loglevel = loglevel
        self.log = Log(self.loglevel).create()
        #                             "L2 [2222]"
        self.log.debug("compiling regex json_dict")
        self.vni_l2 = re.compile('L2\s*\[(\d+)\]')
        #                             "L3 [TENANT_1]"
        self.vni_l3 = re.compile('L3\s*\[(.*?)\]')


