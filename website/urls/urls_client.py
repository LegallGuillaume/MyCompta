from flask import Blueprint
from models.client import Client, ClientDAO
from settings.tools import get_profile_from_session
import logging
from flask_babel import Babel, lazy_gettext as _

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

def get_client_name(id_client):
    cdao = ClientDAO()
    list_all_name = cdao.field(cdao.where('id', id_client), 'name')
    if list_all_name:
        return list_all_name[0][0]
    return _('client_deleted')

def add_client(form):
    profileSession = get_profile_from_session()
    client = Client()
    client.name = form['client_name']
    client.address = form['client_address']
    client.comp_address = form['client_comp']
    client.zipcode = form['client_zipcode']
    client.city = form['client_city']
    client.country = form['client_country']
    client.id_profile = profileSession.id
    cdao = ClientDAO()
    if cdao.insert(client):
        logging.info('add client %s OK', client.name)
        return 1, client
    else:
        logging.warning('add client %s Failed', client.name)
        return 2, None

def remove_client(clientname):
    cdao = ClientDAO()
    if cdao.delete(cdao.where('name', clientname)):
        logging.info('remove client %s OK', clientname)
        return 1
    else:
        logging.warning('remove client %s Failed', clientname)
        return 2

def get_list_client(id_profile):
    cdao = ClientDAO()
    return cdao.get(cdao.where('id_profile', id_profile))
