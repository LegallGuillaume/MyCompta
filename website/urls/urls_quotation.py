from flask import Blueprint
from models.quotation.quotation import Quotation, QuotationDAO, QuotationItem, QuotationItemDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, make_response, session
import datetime
import re
import logging
from flask_babel import Babel, lazy_gettext as _

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

manager_quotation = Blueprint("quotation", __name__)

def add_quotation(form):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        logging.warning('(Quotation) Session closed: ' + profileSession.id)
        flash(_("Impossible to add Quotation, Your session has been expired"), 'danger')
        return

    ddao = QuotationDAO()
    n_quotation = form['quotation']

    if ddao.exist(ddao.where('number', n_quotation)):
        logging.info('quotation exist with number: ' + n_quotation)
        flash(_("Impossible to add Quotation, the number of quotation is ever used"), 'danger')
        return

    client = form['client']
    date_sent = form['date_sent']
    date_validity = form['date_validity']
    tax = (form['tax'] == "true")
    lines = [(x.replace('lines[','').replace('][', '-').replace(']',''), dict(form)[x]) for x in dict(form) if x.startswith('lines[')]
    list_text = [dict(form)[x] for x in dict(form) if x.startswith('text_end[')]
    quotation_obj = Quotation()
    quotation_obj.client = client
    quotation_obj.date_sent = date_sent
    quotation_obj.date_validity = date_validity
    quotation_obj.number = n_quotation
    quotation_obj.tax_price = 0
    quotation_obj.id_profile = id_profile
    quotation_obj.end_text = '\n'.join(list_text)

    didao = QuotationItemDAO()
    success = True
    nb_items = int(len(lines) / 3)
    list_quotation_item = list()
    for i in range(0,nb_items):
        quotationItem = QuotationItem()
        quotationItem.description = lines[(i*3)+0][1]
        quotationItem.quantity_text = lines[(i*3)+1][1]
        result = re.findall(r'[-+]?\d*\.\d+|^\d+', quotationItem.quantity_text)
        if len(result) == 0:
            result = [0]
        quotationItem.quantity = float(result[0])
        uprice = lines[(i*3)+2][1]
        if not uprice:
            uprice = 0
        quotationItem.unit_price = float(uprice)
        quotationItem.reduction = False
        list_quotation_item.append(quotationItem)
        quotation_obj.total += (quotationItem.quantity*quotationItem.unit_price)
        if tax:
            quotation_obj.tax_price += ((quotationItem.quantity*quotationItem.unit_price)*20/100)

    if not ddao.insert(quotation_obj):
        logging.info('add quotation %s FAILED' + n_quotation)
        flash(_("Impossible to add quotation n°%1").replace('%1', n_quotation), 'danger')
        return
    else:
        logging.info('add quotation %s OK' + n_quotation)
    
    for quotationItem in list_quotation_item:
        quotationItem.id_quotation = quotation_obj.id
        success &= didao.insert(quotationItem)

    if not success:
        logging.warning('add quotation item %s FAILED' + n_quotation)
        didao.delete(didao.where('id_quotation', n_quotation))  
        ddao.delete(ddao.where('id', n_quotation))   
        flash(_("Impossible to add quotation n°%1").replace('%1', n_quotation), 'danger')
    else:
        logging.info('add quotation item %s OK' + n_quotation)
        flash(_("The quotation n°%1 has been added successfull").replace('%1', n_quotation), 'success')

def remove_quotation(n_quotation):
    ddao = QuotationDAO()
    didao = QuotationItemDAO()
    if didao.delete(didao.where('id_quotation', n_quotation)): 
        ddao.delete(ddao.where('number', n_quotation))
        flash(_("The quotation n°%1 has been deleted successfull").replace('%1', n_quotation), 'success')
        logging.info('remove quotation %s OK' + n_quotation)
    else:
        flash(_('Error while suppression of quotation n°%1 !').replace('%1', n_quotation), 'danger')
        logging.info('remove quotation %s FAILED' + n_quotation)

def convert_date(date):
    if not date:
        return _('None')
    date = date.replace('-', '/')
    l_month = ['', _('Jan.'), _('Feb.'), _('Mar'), _('Apr.'), _('May'), _('Juin'), _('Jul.'), _('Agu.'), _('Sep.'), _('Oct.'), _('Nov.'), _('Dec.')]
    l_date = date.split('/')
    month = l_date[1]
    return '{} {} {}'.format(l_date[2], l_month[int(month)], l_date[0])

@manager_quotation.route('/quotation')
def quotation():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    ddao = QuotationDAO()
    l_quotation = ddao.get(ddao.where('id_profile', profile.id))
    logging.info('go url /quotation')
    last_quotation = l_quotation[-1].number if l_quotation else ''

    return render_template(
        'quotation.html', convert_date=convert_date, 
        Page_title=_('Quotation'), quotation=reversed(l_quotation), last_quotation=last_quotation,
        profile=profile, len=len, color=Color
    )

@manager_quotation.route('/quotation/<number>')
def quotation_id(number = None):
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('go url /quotation/%s', number)
    profile = get_profile_from_session()
    ddao = QuotationDAO()
    if not ddao.exist(ddao.where('number', number)):
        logging.info('redirect if quotation doesnt exist number: %s' + number)
        return redirect('/quotation')
    quotation = ddao.get(ddao.where('number', number))[0]
    logging.info('display pdf_template_quotation.html with quotation number: ' + number)
    return render_template('template/pdf_template_quotation.html', profile=profile, convert_date=convert_date, quotation=quotation)

@manager_quotation.route('/quotation-delete', methods=['POST'])
def quotation_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /quotation-delete %s', request.form['quotation-id'])
    remove_quotation(request.form['quotation-id'])
    return redirect('/quotation')

@manager_quotation.route('/quotation-add', methods=['POST'])
def quotation_add():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /quotation-add')
    if request.method == 'POST':
        add_quotation(request.form)
    return redirect('/quotation')
