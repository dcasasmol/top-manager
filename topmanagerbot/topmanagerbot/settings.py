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


########## CRAWLER CONFIGURATION
BOT_NAME = u'topmanagerbot'

TM_HOST_NAME = u'transfermarkt.com'

TM_LEAGUES = [
    u'/primera-division/startseite/wettbewerb/ES1',
]

DEFAULT_NA = u'N/A'

SPIDER_MODULES = [u'topmanagerbot.spiders']
NEWSPIDER_MODULE = u'topmanagerbot.spiders'

ITEM_PIPELINES = {
    u'topmanagerbot.pipelines.DuplicatesPipeline': 100,
    u'topmanagerbot.pipelines.ProcessPipeline': 200,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = u'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0'
########## END CRAWLER CONFIGURATION

########## DJANGO CONFIGURATION
# Setting up Django's project full path
DJANGO_PROJECT_PATH = u'/home/dcasas/projects/top-manager.es/topmanagerweb'
sys.path.insert(0, DJANGO_PROJECT_PATH)

# Setting up Django's settings module name. This module is located at:
# /home/dcasas/projects/top-manager.es/topmanagerweb/topmanagerweb/settings/local.py
os.environ[u'DJANGO_SETTINGS_MODULE'] = u'topmanagerweb.settings.local'
########## END DJANGO CONFIGURATION
