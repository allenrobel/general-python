# Poc() - python/lib3/poc.py
import re
import json
# local libraries
from general_python.general.verify_types import VerifyTypes
from general.log import get_logger
OUR_VERSION = 130
'''
Name: poc.py
Description: Create JSON used by PoC scripts to access management functions of switches

Synopsis:
    p = POC()
    p.sid = 301
    p.ansible_host = 'tor-301'
    p.hostname = 'my_dut'
    p.username = 'admin'
    p.password = 'superdupersecret'
    p.ts_password1 = 'superdupersecret'
    p.ts_password2 = 'superdupersecret'
    p.mgmt_ip = '172.29.167.208'
    p.mgmt_ip_prefixlen = 24
    p.mgmt_ipv6 = '2001:167::208'
    p.mgmt_ipv6_prefixlen = 124
    p.gateway = '172.29.167.1'
    p.dns_server1 = '171.70.168.183'
    p.dns_server2 = '171.70.167.183'
    p.ntp_server1 = '172.29.167.1'
    p.ntp_server2 = '172.29.167.250'
    p.location = 'row C, rack C-04'
    p.contact = 'Allen Robel - arobel@cisco.com'

    # p.role can be called multiple times for each sid.
    # Each time it is called, it adds the value to p.sid's
    # role set().  For example, the following adds three
    # roles.  See poc.py self.valid_roles for a list of valid roles.
    p.role = 'tor'
    p.role = 'vtep'
    p.role = 'vpc_peer'

    p.ts_ip1 = '172.22.150.11'
    p.ts_port1 = '2033'
    p.ts_ip2 = '172.22.150.11'
    p.ts_port2 = '2034'
    p.apc_ip1 = '172.22.153.47'
    p.apc_outlet1 = 23
    p.apc_ip2 = '172.22.153.47'
    p.apc_outlet1 = 24
    p.commit()

Revision history: Use git log
'''
log = get_logger('poc', 'INFO', 'DEBUG')

