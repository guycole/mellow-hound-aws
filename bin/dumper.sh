#!/bin/bash
#
# Title:dumper.sh
# Description:dump database to S3
# Development Environment:OS X 10.10.5
# Author:G.S. Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
PYTHONPATH=/home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata; export PYTHONPATH
#
/usr/bin/logger -i -p local3.info dumper start
/home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata/dumper.py /home/gsc/github/mythic-crux-aws/mythic-eoddata/src/main/python/mythic_eoddata/config.db /usr/bin/logger -i -p local3.info dumper stop
#
