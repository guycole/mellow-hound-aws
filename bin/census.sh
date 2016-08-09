#!/bin/bash
#
# Title:census.sh
# Description:monitor row population
# Development Environment:OS X 10.10.5
# Author:G.S. Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
PYTHONPATH=/home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata; export PYTHONPATH
#
/usr/bin/logger -i -p local3.info census start
/home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata/census.py /home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata/config.db
/usr/bin/logger -i -p local3.info census stop
#
