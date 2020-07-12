from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from models.invoice import Invoice, InvoiceDAO
from models.profile import Profile, ProfileDAO
from models.color import Color
from settings.tools import get_profile_from_session, CACHE_INVOICE
from urls.urls_invoice import get_list_invoice, convert_date, get_new_invoice, pdf_file
from urls.urls_client import get_client_name, get_list_client, ClientDAO
from urls.urls_insurance import get_list_insurance
from urls.socketio import app as Flask_app, socketio, babel as Flask_babel
from settings.config import TAX


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

@Flask_app.route('/', methods=['GET', 'POST'])
def login():
    logging.warning('URL / send with ' + request.method)
    if request.method == 'POST':
        email = str(request.form['user-name'])
        pwd = str(request.form['user-password'])
        pdao = ProfileDAO()
        if pdao.check_auth(pdao.where('email', email), pwd):
            session['logged_in'] = str(pdao.get(pdao.where('email', email))[0].id)
    if not session.get('logged_in'):
        logging.warning('display login.html')
        return render_template('v3-login.html')
    else:
        logging.warning('redirect to URL /home')
        return redirect('/home')

@Flask_app.route('/logout')
def logout():
    logging.warning('URL /logout')
    id = session['logged_in']
    del session['logged_in']
    logging.warning('deconnection user id=' + str(id))
    return redirect('/')

@Flask_app.route('/home')
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

    logging.warning('display v3-home.html')

    list_client = get_list_client(profile.id)
    list_client.reverse()

    list_insurance = get_list_insurance(profile.id)
    list_insurance.reverse()

    l_invoice.reverse()

    return render_template(
        'v3-home.html', convert_date=convert_date,
        Page_title=_('Home'), invoices=l_invoice, new_invoice=get_new_invoice(),
        sold_collected=sold_collected, last_invoice=last_i, insurances=list_insurance,
        solde_no_sold=waiting_i, year=year, clients=list_client, get_client_name=get_client_name,
        profile=profile, tax_total=tax_total, tax_collected=tax_collected,
        invoices_available=invo_avail, color=Color, year_1=(year-1),
        inv_collect_last_year=tax_collected_last_year, url="home"
    )

if __name__ == "__main__":
    DEBUG = False
    logging.basicConfig(
        filename='server.log',filemode='w', 
        format='%(asctime)s >> %(levelname)s >> %(message)s', datefmt='%d/%m/%Y %I:%M:%S',
        level=logging.DEBUG if DEBUG else logging.INFO
    )
    pdao = ProfileDAO()
    for profile in pdao.get_list_profile():
        id = pdao.get_profile_id(pdao.where('siret', profile.siret))
        logging.debug('profile checked : id=' + str(id))
        get_element_profile_invoice(id)
    socketio.run(Flask_app, host='0.0.0.0', port=5000, debug=DEBUG)