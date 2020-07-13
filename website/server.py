from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from models.invoice import Invoice, InvoiceDAO
from models.profile import Profile, ProfileDAO
from models.enterprise import Enterprise, EnterpriseDAO
from days.days import nb_day_between_date
from settings.tools import get_profile_from_session, CACHE_INVOICE
from urls.urls_invoice import get_list_invoice, convert_date, get_new_invoice, pdf_file
from urls.urls_client import get_client_name, get_list_client, ClientDAO
from urls.urls_insurance import get_list_insurance
from urls.socketio import app as Flask_app, socketio, babel as Flask_babel, emit_result, MESSAGE_TYPE
from settings.config import TAX

import os
import datetime
import logging
from flask_babel import lazy_gettext as _

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

LANGUAGES = {
    'en': 'English',
    'fr': 'Français'
}

@Flask_babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

def get_element_profile_invoice(id):
    if not CACHE_INVOICE or id not in CACHE_INVOICE.keys():
        l_invoice, sold_collected, last_i, waiting_i = get_list_invoice(id)
        dic = {
            'l_invoice': l_invoice,
            'sold_collected': sold_collected,
            'last_i': last_i,
            'waiting_i': waiting_i,
        }
        CACHE_INVOICE[id] = dic
    return CACHE_INVOICE[id]

@Flask_app.route('/pdf/<invoname>')
def invoice_pdf(invoname = None):
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('go url /pdf/%s ' + invoname)
    return pdf_file(invoname, False)

@Flask_app.route('/', methods=['GET'])
def login():
    logging.warning('URL /login')
    if not session.get('logged_in'):
        return render_template('v3-login.html')
    else:
        return redirect('/home')

@Flask_app.route('/register-data', methods=['POST'])
def register():
    logging.debug('add profile form : %s', str(request.form))
    logging.info('receive socket from /register-data -> profile: %s', request.form['profile-name'])
    form = request.form
    if form['profile-password'] != form['profile-repassword']:
        return render_template('v3-login.html', error=_('Your confirmation password does not match the password you entered'))
    profile = Profile()
    profile.name = form['profile-name']
    profile.firstname = form['profile-firstname']
    profile.email = form['profile-email']
    profile.password = form['profile-password']
    pdao = ProfileDAO()
    if pdao.insert(profile):
        logging.info('add profile %s OK', profile.name)
        session.permanent = True
        session['logged_in'] = pdao.field(pdao.where('email', profile.email), 'id')[0][0]
    else:
        logging.info('add profile %s FAILED', profile.name)
        return render_template('v3-login.html', error=_('Impossible to create new user, please contact an admin !'))

    return redirect('/')

@Flask_app.route('/signin', methods=['POST'])
def signin_form():
    email = request.form['email']
    passwd = request.form['password']
    pdao = ProfileDAO()
    if pdao.check_auth(pdao.where('email', email), passwd):
        session.permanent = True
        session['logged_in'] = str(pdao.get(pdao.where('email', email))[0].id)
        logging.warning('sign in OK, redirect to URL /home')
        return redirect('/home')
    else:
        logging.warning('sign in Failed, send message to /')
        return render_template('v3-login.html', error=_('Email or Password incorrect !'))

@Flask_app.route('/logout', methods=['GET'])
def logout():
    logging.warning('URL /logout')
    id = session['logged_in']
    del session['logged_in']
    logging.warning('deconnection user id=' + str(id))
    return redirect('/')

@Flask_app.route('/home', methods=['GET'])
def accueil():
    logging.warning('URL /home')
    if not session.get('logged_in'):
        logging.warning('redirect /, no session enable')
        return redirect('/')
    profile = get_profile_from_session()
    if not profile:
        logging.warning('redirect /, no session enable')
        del session['logged_in']
        return redirect('/')
    dic_profile = get_element_profile_invoice(profile.id)
    l_invoice = dic_profile['l_invoice']
    sold_collected = dic_profile['sold_collected']
    last_i = dic_profile['last_i']
    waiting_i = dic_profile['waiting_i']
    now = datetime.datetime.now()
    year = now.year
    tax_total = 0
    tax_collected = 0
    invo_avail = 72000
    tax_collected_last_year = 0
    for invo in l_invoice:
        if invo.date_expiry.split('/')[2] == str(year):
            if invo.tax:
                invo_avail -= (float(invo.total)*(1+(TAX/100)))
                if invo.sold:
                    tax_collected += (float(invo.total)*(1+(TAX/100)))
            else:
                invo_avail -= float(invo.total)
                if invo.sold:
                    tax_collected += float(invo.total)
        elif invo.date_expiry.split('/')[2] == str(year-1):
            if invo.sold:
                if invo.tax:
                    tax_collected_last_year += (float(invo.total)*(1+(TAX/100)))
                else:
                    tax_collected_last_year += float(invo.total)
        if invo.sold:
            if invo.tax:
                tax_total += (float(invo.total)*0.20)

    date_now = now.date()
    cp_date_now = date_now
    cp_date_now=date_now.replace(day=31, month=12)
    days_left = nb_day_between_date(date_now, cp_date_now)

    logging.warning('display v3-home.html')

    list_client = get_list_client(profile.id)
    list_client.reverse()

    list_insurance = get_list_insurance(profile.id)
    list_insurance.reverse()

    l_invoice.reverse()

    return render_template(
        'v3-home.html', convert_date=convert_date, days_left=days_left,
        Page_title=_('Home'), invoices=l_invoice, new_invoice=get_new_invoice(),
        sold_collected=sold_collected, last_invoice=last_i, insurances=list_insurance,
        solde_no_sold=waiting_i, year=year, clients=list_client, get_client_name=get_client_name,
        profile=profile, tax_total=tax_total, tax_collected=tax_collected,
        invoices_available=invo_avail, year_1=(year-1),
        inv_collect_last_year=tax_collected_last_year, url="home"
    )

