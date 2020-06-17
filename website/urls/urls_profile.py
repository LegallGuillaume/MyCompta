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
    logging.debug('add profile form : %s', str(request.form))
    logging.info('receive socket from /register-data -> profile: %s', request.form['profile-name'])
    form = request.form
    profile = Profile()
    profile.name = form['profile-name']
    profile.firstname = form['profile-firstname']
    profile.address = form['profile-address']
    profile.comp_address = form['profile-comp_address']
    profile.city = form['profile-city']
    profile.zipcode = form['profile-zipcode']
    profile.country = form['profile-country']
    profile.phone = form['profile-phone']
    profile.email = form['profile-email']
    profile.siret = form['profile-siret']
    pdao = ProfileDAO()
    if pdao.insert(profile):
        logging.info('add profile %s OK', profile.name)
        session['logged_in'] = pdao.field(pdao.where('email', profile.email), 'id')[0][0]
    else:
        logging.info('add profile %s FAILED', profile.name)
    return redirect('/')
