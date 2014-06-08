# -*- coding: utf-8 -*-
import os
import ConfigParser

cfg = ConfigParser.RawConfigParser()
cfg.read(os.path.join(os.path.dirname(__file__),'config.cfg'))
#print 'config.py'
def get_config(option):
    return cfg.get('urqa',option)



