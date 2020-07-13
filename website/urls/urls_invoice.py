from models.invoice import InvoiceDAO, Invoice
from urls.urls_client import get_list_client, ClientDAO, Client, get_client_name
from urls.urls_insurance import InsuranceDAO, Insurance
from settings.config import TAX
from settings.tools import get_profile_from_session, CACHE_INVOICE
import pdfkit
import datetime
import logging
from flask_babel import Babel, lazy_gettext as _
from flask import render_template, make_response, redirect

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

def add_invoice(form):
    cdao = ClientDAO()
    client = cdao.get(cdao.where('name', form['invoice_client'].split(' -- ')[0]))
    if not client:
        logging.warning('(Invoice) This client doesnt exist: ' + form['invoice_client'])
        return 1, None
    client = client[0]
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        logging.warning('(Invoice) Session closed: ' + profileSession.id)
        return 2, None
    invoice = Invoice()
    invoice.name = form['invoice_name']
    invoice.project = form['invoice_project']
    invoice.day_rate = float(form['invoice_day_rate'])
    invoice.days = int(form['invoice_days'])
    invoice.date_sent = '/'.join(reversed(form['invoice_datesent'].split('-')))
    invoice.date_expiry = '/'.join(reversed(form['invoice_dateexpiry'].split('-')))
    invoice.max_delay = '/'.join(reversed(form['invoice_delay'].split('-')))
    invoice.tax = form['invoice_tax'] == 'True'
    invoice.total = (invoice.day_rate * invoice.days)
    invoice.id_client = client.id
    invoice.id_profile = id_profile
    fdao = InvoiceDAO()

    if fdao.insert(invoice):
        logging.info('add invoice %s OK', invoice.name)
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
        return 3, invoice
    else:
        logging.info('add invoice %s FAILED', invoice.name)
        return 4, None

def remove_invoice(invoicename):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        logging.warning('(Invoice) Session closed: ' + profileSession.id)
        return 1
    fdao = InvoiceDAO()
    if fdao.delete(fdao.where('name', invoicename)):
        logging.info('remove invoice %s OK', invoicename)
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
        return 2
    else:
        logging.info('remove invoice %s Failed', invoicename)
        return 3

def bill(invoicename, is_sold):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        logging.warning('(Invoice) Session closed: ' + profileSession.id)
        return 1
    fdao = InvoiceDAO()
    invo = fdao.get(fdao.where('name', invoicename))[0]
    invo.sold = is_sold
    if hasattr(invo, 'total_tax'):
        del invo.total_tax
    if fdao.update(invo):
        logging.info('bill invoice sold %s %s OK', is_sold, invoicename)
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
        return 2
    else:
        logging.info('bill invoice sold %s %s FAILED', is_sold, invoicename)
        return 3

def get_list_invoice(id_profile):
    fdao = InvoiceDAO()
    l_invoices = fdao.get(fdao.where('id_profile', id_profile))
    sold_en = 0
    last_i = ''
    waiting_i = 0
    for invoice in l_invoices:
        if invoice.sold:
            sold_en += float(invoice.total)
        else:
            waiting_i += float(invoice.total)
        if invoice.tax:
            invoice.total_tax = str(float(invoice.total)*(1+(TAX/100)))
        if last_i:
            tmp1 = invoice.date_sent.split('/')
            tmp1.reverse()
            tmp2 = last_i.split('/')
            tmp2.reverse()
            tmp_invo = int(''.join(tmp1))
            tmp_last = int(''.join(tmp2))
            if tmp_invo < tmp_last:
                continue
        last_i = invoice.date_sent
    return l_invoices, sold_en, last_i, waiting_i

def convert_date(date):
    if not date:
        return _('None')
    l_month = ['', _('Jan.'), _('Feb.'), _('Mar'), _('Apr.'), _('May'), _('Juin'), _('Jul.'), _('Agu.'), _('Sep.'), _('Oct.'), _('Nov.'), _('Dec.')]
    l_date = date.split('/')
    month = l_date[1]
    return '{} {} {}'.format(l_date[0], l_month[int(month)], l_date[2])

def get_new_invoice():
    fdao = InvoiceDAO()
    now = datetime.datetime.now()
    year = now.year
    profile = get_profile_from_session()
    l_invs = fdao.get(fdao.where('id_profile', profile.id))
    last_i = ''
    for invoice in l_invs:
        if last_i:
            tmp_invo = int(''.join(invoice.name.split('-')))
            tmp_last = int(''.join(last_i.split('-')))
            if tmp_invo < tmp_last:
                continue
        last_i = invoice.name
    if last_i:
        last_i.split('-')[0]
        if year == int(last_i.split('-')[0]):
            nb = last_i.split('-')[1]
            nb = int(nb) + 1
            return '{}-{:04d}'.format(str(year), nb)
    logging.info('new invoice name: %s', '{}-0001'.format(year))
    return '{}-0001'.format(year)

def pdf_file(invoname, download):
    if not invoname:
        return redirect('/home')
    fdao = InvoiceDAO()
    if not fdao.exist(fdao.where('name', invoname)):
        return redirect('/home')
    invoice = fdao.get(fdao.where('name', invoname))[0]

    def date(dat):
        return '/'.join(reversed(dat.split('/')))

    prestamonth = '/'.join(invoice.date_sent.split('/')[1:])

    client = Client()
    cdao = ClientDAO()
    client = cdao.get(cdao.where('id', invoice.id_client))[0]

    total = float(invoice.total)
    if invoice.tax:
        total *= (1+(TAX/100))

    profile = get_profile_from_session()

    adao = InsuranceDAO()
    insurance = adao.get([adao.where('id_profile', profile.id), adao.where('sel', 'True')])

    html_render = render_template(
        'template/pdf_template.html', profile=profile, 
        prestamonth=prestamonth, date=date, invoice=invoice, 
        convert_date=convert_date, Page_title='Facture',
        client=client, total=total, insurance=insurance, len=len, url="invoice"
    )

    pdf = pdfkit.from_string(html_render, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    if download:
        response.headers['Content-Disposition'] = 'attachment; filename={}_{}.pdf'.format(_('Invoice'), invoname)
    else:
        response.headers['Content-Disposition'] = 'inline; filename={}_{}.pdf'.format(_('Invoice'), invoname)
    logging.info('Invoice create pdf download: %s', str(download))
    return response
