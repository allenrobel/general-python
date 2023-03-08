#!/usr/bin/env python

import argparse

class commonParser:
    def __init__(self):
        self.cArgs = argparse.ArgumentParser(add_help=False)
        self.addCommonArgs(self.cArgs)
    def addCommonArgs(self,cArgs):
        #mandatory = cArgs.add_argument_group(title='MANDATORY ARGUMENTS', description="Must be present")
        #default   = cArgs.add_argument_group(title='DEFAULT ARGUMENTS', description="If absent, a default will be provided")

        cArgs.add_argument('--dut', dest='dut', required=True,
                     help='ip address or hostname of the DUT')
        cArgs.add_argument('--username', dest='username', default='admin',
                     help='username on the DUT')
        cArgs.add_argument('--password', dest='password', default='mypassword',
                     help='password on the DUT')
        self.commonArgs = cArgs.parse_args()
        return(self.commonArgs)
