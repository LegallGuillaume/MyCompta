from flask import Blueprint
from models.insurance import Insurance, InsuranceDAO
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

manager_insurance = Blueprint("insurance", __name__)

def add_insurance(form):
    profile=get_profile_from_session()
    insurance = Insurance()
    insurance.name = form['insurance-name']
    insurance.type = form['insurance-type']
    insurance.region = form['insurance-region']
    insurance.n_contract = form['insurance-contract']
    insurance.sel = False
    insurance.id_profile = profile.id
    adao = InsuranceDAO()
    if adao.insert(insurance):
        logging.info('add insurance %s OK', insurance.name)
        flash(_("The insurance %1 has been added successfull").replace('%1', insurance.name), 'success')
    else:
        logging.warning('add insurance %s OK', insurance.name)
        flash(_('Error while creation of insurance %1 !').replace('%1', insurance.name), 'danger') 

def remove_insurance(insurancename):
    adao = InsuranceDAO()
    if adao.delete(adao.where('name', insurancename)):
        logging.info('remove insurance %s FAILED', insurancename)
        flash(_("The insurance %1 has been deleted successfull").replace('%1', insurancename), 'success')
    else:
        logging.info('remove insurance %s FAILED', insurancename)
        flash(_('Error while supression of insurance %1 !').replace('%1', insurancename), 'danger') 

def select_insurance(insurancename, select):
    adao = InsuranceDAO()
    profile=get_profile_from_session()
    assu = adao.get([adao.where('name', insurancename), adao.where('id_profile', profile.id)])[0]
    assu.sel = select
    ret = adao.update(assu)
    if ret:
        logging.info('insurance %s %s OK', str(select), insurancename)
    else:
        logging.info('insurance %s %s OK', str(select), insurancename)

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
        l_insurances = get_list_insurance(profile.id)
        return render_template('insurance.html', Page_title=_('Insurances'), insurances=reversed(l_insurances),
                                profile=profile, color=Color, url="insurance")
    elif request.method == 'POST':
        logging.debug('add insurance form : %s', str(request.form))
        add_insurance(request.form)
        return ''
    else:
        return redirect('/home')

@manager_insurance.route('/insurance-delete', methods=['POST'])
def as_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.debug('delete insurance form : %s', str(request.form))
    logging.info('receive socket from /insurance-delete')
    remove_insurance(request.form['insurance-name'])
    return redirect('/insurance')

@manager_insurance.route('/insurance-select', methods=['POST'])
def as_select():
    if not session.get('logged_in'):
        return redirect('/')
    logging.debug('sel insurance form : %s', str(request.form))
    logging.info('receive socket from /insurance-select')
    select_insurance(request.form['insurance-name'], request.form['insurance-select'])
    return redirect('/insurance')