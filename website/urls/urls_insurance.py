from models.insurance import Insurance, InsuranceDAO
from settings.tools import get_profile_from_session
import logging
from flask_babel import Babel, lazy_gettext as _

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"


def add_insurance(form):
    profile=get_profile_from_session()
    insurance = Insurance()
    insurance.name = form['insurance_name']
    insurance.type = form['insurance_type']
    insurance.region = form['insurance_region']
    insurance.n_contract = form['insurance_contract']
    insurance.sel = False
    insurance.id_profile = profile.id
    adao = InsuranceDAO()
    if adao.insert(insurance):
        logging.info('add insurance %s OK', insurance.name)
        return 1, insurance
    else:
        logging.warning('add insurance %s OK', insurance.name)
        return 2, None

def remove_insurance(insurancename):
    adao = InsuranceDAO()
    if adao.delete(adao.where('name', insurancename)):
        logging.info('remove insurance %s FAILED', insurancename)
        return 1
    else:
        logging.info('remove insurance %s FAILED', insurancename)
        return 2

def select_insurance(insurancename, select):
    adao = InsuranceDAO()
    profile=get_profile_from_session()
    assu = adao.get([adao.where('name', insurancename), adao.where('id_profile', profile.id)])[0]
    assu.sel = select
    ret = adao.update(assu)
    if ret:
        logging.info('insurance %s %s OK', str(select), insurancename)
        return 1
    else:
        logging.info('insurance %s %s OK', str(select), insurancename)
        return 2

def get_list_insurance(id_profile):
    adao = InsuranceDAO()
    return adao.get(adao.where('id_profile', id_profile))
