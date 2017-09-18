import os, sys
import logging
sys.path.append(os.path.dirname(__file__))

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
STATICPATH = os.path.join(LOCALPATH, 'resources')

ITEM_NOT_IN_INVENTORY = '{} is not in {} inventory'


class log_msg(object):

    ITEM_NOT_IN_INVENTORY = '{} is not in {} inventory'