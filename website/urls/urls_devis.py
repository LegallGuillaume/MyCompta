from flask import Blueprint
from models.devis.devis import Devis, DevisDAO, DevisItem, DevisItemDAO
from models.color import Color
from urls.urls_client import get_list_client, ClientDAO, Client, get_client_name
from urls.urls_assurance import AssuranceDAO, Assurance
from settings.config import TVA
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, make_response, session
import pdfkit
import datetime
import re

manager_devis = Blueprint("devis", __name__)

"""
objs = {
                devis: $('#devis-id').val(),
                client: $('#devis-client').val(),
                date_envoi: $('#devis-dateenvoi').val(),
                date_validite: $('#devis-datevalidite').val(),
                tva: $('#devis-tva').prop('checked'),
                lines: []
            }
            $('.devis-line').each(function()
            {
                obj = {}
                obj['description'] = $(this).find('textarea').val();
                obj['quantity'] = $(this).find('input:first').val();
                obj['prix'] = $(this).find('input:last').val();
                objs['lines'].push(obj)
            });
"""

def add_devis(form):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        flash("Impossible d'ajouter ce devis, car votre session a expirée", 'danger')
        return

    n_devis = form['devis']
    client = form['client']
    date_envoi = form['date_envoi']
    date_validite = form['date_validite']
    tva = (form['tva'] == "true")
    lines = [(x.replace('lines[','').replace('][', '-').replace(']',''), dict(form)[x]) for x in dict(form) if x.startswith('lines[')]
    
    devis_obj = Devis()
    devis_obj.client = client
    devis_obj.date_envoi = date_envoi
    devis_obj.date_validite = date_validite
    devis_obj.numero = n_devis
    devis_obj.tva_price = 0
    devis_obj.id_profile = id_profile

    ddao = DevisDAO()

    didao = DevisItemDAO()
    success = True
    nb_items = int(len(lines) / 3)
    list_devis_item = list()
    for i in range(0,nb_items):
        devisItem = DevisItem()
        devisItem.description = lines[(i*3)+0][1]
        result = re.findall('[-+]?\d*\.\d+|^\d+', lines[(i*3)+1][1])
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
        flash("Impossible d'ajouter le devis n°{}".format(n_devis), 'danger')
        return
    
    for devisItem in list_devis_item:
        devisItem.id_devis = devis_obj.id
        success &= didao.insert(devisItem)

    if not success:
        didao.delete(didao.where('id_devis', n_devis))  
        ddao.delete(ddao.where('id', n_devis))   
        flash("Impossible d'ajouter le devis n°{}".format(n_devis), 'danger')
    else:
        flash("Le devis n°{} a été ajouté avec succès !".format(n_devis), 'success')

def remove_devis(n_devis):
    ddao = DevisDAO()
    didao = DevisItemDAO()
    if didao.delete(didao.where('id_devis', n_devis)): 
        ddao.delete(ddao.where('numero', n_devis))
        flash('Le devis n°{} a été ajouté avec succès !'.format(n_devis), 'success')
    else:
        flash("Erreur lors de la suppression du devis n° {} !".format(n_devis), 'danger')

def convert_date(date):
    if not date:
        return 'Aucune'
    date = date.replace('-', '/')
    l_mois = ['', 'Jan.', 'Fev.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Aou.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
    l_date = date.split('/')
    month = l_date[1]
    return '{} {} {}'.format(l_date[0], l_mois[int(month)], l_date[2])

def pdf_file(factname, download):
    if not factname:
        return redirect('factures')
    fdao = FactureDAO()
    if not fdao.exist(fdao.where('name', factname)):
        return redirect('factures')
    facture = fdao.get(fdao.where('name', factname))[0]

    def date(dat):
        return '/'.join(reversed(dat.split('/')))

    presta_mois = '/'.join(facture.date_envoi.split('/')[1:])

    client = Client()
    cdao = ClientDAO()
    client = cdao.get(cdao.where('id', facture.id_client))[0]

    total = float(facture.total)
    if facture.tva:
        total *= 1.20

    profile = get_profile_from_session()

    adao = AssuranceDAO()
    assurance = adao.get([adao.where('id_profile', profile.id), adao.where('sel', 'True')])

    html_rendu = render_template(
        'template/pdf_template.html', profile=profile, 
        presta_mois=presta_mois, date=date, facture=facture, 
        convert_date=convert_date, Page_title='Facture',
        client=client, total=total, assurance=assurance, len=len
    )

    pdf = pdfkit.from_string(html_rendu, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    if download:
        response.headers['Content-Disposition'] = 'attachment; filename=Facture_{}.pdf'.format(factname)
    else:
        response.headers['Content-Disposition'] = 'inline; filename=Facture_{}.pdf'.format(factname)
    return response

@manager_devis.route('/devis')
def devis():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    l_clients = get_list_client(profile.id)
    ddao = DevisDAO()
    l_devis = ddao.get(ddao.where('id_profile', profile.id))
    return render_template(
        'devis.html', convert_date=convert_date, 
        Page_title='Devis', devis=reversed(l_devis),
        clients=l_clients,
        get_client_name=get_client_name, profile=profile, len=len, color=Color
    )

@manager_devis.route('/devis/<int:numero>')
def devis_id(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, True)

@manager_devis.route('/pdf-devis/<int:numero>')
def devis_pdf(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, False)

@manager_devis.route('/devis-delete', methods=['POST'])
def devis_del():
    if not session.get('logged_in'):
        return redirect('/')
    remove_devis(request.form['devis-id'])
    return redirect('/devis')

@manager_devis.route('/devis-add', methods=['POST'])
def devis_add():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        add_devis(request.form)
    return redirect('/devis')
