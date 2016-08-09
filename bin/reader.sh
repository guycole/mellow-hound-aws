#!/bin/bash
#
# Title:reader.sh
# Description:read SQS for fresh mellow file cues
# Development Environment:OS X 10.10.5
# Author:G.S. Cole (guycole at gmail dot com)
#
PATH=/bin:/usr/bin:/etc:/usr/local/bin; export PATH
#
PYTHONPATH=/home/gsc/github/mellow-hound-aws/src/main/python/mellow_hound; export PYTHONPATH
#
/usr/bin/logger -i -p local3.info reader start
/home/gsc/github/mellow-hound-aws/src/main/python/mellow_hound/reader.py /home/gsc/github/mellow-hound-aws/src/main/python/mellow_hound/config.db
/home/gsc/github/mellow-hound-aws/src/main/python/mellow_hound/loader.py /home/gsc/github/mellow-hound-aws/src/main/python/mellow_hound/config.db
#
/usr/bin/logger -i -p local3.info reader stop
#
