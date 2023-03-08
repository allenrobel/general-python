'''
Summary: 
   Common command line arguments for overlay configuration scripts.
Description:
   Contains common arguments for overlay configuration scripts

NOTES:
    20191126 - needs to be finished and tested with a convergence script.

'''
# standard libraries
import argparse
from general_python.log import get_logger
from general_python.verify_types import VerifyTypes

our_version = 100
script_name = 'args_convergence'
log = get_logger(script_name, 'INFO', 'DEBUG')
verify = VerifyTypes(log)

VALID_OVERLAY = ['ipv4', 'ipv6', 'na']
# VALID_TRAFFIC_PATTERNS
# We unify the syntax for Barefoot and Spirent with the following
# mappings inside their respective libraries:
#    For Barefoot, VALID_BF_TRAFFIC_PATTERNS = ['pair', 'bipartite']
#    For Spirent,  VALID_TRAFFIC_PATTERNS = ['PAIR', BACKBONE']
#    For Barefoot, L2 is mapped to 'pair'
#    For Spirent,  L2 is mapped to 'PAIR'
#    For Barefoot, L3 is mapped to 'bipartite'
#    For Spirent,  L3 is mapped to 'BACKBONE'
#
# Hence, when the user passes 'L2', this is converted to:
#     Barefoot 'pair'
#     Spirent: 'PAIR'
# And when the user passes 'L3', this is converted to:
#     Barefoot: 'bipartite'
#     Spirent: 'BACKBONE'
VALID_TRAFFIC_PATTERNS = ['L2', 'L3']
VALID_UNDERLAY = ['ipv4', 'ipv6']

default_loglevel = 'INFO'


ArgsConvergence = argparse.ArgumentParser(add_help=False)

mandatory = ArgsConvergence.add_argument_group(title='MANDATORY CONVERGENCE ARGS')
default   = ArgsConvergence.add_argument_group(title='DEFAULT CONVERGENCE ARGS', description="If absent, a default will be provided")


help_arp       = 'Default 3.  An integer representing how many times to send and retry ARP resolution before each testcase.  If set to 0, no ARPs will be sent.  Useful if you want to just send traffic without verifing ARP'
help_build     = 'a string representing the build being tested'
help_cfg_dir   = 'path to directory containing testcase configurations for DUTs'
help_full_results = 'If present, write JSON file with full TX/RX packet counts in --json_dir Default: full result is not saved.'
help_json_dir   = 'directory to which testcase results are written'
help_loglevel  = 'Logging level for this script (INFO | WARNING | ERROR | DEBUG)'
help_logfile   = 'if present, file to which logging output is saved'
help_map       = 'testbed map file from which switch IP addresses, etc is read'
help_nve_sids = 'If present, a comma-separated list of switch IDs.  These are verified for consistency using show nve peers ='
help_overlay = 'Either ipv4, ipv6, or na.  Used to determine if VTEP peer should be verified and, if so, whether ipv4 VTEP or ipv6 VTEP should be verified'
help_overwrite = 'By default, if a testcase CSV result already exists, we skip the test.  If --overwrite is used, we do not skip the test and we overwrite the prior CSV file'
help_runs      = 'Number of test runs/trials to iterate over (default is 1)'
help_skip_test = 'Run the traffic, etc, but do not issue perturbances on the DUTs'
help_start_run_id = 'Starting run ID. Affects result filename numbering. Default is run1, run2...'
help_tg       = 'ipv4 address of traffic generator'
help_testbed  = 'testbed in which convergence tests are run.  This impacts platform-specific verifications'
help_testcase_info = 'JSON file from which testcase parameters are read'
help_traffic_pattern = 'traffic pattern: One of {}'.format(VALID_TRAFFIC_PATTERNS)
help_underlay = 'Either ipv4, ipv6.  Is added to [meta][underlay] in result json. This sets the Underlay field in the title page of the report.'

help_vpc = 'If present, one VTEP is a VPC peer.  Else, All VTEP are standalone'
help_vpc_interfaces = 'If present, a comma-separated list of port-channel interfaces.  These are verified for consistency using show vpc consistency-parameters interface <interface>'
help_vpc_sids = 'If present, a comma-separated list of switch IDs.  These are verified for consistency using show vpc consistency-parameters...'

