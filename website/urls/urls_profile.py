from flask import Blueprint
from models.profile import ProfileDAO, Profile
from flask import flash, request, render_template, redirect, make_response, session
import datetime
import logging
#register-data

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

manager_profile = Blueprint("profile", __name__)

@manager_profile.route('/register-data', methods=['POST'])
def register():
    if request.method == 'GET':
        return redirect('/')
    logging.info('receive socket from /register-data -> profile: %s', request.form['profile-name'])
    form = request.form
    profile = Profile()
    profile.name = form['profile-name']
    profile.prenom = form['profile-prenom']
    profile.adresse = form['profile-adresse']
    profile.comp_adresse = form['profile-comp_adresse']
    profile.ville = form['profile-ville']
    profile.cp = form['profile-cp']
    profile.pays = form['profile-pays']
    profile.tel = form['profile-tel']
    profile.email = form['profile-email']
    profile.siret = form['profile-siret']
    pdao = ProfileDAO()
    if pdao.insert(profile):
        logging.info('add profile %s OK', profile.name)
        session['logged_in'] = pdao.field(pdao.where('email', profile.email), 'id')[0][0]
    else:
        logging.info('add profile %s FAILED', profile.name)
    return redirect('/')
