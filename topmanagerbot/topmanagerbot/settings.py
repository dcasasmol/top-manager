# -*- coding: utf-8 -*-

# Scrapy settings for topmanagerbot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys


########## DJANGO CONFIGURATION
# Setting up Django's project full path
DJANGO_PROJECT_PATH = '/home/dcasas/projects/top-manager.es/topmanagerweb'
sys.path.insert(0, DJANGO_PROJECT_PATH)

# Setting up Django's settings module name. This module is located at:
# /home/dcasas/projects/top-manager.es/topmanagerweb/topmanagerweb/settings/local.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'topmanagerweb.settings.local'
########## END DJANGO CONFIGURATION

########## CRAWLER CONFIGURATION
BOT_NAME = 'topmanagerbot'

SPIDER_MODULES = ['topmanagerbot.spiders']
NEWSPIDER_MODULE = 'topmanagerbot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'topmanagerbot (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0'
########## END CRAWLER CONFIGURATION
