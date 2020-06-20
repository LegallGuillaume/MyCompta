from flask import Blueprint
from models.client import Client, ClientDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, session
import logging
from flask_babel import Babel, lazy_gettext as _

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

manager_client = Blueprint("client", __name__)

def get_client_name(id_client):
    cdao = ClientDAO()
    list_all_name = cdao.field(cdao.where('id', id_client), 'name')
    if list_all_name:
        return list_all_name[0][0]
    return _('client_deleted')

def add_client(form):
    profileSession = get_profile_from_session()
    client = Client()
    client.name = form['client-name']
    client.address = form['client-address']
    client.comp_address = form['client-comp']
    client.zipcode = form['client-zipcode']
    client.city = form['client-city']
    client.country = form['client-country']
    client.id_profile = profileSession.id
    cdao = ClientDAO()
    if cdao.insert(client):
        logging.info('add client %s OK', client.name)
        flash(_('The client %1 has been added successfull').replace('%1', client.name), 'success')
    else:
        logging.warning('add client %s Failed', client.name)
        flash(_('Error while creation of client %1 !').replace('%1', client.name), 'danger') 

def remove_client(clientname):
    cdao = ClientDAO()
    if cdao.delete(cdao.where('name', clientname)):
        logging.info('remove client %s OK', clientname)
        flash(_('The client %1 has been deleted!').replace('%1', clientname), 'success') 
    else:
        logging.warning('remove client %s Failed', clientname)
        flash(_('Error while supression of client %1 !').replace('%1', clientname), 'danger') 

def get_list_client(id_profile):
    cdao = ClientDAO()
    return cdao.get(cdao.where('id_profile', id_profile))

@manager_client.route('/clients', methods=['GET', 'POST'])
def cl():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('go url /clients with ' + request.method)
    if request.method == 'GET':
        profile=get_profile_from_session()
        l_clients = get_list_client(profile.id)
        return render_template('client.html', Page_title=_('Clients'), clients=reversed(l_clients),
                                profile=profile, color=Color, url="client")
    elif request.method == 'POST':
        logging.debug('add client form : %s', str(request.form))
        add_client(request.form)
        return redirect('/clients')
    else:
        return redirect('/home')

@manager_client.route('/client-delete', methods=['POST'])
def cl_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /client-delete')
    logging.debug('delete client form : %s', str(request.form))
    remove_client(request.form['client-name'])
    return redirect('/clients')