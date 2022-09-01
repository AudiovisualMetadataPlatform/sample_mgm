#!/bin/env python3

from amp.package import *
import argparse
import logging
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil

def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("--debug", default=False, action="store_true", help="Turn on debugging")    
    parser.add_argument("--package", default=False, action="store_true", help="Build package instead of install")
    parser.add_argument("destination", help="Destination for build (should be an AMP_ROOT for non-package)")
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)-8s] (%(filename)s:%(lineno)d)  %(message)s",
                        level=logging.DEBUG if args.debug else logging.INFO)

    # Build the software
    # this is a simple script MGM, so there's nothing to really build
    # here, but if there were, here's where it'd be done.
    pass



    # Install the software
    # This is going to copy the files we need to use the MGM -- but not
    # the stuff that goes into the package (like the lifecycle scripts
    # and config defaults).  One assumes that prior to installation the
    # developer has put the configuration in their amp.yaml configuration
    # for testing    
    # Since this is an MGM, the installation path is 'galaxy/tools/sample_mgm' 
    # so it's separate from other MGMs.
    installation_path = "galaxy/tools/sample_mgm"

    destdir = Path(args.destination)
    if args.package:
        # create a temporary directory for the build.
        tempdir = tempfile.TemporaryDirectory()
        destdir = Path(tempdir.name)

    # create our installation path
    (destdir / installation_path).mkdir(parents=True, exist_ok=True)
    # we're only going to copy the MGM code and the galaxy interface
    # file to the destination
    try: 
        for file in ('sample_mgm.py', 'sample_mgm.xml'):        
            src = sys.path[0] + "/" + file
            dst = destdir / installation_path / file
            logging.info(f"Copying {src!s} -> {dst!s}")
            shutil.copyfile(src, dst)
            # make sure the permissions get copied too...
            shutil.copystat(src, dst)    
    except Exception as e:
        logging.error(f"Failed to copy files: {e}")
        exit(1)

    # Package it, if needed
    if args.package:
        try:
            new_package = create_package(Path(args.destination), destdir / installation_path,
                                         metadata={'name': 'sample_mgm', 
                                                   'version': '1.0', 
                                                   'install_path': installation_path},
                                         # install all of the hooks, just to show how it's done
                                         hooks={'pre': 'pre_script.py',
                                                'post': 'post_script.py',
                                                'config': 'config_script.py'},
                                         # we're also extending the configuration
                                         # so we need to let the packager know 
                                         defaults=Path("sample_mgm.default"),
                                         # There's nothing here that is architecture specific
                                         arch_specific=False,
                                         # specify which packages we require to be installed
                                         # can also be a list.
                                         depends_on='galaxy')
            logging.info(f"New package in {new_package}")    
        except Exception as e:
            logging.error(f"Failed to build backage: {e}")
            exit(1)


if __name__ == "__main__":
    main()