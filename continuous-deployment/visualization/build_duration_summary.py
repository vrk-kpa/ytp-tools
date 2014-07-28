#!/usr/bin/env python

import sys
import os
import glob
from collections import defaultdict
from operator import itemgetter
import json
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parse_task_durations_from_log_files():
    
    log_directory = '../deployment_cache'
    results = defaultdict(list)

    for build_directory in os.walk(log_directory).next()[1]:
        logfile_list = sorted(glob.glob(log_directory + '/' + build_directory + '/time_log_*.log'))    
        timestamp = int(build_directory.strip('cd-ytp-')[:-3])

        if len(logfile_list) != 5:
            log.warn("could not find excepted log files for build {0}".format(build_directory))
            continue

        for playbook_logfile in logfile_list[1:3]:
            with open(playbook_logfile, 'r') as logfile:
                for task_line in logfile:
                    split = task_line.replace('\n', '')
                    split = split.split(' s, ')
                    duration = float(split[0])

                    split = split[1].split(' | ')

                    if len(split) == 2:
                        results['{0} ({1})'.format(split[1], split[0])].append({"x": timestamp, "y": duration})
                    elif len(split) == 1:
                        results['{0} (no role)'.format(split[0])].append({"x": timestamp, "y": duration})
                    else:
                        log.error("Encountered unparseable line {0}".format(task_line))
                        sys.exit()
    return results


def transform_data_for_rickshaw(results):
    series = []
    for task, durations in results.iteritems():
        series.append({"name": task, "data": sorted(durations, key=itemgetter('x')) })
    return series


def write_data_as_json_to_file(data, filename):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile)


if __name__ == "__main__":
    results = parse_task_durations_from_log_files()
    write_data_as_json_to_file(transform_data_for_rickshaw(results), "results.json")
