#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from .pgoapi.utilities import get_pogo_server_status

config = {
    'LOCALE': 'en',
    'LOCALES_DIR': 'static/locales',
    'ROOT_PATH': '',
    'ORIGINAL_LATITUDE': None,
    'ORIGINAL_LONGITUDE': None,
    'GMAPS_KEY': None,
    'GA_KEY': None,
    'REQ_SLEEP': 5,
    'REQ_HEAVY_SLEEP': 30,
    'REQ_MAX_FAILED': 5,
    'POGO_SERVER_STATUS':
    {
     'status': get_pogo_server_status(),
     'timestamp': datetime.utcnow()
    },
    'PASSWORD': None
}
