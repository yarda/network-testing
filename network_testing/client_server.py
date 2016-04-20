# -*- coding: utf-8 -*-
from __future__ import print_function

import argparse
import logging
import os
import subprocess

from .test_suite import TestCase, TestSuite, testcase_path

SOCKET_OPERATIONS = set(['bind', 'listen', 'accept', 'connect', 'getsockopt', 'shutdown', 'close'])
PROCESS_SYSCALLS = set(['close', 'execve', 'fork', 'clone'])


def main():
    if os.geteuid() != 0:
        print("You have to be root to run the test driver. Please use sudo.")
        exit(1)

    parser = argparse.ArgumentParser(description="Test driver for client-server networking applications.")
    parser.add_argument("--debug", "-d", action="store_true", help="Print debug messages.")
    parser.add_argument("--list-testcases", "-l", action="store_true", help="List testcases and scenarios.")
    parser.add_argument("--list-scenarios", action="store_true", help="List testcases and scenarios.")
    parser.add_argument("--deps", action="store_true", help="List dependencies.")
    parser.add_argument("--outdir", default="./json-output/", help="List dependencies.")
    parser.add_argument("testcases", nargs="?")
    parser.add_argument("scenarios", nargs="?")
    options = parser.parse_args()

    if options.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    testcases = options.testcases and options.testcases.split(',')
    scenarios = options.scenarios and options.scenarios.split(',')

    suite = TestSuite(testcases, scenarios)
    if options.list_testcases:
        for testcase in suite.testcases:
            print(testcase.name)
        exit(0)
    elif options.list_scenarios:
        for scenario in TestCase.scenario_classes:
            print(scenario.name)
        exit(0)
    elif options.deps:
        for testcase in suite.testcases:
            path = os.path.join(testcase_path, testcase.name, "deps")
            if os.path.isfile(path):
                subprocess.check_call(['cat', path])
        exit(0)
    else:
        suite.run()
        suite.save(options.outdir)
        suite.report()

    exit(0 if suite.result else 1)

if __name__ == '__main__':
    main()
