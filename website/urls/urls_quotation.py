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

manager_quotation = Blueprint("devis", __name__)

def add_quotation(form):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        logging.warning('(Quotation) Session closed: ' + profileSession.id)
        flash(_("Impossible to add Quotation, Your session has been expired"), 'danger')
        return

    ddao = QuotationDAO()
    n_devis = form['devis']

    if ddao.exist(ddao.where('numero', n_devis)):
        logging.info('quotation exist with numero: ' + n_devis)
        flash(_("Impossible to add Quotation, the number of quotation is ever used"), 'danger')
        return

    client = form['client']
    date_envoi = form['date_envoi']
    date_validite = form['date_validite']
    tva = (form['tva'] == "true")
    lines = [(x.replace('lines[','').replace('][', '-').replace(']',''), dict(form)[x]) for x in dict(form) if x.startswith('lines[')]
    list_text = [dict(form)[x] for x in dict(form) if x.startswith('text_end[')]
    devis_obj = Quotation()
    devis_obj.client = client
    devis_obj.date_envoi = date_envoi
    devis_obj.date_validite = date_validite
    devis_obj.numero = n_devis
    devis_obj.tva_price = 0
    devis_obj.id_profile = id_profile
    devis_obj.end_text = '\n'.join(list_text)

    didao = QuotationItemDAO()
    success = True
    nb_items = int(len(lines) / 3)
    list_devis_item = list()
    for i in range(0,nb_items):
        devisItem = QuotationItem()
        devisItem.description = lines[(i*3)+0][1]
        devisItem.quantity_text = lines[(i*3)+1][1]
        result = re.findall(r'[-+]?\d*\.\d+|^\d+', devisItem.quantity_text)
        if len(result) == 0:
            result = [0]
        devisItem.quantity = float(result[0])
        uprice = lines[(i*3)+2][1]
        if not uprice:
            uprice = 0
        devisItem.unit_price = float(uprice)
        devisItem.reduction = False
        list_devis_item.append(devisItem)
        devis_obj.total += (devisItem.quantity*devisItem.unit_price)
        if tva:
            devis_obj.tva_price += ((devisItem.quantity*devisItem.unit_price)*20/100)

    if not ddao.insert(devis_obj):
        logging.info('add quotation %s FAILED' + n_devis)
        flash(_("Impossible to add quotation n°%1").replace('%1', n_devis), 'danger')
        return
    else:
        logging.info('add quotation %s OK' + n_devis)
    
    for devisItem in list_devis_item:
        devisItem.id_devis = devis_obj.id
        success &= didao.insert(devisItem)

    if not success:
        logging.warning('add quotation item %s FAILED' + n_devis)
        didao.delete(didao.where('id_devis', n_devis))  
        ddao.delete(ddao.where('id', n_devis))   
        flash(_("Impossible to add quotation n°%1").replace('%1', n_devis), 'danger')
    else:
        logging.info('add quotation item %s OK' + n_devis)
        flash(_("The quotation n°%1 has been added successfull").replace('%1', n_devis), 'success')

def remove_quotation(n_devis):
    ddao = QuotationDAO()
    didao = QuotationItemDAO()
    if didao.delete(didao.where('id_devis', n_devis)): 
        ddao.delete(ddao.where('numero', n_devis))
        flash(_("The quotation n°%1 has been deleted successfull").replace('%1', n_devis), 'success')
        logging.info('remove quotation %s OK' + n_devis)
    else:
        flash(_('Error while suppression of quotation n°%1 !').replace('%1', n_devis), 'danger')
        logging.info('remove quotation %s FAILED' + n_devis)

def convert_date(date):
    if not date:
        return 'Aucune'
    date = date.replace('-', '/')
    l_mois = ['', _('Jan.'), _('Feb.'), _('Mar'), _('Apr.'), _('May'), _('Juin'), _('Jul.'), _('Agu.'), _('Sep.'), _('Oct.'), _('Nov.'), _('Dec.')]
    l_date = date.split('/')
    month = l_date[1]
    return '{} {} {}'.format(l_date[2], l_mois[int(month)], l_date[0])

@manager_quotation.route('/quotation')
def devis():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    ddao = QuotationDAO()
    l_devis = ddao.get(ddao.where('id_profile', profile.id))
    logging.info('go url /quotation')
    last_devis = l_devis[-1].numero if l_devis else ''

    return render_template(
        'quotation.html', convert_date=convert_date, 
        Page_title=_('Quotation'), devis=reversed(l_devis), last_devis=last_devis,
        profile=profile, len=len, color=Color
    )

@manager_quotation.route('/quotation/<numero>')
def devis_id(numero = None):
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('go url /quotation/%s', numero)
    profile = get_profile_from_session()
    ddao = QuotationDAO()
    if not ddao.exist(ddao.where('numero', numero)):
        logging.info('redirect if quotation doesnt exist numero: %s' + numero)
        return redirect('/quotation')
    devis = ddao.get(ddao.where('numero', numero))[0]
    logging.info('display pdf_template_quotation.html with quotation numero: ' + numero)
    return render_template('template/pdf_template_quotation.html', profile=profile, convert_date=convert_date, devis=devis)

@manager_quotation.route('/quotation-delete', methods=['POST'])
def devis_del():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /quotation-delete %s', request.form['devis-id'])
    remove_quotation(request.form['devis-id'])
    return redirect('/quotation')

@manager_quotation.route('/quotation-add', methods=['POST'])
def devis_add():
    if not session.get('logged_in'):
        return redirect('/')
    logging.info('receive socket from /quotation-add')
    if request.method == 'POST':
        add_quotation(request.form)
    return redirect('/quotation')
