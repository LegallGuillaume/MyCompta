import json
from flask import session
from models.profile import ProfileDAO

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

CACHE_INVOICE = dict()

def get_profile_from_session():
    st_id = session['logged_in']
    pdao = ProfileDAO()
    wh = pdao.where('id', st_id)
    if pdao.exist(wh):
        return pdao.get(wh)[0]
    return None