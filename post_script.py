#!/bin/env python3
from amp.logging import setup_logging
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true', help="Enable debugging")
    parser.add_argument('install_path', help="Where the package will be installed")
    args = parser.parse_args()

    setup_logging(None, args.debug)

    print("Hello from the post-installation script!")
    print(f"The installation directory is: {args.install_path}")


if __name__ == "__main__":
    main()


