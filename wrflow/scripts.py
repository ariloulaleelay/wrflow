#!/usr/bin/env python
# coding: utf8

import argparse
import logging
import os
from wrflow.config import default_config

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('root')


def initdb(args, config):
    logger.info("starting initdb")


def main():
    parser = argparse.ArgumentParser(description='Wrflow control script')
    parser.add_argument('--config', default=os.environ['WRFLOW_CONFIG'])

    subparsers = parser.add_subparsers(help='subcommands')
    parser_command = subparsers.add_parser("initdb")
    parser_command.set_defaults(func=initdb)

    args = parser.parse_args()
    config = default_config(args.config)
    args.func(args, config)

if __name__ == '__main__':
    main()
