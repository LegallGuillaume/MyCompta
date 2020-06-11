from flask import Blueprint
from models.client import Client, ClientDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, session
import logging

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

manager_client = Blueprint("client", __name__)

def get_client_name(id_client):
    cdao = ClientDAO()
    return cdao.field(cdao.where('id', id_client), 'name')[0][0]

def add_client(form):
    profileSession = get_profile_from_session()
    client = Client()
    client.name = form['client-name']
    client.adresse = form['client-adresse']
    client.comp_adresse = form['client-comp']
    client.cp = form['client-cp']
    client.ville = form['client-ville']
    client.pays = form['client-pays']
    client.id_profile = profileSession.id
    cdao = ClientDAO()
    if cdao.insert(client):
        logging.info('add client %s OK', client.name)
        flash('Le client {} a été ajoutée avec succès !'.format(client.name), 'success')
    else:
        logging.warning('add client %s Failed', client.name)
        flash("Erreur lors de la création du client {} !".format(client.name), 'danger')

def remove_client(clientname):
    cdao = ClientDAO()
    if cdao.delete(cdao.where('name', clientname)):
        logging.info('remove client %s OK', clientname)
        flash('La facture {} a été supprimée avec succès !'.format(clientname), 'success')
    else:
        logging.warning('remove client %s Failed', clientname)
        flash("Erreur lors de la suppression de la facture {} !".format(clientname), 'danger')

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
        return render_template('client.html', Page_title='Clients', clients=reversed(l_clients),
                                profile=profile, color=Color)
    elif request.method == 'POST':
        add_client(request.form)
        return ''
    else:
        return redirect('/home')

@manager_client.route('/client-delete', methods=['POST'])
def cl_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /client-delete')
    remove_client(request.form['client-name'])
    return redirect('/clients')