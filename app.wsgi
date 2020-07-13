#!/usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/alvin/PycharmProjects/etsi-qkd-api/')

from project import app as application
application.secret_key = 'anything you wish'