@Flask_app.route('/enterprise', methods=['GET', 'POST'])
def enterprise():
    profile = get_profile_from_session()
    if request.method == 'GET':
        logging.warning('URL /enterprise')
        if not session.get('logged_in'):
            logging.warning('redirect /, no session enable')
            return redirect('/')
        edao = EnterpriseDAO()
        list_enterprise = edao.get(edao.where('id_profile', profile.id))
        if not list_enterprise:
            enterprise = Enterprise()
        else:
            enterprise = list_enterprise[0]
        return render_template('v3-enterprise.html', profile=profile, enterprise=enterprise)
    elif request.method == 'POST':
        logging.debug('add enterprise form : %s', str(request.form))
        logging.info('receive socket from /enterprise -> enterprise: %s', request.form['enterprise-name'])
        form = request.form
        enterprise = Enterprise()
        enterprise.id_profile = profile.id
        enterprise.name = form['enterprise-name']
        enterprise.slogan = form['enterprise-slogan']
        enterprise.address = form['enterprise-address']
        enterprise.comp_address = form['enterprise-comp_address']
        enterprise.city = form['enterprise-city']
        enterprise.zipcode = form['enterprise-zipcode']
        enterprise.country = form['enterprise-country']
        enterprise.email = form['enterprise-email']
        enterprise.phone = form['enterprise-phone']
        edao = EnterpriseDAO()
        if edao.exist(edao.where('id_profile', enterprise.id_profile)):
            if not edao.update(enterprise, edao.where('id_profile', enterprise.id_profile)):
                logging.info('update enterprise %s FAILED', enterprise.name)
                return render_template('v3-enterprise.html', enterprise=enterprise, profile=profile, error=_('Impossible to update enterprise, please contact an admin !'))
            logging.info('update enterprise %s OK', enterprise.name)
        else:
            enterprise.siret = form['enterprise-siret'].replace(' ','_').replace("'", "").replace('-', ' ')
            if not edao.insert(enterprise):
                logging.info('add enterprise %s FAILED', enterprise.name)
                return render_template('v3-enterprise.html', enterprise=enterprise, profile=profile, error=_('Impossible to create new enterprise, please contact an admin !'))
            logging.info('add enterprise %s OK', enterprise.name)
        return render_template('v3-enterprise.html', enterprise=enterprise, profile=profile)

@Flask_app.route('/profile', methods=['GET', 'POST'])
def profile_edit():
    logging.warning('URL /profile')
    if not session.get('logged_in'):
        logging.warning('redirect /, no session enable')
        return redirect('/')
    if request.method == 'GET':
        profile = get_profile_from_session()
        return render_template('v3-profile.html', profile=profile)
    else:
        profile_old = get_profile_from_session()
        form = request.form
        if form['profile-password'] != form['profile-repassword']:
            return render_template('v3-profile.html', profile=profile_old, error=_('Your confirmation password does not match the password you entered'))
        profile = profile_old
        if form['profile-name']:
            profile.name = form['profile-name']
        if form['profile-firstname']:
            profile.firstname = form['profile-firstname']
        if form['profile-email']:
            profile.email = form['profile-email']
        if form['profile-password']:
            profile.password = form['profile-password']
        pdao = ProfileDAO()
        id_profile = profile.id
        if pdao.update(profile, pdao.where('id', id_profile)):
            logging.info('edit profile %s OK', str(id_profile))
        else:
            logging.info('add profile %s FAILED', profile.name)
            return render_template('v3-profile.html',profile=profile_old, error=_('Impossible to edit user, please contact an admin !'))
    return redirect('/profile')

if __name__ == "__main__":
    DEBUG = False
    logging.basicConfig(
        filename='server.log',filemode='w', 
        format='%(asctime)s >> %(levelname)s >> %(message)s', datefmt='%d/%m/%Y %I:%M:%S',
        level=logging.DEBUG if DEBUG else logging.INFO
    )
    pdao = ProfileDAO()
    for profile in pdao.get_list_profile():
        id = pdao.get_profile_id(pdao.where('email', profile.email))
        logging.debug('profile checked : id=' + str(id))
        get_element_profile_invoice(id)
    socketio.run(Flask_app, host='0.0.0.0', port=5000, debug=DEBUG)