class POC(object):
    '''
    methods for creating json-format dut mapping files for testbeds

    Defined parameters:
        ansible_host        - name used in ansible inventory
        apc_ip1             - ip address of APC associated with outlet connected to PS1 on DUT
        apc_ip2             - ip address of APC associated with outlet connected to PS2 on DUT
        apc_ip3             - ip address of APC associated with outlet connected to PS3 on DUT
        apc_ip4             - ip address of APC associated with outlet connected to PS4 on DUT
        apc_outlet1         - APC outlet connected to PS1 on DUT
        apc_outlet2         - APC outlet connected to PS2 on DUT
        apc_outlet3         - APC outlet connected to PS3 on DUT
        apc_outlet4         - APC outlet connected to PS4 on DUT
        fn                  - POC filename to read (see POC() in poc.py for method to write this file)
        sid                 - switch ID
        mgmt_ip             - mgmt0 ip address
        mgmt_ip_prefixlen   - mgmt0 prefix length
        mgmt_ipv6           - mgmt0 ipv6 address
        mgmt_ipv6_prefixlen - mgmt0 prefix length
        hostname            - hostname
        gateway             - ip gateway for mgmt_ip
        nameserver          - deprecated, nameserver for mgmt_ip
        dns_server1         - primary nameserver for mgmt_ip
        dns_server2         - secondary nameserver for mgmt_ip
        ntp_server1         - primary ntp server
        ntp_server2         - secondary ntp server
        username            - username on sid
        password            - password on sid
        role                - role for this sid
                              called using str() e.g. instance.role = 'core'
                              can be called multiple times, each time adds a new role to internal role set()
                              role is stored as a list() in JSON
                              internally, role is a set()
        ts_ip1              - ip address of terminal server associated with 1st console port for dut
        ts_ip2              - ip address of terminal server associated with 2nd console port for dut
        ts_port1            - 1st console port for dut
        ts_port2            - 2nd console port for dut
        ts_password         - terminal server password when telneting to port 21
        contact             - freeform string with contact into (phone, email, etc), can be used for snmp contact
        location            - freeform string with location into (row, rack, etc), can be used for snmp location
    '''
    def __init__(self):
        self.classname = __class__.__name__
        self.lib_version = OUR_VERSION
        self.log = get_logger('{}.{}'.format(self.classname, self.lib_version), 'INFO', 'DEBUG')
        self.verify = VerifyTypes(log)
        self.cfg = dict()
        self._sid = False
        self._ansible_host = False
        self._contact = False
        self._location = False
        self._mgmt_ip = False
        self._mgmt_ip_prefixlen = False
        self._mgmt_ipv6 = False
        self._mgmt_ipv6_prefixlen = False
        self._gateway = False
        self._nameserver = False
        self._dns_server1 = False
        self._dns_server2 = False
        self._ntp_server1 = False
        self._ntp_server2 = False
        self._hostname = False
        self._username = False
        self._password = False
        self._apc_ip1 = False
        self._apc_ip2 = False
        self._apc_ip3 = False
        self._apc_ip4 = False
        self._apc_outlet1 = False
        self._apc_outlet2 = False
        self._apc_outlet3 = False
        self._apc_outlet4 = False
        self._role = set()
        self._ts_ip1 = False
        self._ts_ip2 = False
        self._ts_password1 = False
        self._ts_password2 = False
        self._ts_port1 = False
        self._ts_port2 = False
        self.fn  = False
        # terminal server port number should be 4 digits
        self.re_4digits = re.compile('^\d{4}$')

        # the below are deprecated
        self._console_ip1 = False
        self._console_port1 = False
        self._console_ip2 = False
        self._console_port2 = False
        self.valid_roles = set()
        self.valid_roles.add('bgp_external')
        self.valid_roles.add('bgw')
        self.valid_roles.add('border_gateway')
        self.valid_roles.add('core')
        self.valid_roles.add('dc')
        self.valid_roles.add('dci')
        self.valid_roles.add('fanout')
        self.valid_roles.add('labserver')
        self.valid_roles.add('leaf')
        self.valid_roles.add('mgmt')
        self.valid_roles.add('pim_rp')
        self.valid_roles.add('spine')
        self.valid_roles.add('sspine')
        self.valid_roles.add('super_spine')
        self.valid_roles.add('termserver')
        self.valid_roles.add('tgen')
        self.valid_roles.add('tgen_core')
        self.valid_roles.add('tgen_dc')
        self.valid_roles.add('tgen_dci')
        self.valid_roles.add('tgen_spine')
        self.valid_roles.add('tgen_tor')
        self.valid_roles.add('tgen_tier1')
        self.valid_roles.add('tgen_tier2')
        self.valid_roles.add('tier1')
        self.valid_roles.add('tier2')
        self.valid_roles.add('tier3')
        self.valid_roles.add('tier4')
        self.valid_roles.add('tor')
        self.valid_roles.add('vpc_peer')
        self.valid_roles.add('vtep')

    def add_role(self, x):
        self._role.add(x)

    def remove_role(self, x):
        if x in self._role:
            self._role.remove(x)

    def verify_console_port(self,x):
        '''verify the current terminal server port number'''
        m = self.re_4digits.search(str(x))
        if m:
            return True
        else:
            return False

    def verify_role(self,x):
        '''
        verify x is in self.valid_roles
        '''
        if x in self.valid_roles:
            return
        self.log.error('exiting. {} is not a valid role. Expected one of {}'.format(x, ','.join(self.valid_roles)))
        exit(1)

    @property
    def ansible_host(self):
        '''
        ansible inventory hostname of dut
        synopsis:
            p = POC()
            p.ansible_host = 's301'
        '''
        return self._ansible_host
    @ansible_host.setter
    def ansible_host(self, x):
        self._ansible_host = x

    @property
    def contact(self):
        '''
        contact information, can be used for snmp contact
        synopsis:
            p = POC()
            p.contact = 'Allen Robel : arobel@cisco.com : 669-222-0033'
        '''
        return self._contact
    @contact.setter
    def contact(self, x):
        self._contact = x

    @property
    def filename(self):
        '''output filename for mapping file
           synopsis:
              p = POC()
              p.filename = mymap.json
        '''
        return self.fn
    @filename.setter
    def filename(self, fn):
        self.fn = str(fn)

    @property
    def location(self):
        '''
        location information, can be used for snmp location
        synopsis:
            p = POC()
            p.location = 'row C : rack 17'
        '''
        return self._location
    @location.setter
    def location(self, x):
        self._location = x

    @property
    def role(self):
        '''
        returns the current role set() for sid
           synopsis:
              p = POC()
              p.role = 'spine'
              p.role = 'pim_rp'
              print('p.role {}'.format(p.role)) # {"pim_rp", "spine"}
        '''
        return self._role
    @role.setter
    def role(self,x):
        '''
        adds a role to role set() for sid
           synopsis:
              p = POC()
              p.role = 'spine'
              p.role = 'pim_rp'
              print('p.role {}'.format(p.role)) # {"pim_rp", "spine"}
        '''
        self.verify_role(x)
        self.add_role(x)

    @property
    def sid(self):
        '''switch id of dut
           synopsis:
              p = POC()
              p.sid = 31
        '''
        return self._sid
    @sid.setter
    def sid(self, x):
        if self.verify.is_digits(x):
            self._sid = int(x)
            return
        self.log.error("exiting. expected digits for switch ID. got {}".format(x))
        exit(1)

    @property
    def username(self):
        '''username for dut
           synopsis:
              p = POC()
              p.username = 'admin'
        '''
        return self._username
    @username.setter
    def username(self, x):
        self._username = x

    @property
    def password(self):
        '''password for dut
           synopsis:
              p = POC()
              p.password = 'mypassword'
        '''
        return self._password
    @password.setter
    def password(self, x):
        self._password = x

    @property
    def ts_password1(self):
        '''terminal server password for dut's console1
           synopsis:
              p = POC()
              p.ts_password1 = 'mypassword'
        '''
        return self._ts_password1
    @ts_password1.setter
    def ts_password1(self, x):
        self._ts_password1 = x

    @property
    def ts_password2(self):
        '''terminal server password for dut's console2
           synopsis:
              p = POC()
              p.ts_password2 = 'mypassword'
        '''
        return self._ts_password2
    @ts_password2.setter
    def ts_password2(self, x):
        self._ts_password2 = x

    @property
    def hostname(self):
        '''hostname of dut
           synopsis:
              p = POC()
              p.hostname = 'spine_1'
        '''
        return self._hostname
    @hostname.setter
    def hostname(self, x):
        self._hostname = x

    @property
    def mgmt_ip(self):
        '''management ip address of dut (usually interface mgmt0)
           synopsis:
              p = POC()
              p.mgmt_ip = '172.29.156.1'
        '''
        return self._mgmt_ip
    @mgmt_ip.setter
    def mgmt_ip(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._mgmt_ip = x
            return
        print("WARNING: Invalid mgmt_ip {}. Setting mgmt_ip to False".format(x))
        self._mgmt_ip = False

    @property
    def mgmt_ip_prefixlen(self):
        '''management ip address prefixlen of dut (usually interface mgmt0)
           synopsis:
              p = POC()
              p.mgmt_ip_prefixlen = 24
        '''
        return self._mgmt_ip_prefixlen
    @mgmt_ip_prefixlen.setter
    def mgmt_ip_prefixlen(self, x):
        if self.verify.is_ipv4_mask(x):
            self._mgmt_ip_prefixlen = x
            return
        print("WARNING: Invalid mgmt_ip_prefixlen {}. Setting mgmt_ip_prefixlen to False".format(x))
        self._mgmt_ip_prefixlen = False


    @property
    def mgmt_ipv6(self):
        '''management ipv6 address of dut (usually interface mgmt0)
           synopsis:
              p = POC()
              p.mgmt_ipv6 = '2001::14'
        '''
        return self._mgmt_ipv6
    @mgmt_ipv6.setter
    def mgmt_ipv6(self, x):
        if x == None:
            self._mgmt_ipv6 = False
            return
        if x == False:
            self._mgmt_ipv6 = False
            return
        if self.verify.is_ipv6_unicast_address(x):
            self._mgmt_ipv6 = x
            return
        print("WARNING: Invalid mgmt_ipv6 {}. Setting mgmt_ipv6 to False".format(x))
        self._mgmt_ipv6 = False

    @property
    def mgmt_ipv6_prefixlen(self):
        '''management ipv6 address prefixlen/mask of dut (usually interface mgmt0)
           synopsis:
              p = POC()
              p.mgmt_ipv6_prefixlen = 126
        '''
        return self._mgmt_ipv6_prefixlen
    @mgmt_ipv6_prefixlen.setter
    def mgmt_ipv6_prefixlen(self, x):
        if x == None:
            self._mgmt_ipv6_prefixlen = False
            return
        if x == False:
            self._mgmt_ipv6_prefixlen = False
            return
        if self.verify.is_ipv6_mask(x):
            self._mgmt_ipv6_prefixlen = x
            return
        print("WARNING: Invalid mgmt_ipv6_prefixlen {}. Setting mgmt_ipv6_prefixlen to False".format(x))
        self._mgmt_ipv6_prefixlen = False

    @property
    def gateway(self):
        '''gateway ip address of dut
           synopsis:
              p = POC()
              p.gateway = '172.29.156.1'
        '''
        return self._gateway
    @gateway.setter
    def gateway(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._gateway = x
            return
        print("WARNING: Invalid gateway {}. Setting gateway to False".format(x))
        self._gateway = False

    @property
    def gateway_ipv6(self):
        '''ipv6 address of dut gateway
           synopsis:
              p = POC()
              p.gateway_ipv6 = '2001:420:283:2000:3:11:160::1'
        '''
        return self._gateway_ipv6
    @gateway_ipv6.setter
    def gateway_ipv6(self, x):
        if x == None:
            self._gateway_ipv6 = False
            return
        if x == False:
            self._gateway_ipv6 = False
            return
        if self.verify.is_ipv6_unicast_address(x):
            self._gateway_ipv6 = x
            return
        print("WARNING: Invalid gateway_ipv6 {}. Setting gateway to False".format(x))
        self._gateway_ipv6 = False

    @property
    def nameserver(self):
        '''
        DEPRECATED. Use dns_server1 and dns_server2
        ip address of nameserver
           synopsis:
              p = POC()
              p.nameserver = '171.70.168.183'
        '''
        return self._nameserver
    @nameserver.setter
    def nameserver(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._nameserver = x
            return
        print("WARNING: Invalid nameserver {}. Setting nameserver to False".format(x))
        self._nameserver = False

    @property
    def dns_server1(self):
        '''
        ip address of primary nameserver
           synopsis:
              p = POC()
              p.dns_server1 = '171.70.168.183'
        '''
        return self._dns_server1
    @dns_server1.setter
    def dns_server1(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._dns_server1 = x
            return
        print("WARNING: Invalid dns_server1 {}. Setting dns_server1 to False".format(x))
        self._dns_server1 = False

    @property
    def dns_server2(self):
        '''
        ip address of secondary nameserver
           synopsis:
              p = POC()
              p.dns_server2 = '171.70.168.183'
        '''
        return self._dns_server2
    @dns_server2.setter
    def dns_server2(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._dns_server2 = x
            return
        print("WARNING: Invalid dns_server2 {}. Setting dns_server2 to False".format(x))
        self._dns_server2 = False

    @property
    def ntp_server1(self):
        '''ip address of primary ntp_server
           synopsis:
              p = POC()
              p.ntp_server1 = '172.29.167.1'
        '''
        return self._ntp_server1
    @ntp_server1.setter
    def ntp_server1(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ntp_server1 = x
            return
        print("WARNING: Invalid ntp_server1 {}. Setting ntp_server1 to False".format(x))
        self._ntp_server1 = False

    @property
    def ntp_server2(self):
        '''ip address of secondary ntp_server
           synopsis:
              p = POC()
              p.ntp_server2 = '172.29.167.2'
        '''
        return self._ntp_server2
    @ntp_server2.setter
    def ntp_server2(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ntp_server2 = x
            return
        print("WARNING: Invalid ntp_server2 {}. Setting ntp_server2 to False".format(x))
        self._ntp_server2 = False

    @property
    def apc_ip1(self):
        '''apc ip address for dut corresponding to apc_outlet1
           synopsis:
               p = POC()
               p.apc_ip1 = '172.22.150.31'
        '''
        return self._apc_ip1
    @apc_ip1.setter
    def apc_ip1(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._apc_ip1 = x
            return
        print("WARNING: Invalid apc_ip1 {}. Setting to null".format(x))
        self._apc_ip1 = False

    @property
    def apc_ip2(self):
        '''apc ip address for dut corresponding to apc_outlet2
           synopsis:
               p = POC()
               p.apc_ip2 = '172.22.150.31'
        '''
        return self._apc_ip2
    @apc_ip2.setter
    def apc_ip2(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._apc_ip2 = x
            return
        print("WARNING: Invalid apc_ip2 {}. Setting to null".format(x))
        self._apc_ip2 = False

    @property
    def apc_ip3(self):
        '''apc ip address for dut corresponding to apc_outlet3
           synopsis:
               p = POC()
               p.apc_ip3 = '172.22.150.31'
        '''
        return self._apc_ip3
    @apc_ip3.setter
    def apc_ip3(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._apc_ip3 = x
            return
        print("WARNING: Invalid apc_ip3 {}. Setting to null".format(x))
        self._apc_ip3 = False

    @property
    def apc_ip4(self):
        '''apc ip address for dut corresponding to apc_outlet4
           synopsis:
               p = POC()
               p.apc_ip4 = '172.22.150.31'
        '''
        return self._apc_ip4
    @apc_ip4.setter
    def apc_ip4(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._apc_ip4 = x
            return
        print("WARNING: Invalid apc_ip4 {}. Setting to null".format(x))
        self._apc_ip4 = False

    @property
    def apc_outlet1(self):
        '''apc outlet for dut corresponding to apc_ip1
           synopsis:
               p = POC()
               p.apc_outlet1 = 7
        '''
        return self._apc_outlet1
    @apc_outlet1.setter
    def apc_outlet1(self, x):
        if self.verify.is_digits(x):
            self._apc_outlet1 = int(x)
            return
        print("WARNING: Invalid apc_outlet1 {}. Setting to null".format(x))
        self._apc_outlet1 = False

    @property
    def apc_outlet2(self):
        '''apc outlet for dut corresponding to apc_ip2
           synopsis:
               p = POC()
               p.apc_outlet2 = 7
        '''
        return self._apc_outlet2
    @apc_outlet2.setter
    def apc_outlet2(self, x):
        if self.verify.is_digits(x):
            self._apc_outlet2 = int(x)
            return
        print("WARNING: Invalid apc_outlet2 {}. Setting to null".format(x))
        self._apc_outlet2 = False

    @property
    def apc_outlet3(self):
        '''apc outlet for dut corresponding to apc_ip3
           synopsis:
               p = POC()
               p.apc_outlet3 = 7
        '''
        return self._apc_outlet3
    @apc_outlet3.setter
    def apc_outlet3(self, x):
        if self.verify.is_digits(x):
            self._apc_outlet3 = int(x)
            return
        print("WARNING: Invalid apc_outlet3 {}. Setting to null".format(x))
        self._apc_outlet3 = False

    @property
    def apc_outlet4(self):
        '''apc outlet for dut corresponding to apc_ip4
           synopsis:
               p = POC()
               p.apc_outlet4 = 7
        '''
        return self._apc_outlet4
    @apc_outlet4.setter
    def apc_outlet4(self, x):
        if self.verify.is_digits(x):
            self._apc_outlet4 = int(x)
            return
        print("WARNING: Invalid apc_outlet4 {}. Setting to null".format(x))
        self._apc_outlet4 = False

    @property
    def ts_ip1(self):
        '''
        ip address of terminal server associated with 1st console port for dut
          synopsis:
              p = POC()
              p.ts_ip1 = '172.22.150.31'
        '''
        return self._ts_ip1
    @ts_ip1.setter
    def ts_ip1(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ts_ip1 = x
            return
        print("WARNING: Invalid ts_ip1 {}. Setting to null".format(x))
        self._ts_ip1 = False

    @property
    def ts_ip2(self):
        '''
        ip address of terminal server associated with 2nd console port, if any, for dut
        synopsis:
            p = POC()
            p.ts_ip2 = '172.22.150.31'
        '''
        return self._ts_ip2
    @ts_ip2.setter
    def ts_ip2(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ts_ip2 = x
            return
        print("WARNING: Invalid ts_ip2 {}. Setting to null".format(x))
        self._ts_ip2 = False

    @property
    def ts_port1(self):
        '''
        2nd console port, if any, for dut
        synopsis:
            p = POC()
            p.ts_port1 = 2003
        '''
        return self._ts_port1
    @ts_port1.setter
    def ts_port1(self, x):
        if self.verify_console_port(x):
            self._ts_port1 = x
            return
        print("WARNING: Invalid ts_port1 {}. Setting to null".format(x))
        self._ts_port1 = False


    @property
    def ts_port2(self):
        '''
        2nd console port, if any, for dut
        synopsis:
            p = POC()
            p.ts_port2 = 2003
        '''
        return self._ts_port2
    @ts_port2.setter
    def ts_port2(self, x):
        if self.verify_console_port(x):
            self._ts_port2 = x
            return
        print("WARNING: Invalid ts_port2 {}. Setting to null".format(x))
        self._ts_port2 = False




    def commit(self):
        '''
        commit info for the currently-defined dut. This only updates user items which are not set to False
        '''
        if self.sid is False:
            print("Got sid {}. Please call p.sid() first.  Exiting.".format(self.sid))
            exit(1)
        if self.sid not in self.cfg:
            self.cfg[self.sid] = dict()
            self.cfg[self.sid]['sid'] = self.sid
        if self.ansible_host != False:
            self.cfg[self.sid]['ansible_host'] = self.ansible_host
        if self.contact != False:
            self.cfg[self.sid]['contact'] = self.contact
        if self.location != False:
            self.cfg[self.sid]['location'] = self.location
        if self.mgmt_ip != False:
            self.cfg[self.sid]['mgmt_ip'] = self.mgmt_ip
        if self.mgmt_ip_prefixlen != False:
            self.cfg[self.sid]['mgmt_ip_prefixlen'] = self.mgmt_ip_prefixlen
        if self.mgmt_ipv6 != False:
            self.cfg[self.sid]['mgmt_ipv6'] = self.mgmt_ipv6
        if self.mgmt_ipv6_prefixlen != False:
            self.cfg[self.sid]['mgmt_ipv6_prefixlen'] = self.mgmt_ipv6_prefixlen
        if self.gateway != False:
            self.cfg[self.sid]['gateway'] = self.gateway
        if self.nameserver != False:
            self.cfg[self.sid]['nameserver'] = self.nameserver
        if self.dns_server1 != False:
            self.cfg[self.sid]['dns_server1'] = self.dns_server1
        if self.dns_server2 != False:
            self.cfg[self.sid]['dns_server2'] = self.dns_server2
        if self.ntp_server1 != False:
            self.cfg[self.sid]['ntp_server1'] = self.ntp_server1
        if self.ntp_server2 != False:
            self.cfg[self.sid]['ntp_server2'] = self.ntp_server2
        if self.hostname != False:
            self.cfg[self.sid]['hostname'] = self.hostname
        if self.username != False:
            self.cfg[self.sid]['username'] = self.username
        if self.password != False:
            self.cfg[self.sid]['password'] = self.password
        if len(self.role) != 0:
            self.cfg[self.sid]['role'] = [str(x) for x in self._role.copy()] # JSON cannot store a set, so convert to list()

        if self.ts_password1 != False:
            self.cfg[self.sid]['ts_password1'] = self.ts_password1
        if self.ts_password2 != False:
            self.cfg[self.sid]['ts_password2'] = self.ts_password2

        if self.ts_ip1 != False:
            self.cfg[self.sid]['ts_ip1'] = self.ts_ip1
        if self.ts_port1 != False:
            self.cfg[self.sid]['ts_port1'] = self.ts_port1
        if self.ts_ip2 != False:
            self.cfg[self.sid]['ts_ip2'] = self.ts_ip2
        if self.ts_port2 != False:
            self.cfg[self.sid]['ts_port2'] = self.ts_port2

        if self.apc_ip1 != False:
            self.cfg[self.sid]['apc_ip1'] = self.apc_ip1
        if self.apc_ip2 != False:
            self.cfg[self.sid]['apc_ip2'] = self.apc_ip2
        if self.apc_ip3 != False:
            self.cfg[self.sid]['apc_ip3'] = self.apc_ip3
        if self.apc_ip4 != False:
            self.cfg[self.sid]['apc_ip4'] = self.apc_ip4
        if self.apc_outlet1 != False:
            self.cfg[self.sid]['apc_outlet1'] = self.apc_outlet1
        if self.apc_outlet2 != False:
            self.cfg[self.sid]['apc_outlet2'] = self.apc_outlet2
        if self.apc_outlet3 != False:
            self.cfg[self.sid]['apc_outlet3'] = self.apc_outlet3
        if self.apc_outlet4 != False:
            self.cfg[self.sid]['apc_outlet4'] = self.apc_outlet4

        # Below are deprecated.  We set self.cfg to their corresponding
        # non-deprecated keys if the user accesses them
        if self.console_ip1 != False:
            self.cfg[self.sid]['ts_ip1'] = self.console_ip1
        if self.console_port1 != False:
            self.cfg[self.sid]['ts_port1'] = self.console_port1
        if self.console_ip2 != False:
            self.cfg[self.sid]['ts_ip2'] = self.console_ip2
        if self.console_port2 != False:
            self.cfg[self.sid]['ts_port2'] = self.console_port2

        # we bypass setter validations here to avoid warning messages
        self._sid = False
        self._ansible_host = False
        self._contact = False
        self._location = False
        self._mgmt_ip = False
        self._mgmt_ip_prefixlen = False
        self._mgmt_ipv6 = False
        self._mgmt_ipv6_prefixlen = False
        self._gateway = False
        self._nameserver = False
        self._dns_server1 = False
        self._dns_server2 = False
        self._ntp_server1 = False
        self._ntp_server2 = False
        self._hostname = False
        self._username = False
        self._password = False
        self._role = set()
        self._apc_ip1 = False
        self._apc_ip2 = False
        self._apc_ip3 = False
        self._apc_ip4 = False
        self._apc_outlet1 = False
        self._apc_outlet2 = False
        self._apc_outlet3 = False
        self._apc_outlet4 = False
        self._ts_password1 = False
        self._ts_password2 = False
        self._ts_ip1 = False
        self._ts_port1 = False
        self._ts_ip2 = False
        self._ts_port2 = False

        # below are deprecated
        self._console_ip1 = False
        self._console_port1 = False
        self._console_ip2 = False
        self._console_port2 = False


    def save(self):
        if len(self.cfg) == 0:
            print("Nothing to save. Exiting.")
            exit(1)
        if self.fn == None:
            print("Call instance.filename = myfile first.  Exiting.")
            exit(1)
        with open(self.fn, "w") as fh:
            json.dump(self.cfg, fh)



    # methods and properties below are deprecated
    # please do not use

    @property
    def console_ip1(self):
        '''
        DEPRECATED. Use ts_ip1 instead
        console ip address for dut
           synopsis:
               p = POC()
               p.console_ip = '172.22.150.31'
        '''
        return self._ts_ip1
    @console_ip1.setter
    def console_ip1(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ts_ip1 = x
            return
        print("WARNING: Invalid ts_ip1 {}. Setting to null".format(x))
        self._ts_ip1 = False

    @property
    def console_port1(self):
        '''
        DEPRECATED. Use ts_port1 instead
        '''
        return self._ts_port1
    @console_port1.setter
    def console_port1(self, x):
        if self.verify_console_port(x):
            self._ts_port1 = x
            return
        print("WARNING: Invalid console_port {}. Setting to null".format(x))
        self._ts_port1 = False

    @property
    def console_ip2(self):
        '''
        DEPRECATED. Use ts_ip2 instead
        '''
        return self._ts_ip2
    @console_ip2.setter
    def console_ip2(self, x):
        if self.verify.is_ipv4_unicast_address(x):
            self._ts_ip2 = x
            return
        print("WARNING: Invalid ts_ip2 {}. Setting to null".format(x))
        self._ts_ip2 = False

    @property
    def console_port2(self):
        '''
        DEPRECATED. Use ts_port2 instead
        '''
        return self._ts_port2
    @console_port2.setter
    def console_port2(self, x):
        if self.verify_console_port(x):
            self._ts_port2 = x
            return
        print("WARNING: Invalid console_port {}. Setting to null".format(x))
        self._ts_port2 = False

