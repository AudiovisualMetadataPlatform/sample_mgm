#!/bin/env python3
# This is an example of a config script.  It will be run when
# AMP is being reconfigured.   Generally the only packages
# which will need to hook into configuration are subsystems like
# galaxy, tomcat, and the UI since they have unusual configuration
# requirements.
#
# However, this would be a place for a package to do valditity 
# checking of the user-set configuration

from amp.logging import setup_logging
from amp.config import load_amp_config
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Enable debugging")    
    args = parser.parse_args()

    setup_logging(None, args.debug)

    config = load_amp_config()

    print("Hello from the configuration script!")
    print(f"The installation directory is: {os.environ['AMP_ROOT']}")


if __name__ == "__main__":
    main()