# -*- coding: utf-8 -*-
# topmanagerbot/settings.py

import os
import sys


########## DJANGO CONFIGURATION
# Setting up Django's project full path
DJANGO_PROJECT_PATH = u'../topmanagerweb'
sys.path.insert(0, DJANGO_PROJECT_PATH)

# Setting up Django's settings module name. This module is located at:
# /home/dcasas/projects/top-manager.es/topmanagerweb/topmanagerweb/settings/local.py
os.environ[u'DJANGO_SETTINGS_MODULE'] = u'topmanagerweb.settings.local'
########## END DJANGO CONFIGURATION

########## CRAWLER CONFIGURATION
BOT_NAME = u'topmanagerbot'

TM_HOST_NAME = u'transfermarkt.com'

TM_LEAGUES = [
    u'/primera-division/startseite/wettbewerb/ES1',
]

DEFAULT_NA = u'N/A'

SPIDER_MODULES = [u'topmanagerbot.spiders']
NEWSPIDER_MODULE = u'topmanagerbot.spiders'

IMAGES_STORE = u'%s/media' % DJANGO_PROJECT_PATH

ITEM_PIPELINES = {
    u'topmanagerbot.pipelines.DuplicatesPipeline': 100,
    u'topmanagerbot.pipelines.SaveImagesPipeline': 200,
    u'topmanagerbot.pipelines.ProcessPipeline': 500,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = u'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0'
########## END CRAWLER CONFIGURATION
