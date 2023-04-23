'''
verify_types.py
Summary: Methods for verifying types (e.g. int, str) and formats (mac address, ipv4 address)
Author: Allen Robel
Email: arobel@cisco.com
'''
import sys
import ipaddress
import logging
import math # is_power()
import re
# local libraries
from general_python.general.constants import Constants

OUR_VERSION = 136

class VerifyTypes(Constants):
    '''
    methods to verify various types e.g. boolean, int, str, hex values, etc

    Example usage:

    from verify_types import VerifyTypes()
    verify = VerifyTypes()
    mac = ":_LLLL"
    if not verify.is_mac_address(mac):
        print(f"{mac} not a mac-address.")

    '''
    def __init__(self, log):
        super().__init__()
        self.lib_version = OUR_VERSION
        self.lib_name = "VerifyTypes"
        self.log = log
        self.DEFAULT_LOGLEVEL = 'INFO'
        self.ipv4_mask_range = range(0,33)
        self.ipv6_mask_range = range(0,129)
        self.re_digits = re.compile('^(\d+)$')
        self.re_mac_address = re.compile(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2}$)', re.I)

    def is_boolean(self,x):
        '''verify x is a boolean value'''
        if isinstance(x, bool):
            return True
        return False

    def is_digits(self,x):
        '''verify x contains only digits i.e. is a positive integer'''
        if not self.re_digits.search(str(x)):
            return False
        return True

    def is_float(self,x):
        '''verify x is a float'''
        if isinstance(x, float):
            return True
        return False

    def is_hex(self,x):
        '''
        verify x contains only hexidecimal characters
        '''
        if not self.HEX_DIGITS.issuperset(x):
            return False
        return True

    def is_int(self,x):
        '''verify x is a integer'''
        if isinstance(x, int):
            return True
        return False

    def is_ipv4_address(self,x):
        '''verify x is an ipv4 address'''
        try:
            a = ipaddress.IPv4Address(x)
            return True
        except:
            self.log.debug(f"Not a valid ipv4 address: {x}. Should be in the form A.B.C.D")
            return False

    def is_ipv4_address_with_prefix(self,x):
        '''
        verify x is an ipv4 address with prefix of the form X.X.X.X/Y
        '''
        if not self.is_ipv4_address(re.sub('\/.*','',x)):
            self.log.debug(f"Not a valid ipv4 address with prefix: {x}. Should be in the form A.B.C.D/M")
            return False
        if "/" not in x:
            self.log.debug(f"Not a valid ipv4 address with prefix: {x}. Should be in the form A.B.C.D/M")
            return False
        return True

    def is_ipv4_network(self,x):
        try:
            ipaddress.IPv4Network(x)
            return True
        except Exception as e:
            self.log.debug(f"Not a valid ipv4 network: {x} -> {e}")
            return False

    def is_ipv4_mask(self,x):
        if not isinstance(x, int):
            self.log.debug(f"bad ipv4 network mask. Expected an integer. Got {x}")
            return False
        if x not in self.ipv4_mask_range:
            msg = f"bad ipv4 network mask {x}."
            msg += f" Should be an int {self.ipv4_mask_range.start}"
            msg += f" >= x <= {self.ipv4.mask_range.stop -1}"
            self.log.debug(msg)
            return False
        return True

    def is_ipv4_unicast_address(self,x):
        '''verify x is an ipv4 unicast address'''
        if self.is_ipv4_address(x) is False:
            return False
        _test = ipaddress.IPv4Address(x)
        bad_type = ''
        if _test.is_multicast:
            bad_type = 'is_multicast'
        elif _test.is_loopback:
            bad_type = 'is_loopback'
        elif _test.is_reserved:
            bad_type = 'is_reserved'
        elif _test.is_unspecified:
            bad_type = 'is_unspecified'
        elif _test.is_link_local:
            bad_type = 'is_link_local'
        elif re.search('\/', x):
            bad_type = 'is_subnet'
        if bad_type != '':
            self.log.debug(f"{x} not a unicast ipv4 address -> {bad_type}")
            return False
        return True

    def is_ipv6_network(self,x):
        if isinstance(x, ipaddress.IPv6Network):
            return True
        return False

    def is_ipv6_mask(self,x):
        if not isinstance(x, int):
            self.log.debug(f"bad ipv6 network mask. Expected int(). Got {x}.")
            return False
        if x not in self.ipv6_mask_range:
            msg = f"bad ipv6 network mask {x}."
            msg += f" Should be an int {self.ipv6_mask_range.start}"
            msg += f" >= x <= {self.ipv6.mask_range.stop -1}"
            self.log.debug(msg)
            return False
        return True

    def is_ipv6_address(self, x):
        '''
        verify x is an ipv6 address
        '''
        if isinstance(x, ipaddress.IPv6Address):
            return True
        self.log.debug(f"Not a valid ipv6 address: {x}")
        return False


    def is_ipv6_link_local_address(self, x):
        '''
        verify x is an ipv6 link-local address
        '''
        if not isinstance(x, ipaddress.IPv6Address):
            return False
        _a = ipaddress.IPv6Address(x)
        if not _a.is_link_local:
            return False
        return True
        
    def is_ipv6_unicast_address(self,x):
        '''
        verify x is an ipv6 unicast address
        '''
        try:
            _test = ipaddress.IPv6Address(x)
        except ipaddress.AddressValueError as exception:
            message = (
                f"{x} is not a valid ipv6 address."
                f"Exception detail: {exception}"
            )
            self.log.error(message)
            return False
        bad_type = ''
        if _test.is_multicast:
            bad_type = 'is_multicast'
        elif _test.is_loopback:
            bad_type = 'is_loopback'
        elif _test.is_reserved:
            bad_type = 'is_reserved'
        elif _test.is_unspecified:
            bad_type = 'is_unspecified'
        elif _test.is_link_local:
            bad_type = 'is_link_local'
        elif re.search('\.0$', x):
            bad_type = 'is_subnet'
        if bad_type != '':
            self.log.error(f"{x} not a unicast ipv6 address -> {bad_type}")
            return False
        return True

    def is_logging_instance(self, x):
        '''
        return True if x is a logging instance
        else, return False
        '''
        if isinstance(x, logging.Logger):
            return True
        return False

    def is_loglevel(self, x):
        if x in self.VALID_LOGLEVELS:
            return True
        return False

    def is_dict(self, x):
        '''verify x is a dictionary'''
        if isinstance(x, dict):
            return True
        return False

    def is_list(self, x):
        '''verify x is a list'''
        if isinstance(x, list):
            return True
        return False

    def is_list_of_int(self, x):
        '''verify x is a list containing only integers'''
        if not isinstance(x, list):
            return False
        for e in x:
            if not isinstance(e, int):
                self.log.error(f"One or more elements of list are not integers: {x}")
                return False
        return True


    def is_mac_address(self, x):
        '''verify x is a mac address'''
        m = self.re_mac_address.search(x)
        if m:
            return True
        return False

    def is_power(self, x, b):
        '''
        verify x is a power of b
        Examples:
            is_power(8,2)  # True
            is_power(7,2)  # False
        '''
        if b == 1:
            return x == 1
        return b**int(math.log(x, b)+.5) == x

    def is_range(self, x):
        if isinstance(x, range):
            return True
        self.log.error(f"Not a python range() type. Expected range(x,y). Got {x}")
        return False

    def is_tuple(self, x):
        if isinstance(x, tuple):
            return True
        return False
