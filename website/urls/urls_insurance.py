from flask import Blueprint
from models.insurance import Insurance, InsuranceDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, session
import logging
from flask_babel import Babel, lazy_gettext as _

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

manager_insurance = Blueprint("insurance", __name__)

def add_insurance(form):
    profile=get_profile_from_session()
    insurance = Insurance()
    insurance.name = form['assurance-name']
    insurance.type = form['assurance-type']
    insurance.region = form['assurance-region']
    insurance.n_contrat = form['assurance-contrat']
    insurance.sel = False
    insurance.id_profile = profile.id
    adao = InsuranceDAO()
    if adao.insert(insurance):
        logging.info('add insurance %s OK', insurance.name)
        flash(_("The insurance %1 has been added successfull").replace('%1', insurance.name), 'success')
    else:
        logging.warning('add insurance %s OK', insurance.name)
        flash(_('Error while creation of insurance %1 !').replace('%1', insurance.name), 'danger') 

def remove_insurance(assurancename):
    adao = InsuranceDAO()
    if adao.delete(adao.where('name', assurancename)):
        logging.info('remove insurance %s FAILED', assurancename)
        flash(_("The insurance %1 has been deleted successfull").replace('%1', assurancename), 'success')
    else:
        logging.info('remove insurance %s FAILED', assurancename)
        flash(_('Error while supression of insurance %1 !').replace('%1', assurancename), 'danger') 

def select_insurance(assurancename, select):
    adao = InsuranceDAO()
    profile=get_profile_from_session()
    assu = adao.get([adao.where('name', assurancename), adao.where('id_profile', profile.id)])[0]
    assu.sel = select
    ret = adao.update(assu)
    if ret:
        logging.info('insurance %s %s OK', str(select), assurancename)
    else:
        logging.info('insurance %s %s OK', str(select), assurancename)

def get_list_insurance(id_profile):
    adao = InsuranceDAO()
    return adao.get(adao.where('id_profile', id_profile))

@manager_insurance.route('/insurance', methods=['GET', 'POST'])
def as_():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('go url /insurance with ' + request.method)
    if request.method == 'GET':
        profile=get_profile_from_session()
        l_assurances = get_list_insurance(profile.id)
        return render_template('insurance.html', Page_title=_('Insurances'), assurances=reversed(l_assurances),
                                profile=profile, color=Color)
    elif request.method == 'POST':
        add_insurance(request.form)
        return ''
    else:
        return redirect('/home')

@manager_insurance.route('/insurance-delete', methods=['POST'])
def as_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /insurance-delete')
    remove_insurance(request.form['assurance-name'])
    return redirect('/insurance')

@manager_insurance.route('/insurance-select', methods=['POST'])
def as_select():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /insurance-select')
    select_insurance(request.form['assurance-name'], request.form['assurance-select'])
    return redirect('/insurance')