ex_prefix = 'Example: '
ex_arp       = '{} --arp 5'.format(ex_prefix)
ex_build     = '{} --build iplus_dev_654'.format(ex_prefix)
ex_cfg_dir   = '{} --cfg_dir /home/arobel/repos/poc/fb4/cfg/tc'.format(ex_prefix)
ex_full_results = '{} --full_results'.format(ex_prefix)
ex_json_dir   = '{} --json_dir /home/arobel/repos/poc/fb4/json'.format(ex_prefix)
ex_logfile   = '{} --logfile /tmp/myscript.log'.format(ex_prefix)
ex_loglevel  = '{} --loglevel ERROR'.format(ex_prefix)
ex_map       = '{} --map /users/arobel/repos/poc/sfdc/topo/vxlan.map'.format(ex_prefix)
ex_nve_sids = '{} --nve_sids 101,102,104'.format(ex_prefix)
ex_overlay = '{} --overlay ipv6'.format(ex_prefix)
ex_overwrite = '{} --overwrite'.format(ex_prefix)
ex_runs      = '{} --runs 3'.format(ex_prefix)
ex_start_run_id = '{} --start_run_id 4  results in run4, run5...'.format(ex_prefix)
ex_skip_test = '{} --skip_test'.format(ex_prefix)
ex_testbed   = '{} --testbed telstra'.format(ex_prefix)
ex_testcase_info = '{} --testcase_info /users/arobel/repos/fb4/py/ebgp_all.json'.format(ex_prefix)
ex_tg            = '{} --tg 172.22.159.5'.format(ex_prefix)
ex_traffic_pattern = '{} --traffic_pattern BACKBONE'.format(ex_prefix)
ex_underlay = '{} --underlay ipv6'.format(ex_prefix)

ex_vpc = '{} --vpc'.format(ex_prefix)
ex_vpc_interfaces = '{} --vpc_interfaces Po1,Po10'.format(ex_prefix)
ex_vpc_sids = '{} --vpc_sids 101,102'.format(ex_prefix)


default.add_argument('--arp',
               dest='arp',
               required=False,
               default=3,
               help='{} {}'.format(help_arp, ex_arp))
mandatory.add_argument('--build',
               dest='build',
               required=True,
               help='{} {}'.format(help_build, ex_build))
mandatory.add_argument('--cfg_dir',
               dest='cfg_dir',
               required=True,
               help='{} {}'.format(help_cfg_dir, ex_cfg_dir))
default.add_argument('--full_results',
               dest='full_results',
               required=False,
               action='store_true',
               default=False,
               help='{} {}'.format(help_full_results, ex_full_results))
default.add_argument('--logfile',
               dest='logfile',
               required=False,
               default='',
               help='{} {}'.format(help_logfile, ex_logfile))
default.add_argument('--loglevel',
               dest='loglevel',
               required=False,
               default='INFO',
               help='{} {}'.format(help_loglevel, ex_loglevel))
mandatory.add_argument('--json_dir',
               dest='json_dir',
               required=True,
               help='{} {}'.format(help_json_dir, ex_json_dir))
mandatory.add_argument('--map',
               dest='map',
               required=True,
               help='{} {}'.format(help_map, ex_map))
default.add_argument('--overwrite',
               dest='overwrite',
               required=False,
               action='store_true',
               default=False,
               help='{} {}'.format(help_overwrite, ex_overwrite))
default.add_argument('--runs',
               dest='runs',
               required=False,
               default=1,
               help='{} {}'.format(help_runs, ex_runs))
default.add_argument('--skip_test',
               dest='skip_test',
               required=False,
               action='store_true',
               default=False,
               help='{} {}'.format(help_skip_test, ex_skip_test))
default.add_argument('--start_run_id',
               dest='start_run_id',
               required=False,
               default=1,
               help='{} {}'.format(help_start_run_id, ex_start_run_id))
mandatory.add_argument('--tg',
               dest='tg',
               required=True,
               help='{} {}'.format(help_tg, ex_tg))
mandatory.add_argument('--testbed',
               dest='testbed',
               required=True,
               help='{} {}'.format(help_testbed, ex_testbed))
mandatory.add_argument('--testcase_info',
               dest='testcase_info',
               required=True,
               help='{} {}'.format(help_testcase_info, ex_testcase_info))
default.add_argument('--traffic_pattern',
               dest='traffic_pattern',
               required=False,
               default=verify.stc.DEFAULT_TRAFFIC_PATTERN,
               help='{} {}'.format(help_traffic_pattern, ex_traffic_pattern))
default.add_argument('--vpc',
               dest='vpc',
               required=False,
               action='store_true',
               default=False,
               help='{} {}'.format(help_vpc, ex_vpc))
default.add_argument('--nve_sids',
               dest='nve_sids',
               required=False,
               default=False,
               help='{} {}'.format(help_nve_sids, ex_nve_sids))

default.add_argument('--vpc_sids',
               dest='vpc_sids',
               required=False,
               default=False,
               help='{} {}'.format(help_vpc_sids, ex_vpc_sids))

default.add_argument('--vpc_interfaces',
               dest='vpc_interfaces',
               required=False,
               default=False,
               help='{} {}'.format(help_vpc_interfaces, ex_vpc_interfaces))
mandatory.add_argument('--overlay',
               dest='overlay',
               required=True,
               help='{} {}'.format(help_overlay, ex_overlay))
mandatory.add_argument('--underlay',
               dest='underlay',
               required=True,
               help='{} {}'.format(help_underlay, ex_underlay))

