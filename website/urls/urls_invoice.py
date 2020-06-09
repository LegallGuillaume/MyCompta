from flask import Blueprint
from models.invoice import InvoiceDAO, Invoice
from models.color import Color
from urls.urls_client import get_list_client, ClientDAO, Client, get_client_name
from urls.urls_insurance import InsuranceDAO, Insurance
from settings.config import TVA
from settings.tools import get_profile_from_session, CACHE_INVOICE
from flask import flash, request, render_template, redirect, make_response, session
import pdfkit
import datetime

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

manager_invoice = Blueprint("invoice", __name__)

def add_invoice(form):
    cdao = ClientDAO()
    if not cdao.exist(cdao.where('name', form['facture-client'])):
        flash("Ce client n'existe plus, veuillez recharger la page !", 'danger')
        return
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        flash("Impossible d'ajouter cette facture, car votre session a expirée", 'danger')
        return
    facture = Invoice()
    facture.name = form['facture-name']
    facture.projet = form['facture-projet']
    facture.tjm = float(form['facture-tjm'])
    facture.days = int(form['facture-jour'])
    facture.date_envoi = '/'.join(reversed(form['facture-dateenvoi'].split('-')))
    facture.date_echeance = '/'.join(reversed(form['facture-dateecheance'].split('-')))
    facture.delai_max = '/'.join(reversed(form['facture-delai'].split('-')))
    facture.tva = form['facture-tva'] == 'True'
    facture.total = (facture.tjm * facture.days)
    facture.id_client = cdao.get(cdao.where('name', form['facture-client']))[0].id
    facture.id_profile = id_profile
    fdao = InvoiceDAO()

    if fdao.insert(facture):
        flash('La facture {} a été ajoutée avec succès !'.format(facture.name), 'success')
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
    else:
        flash("Erreur lors de la création de la facture {} !".format(facture.name), 'danger')

def remove_invoice(facturename):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        flash("Impossible de supprimer cette facture, car votre session a expirée", 'danger')
        return
    fdao = InvoiceDAO()
    if fdao.delete(fdao.where('name', facturename)):
        flash('La facture {} a été supprimée avec succès !'.format(facturename), 'success')
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
    else:
        flash("Erreur lors de la suppression de la facture {} !".format(facturename), 'danger')

def bill(facturename, payer):
    profileSession = get_profile_from_session()
    if profileSession.id:
        id_profile = profileSession.id
    else:
        flash("Impossible de payée cette facture, car votre session a expirée", 'danger')
        return
    fdao = InvoiceDAO()
    fac = fdao.get(fdao.where('name', facturename))[0]
    fac.payee = payer
    del fac.total_ttc
    if fdao.update(fac):
        flash('La facture {} {} avec succès !'.format(facturename, 'a été payée' if payer else 'a été rééditée'), 'success')
        if id_profile in CACHE_INVOICE.keys():
            del CACHE_INVOICE[id_profile]
    else:
        flash("Erreur lors de la {} du paiement de la facture {} !".format('validation' if payer else 'réédition', facturename), 'danger')

def get_list_invoice(id_profile):
    fdao = InvoiceDAO()
    l_factures = fdao.get(fdao.where('id_profile', id_profile))
    sold_en = 0
    last_f = ''
    attent_f = 0
    for facture in l_factures:
        if facture.payee:
            sold_en += float(facture.total)
        else:
            attent_f += float(facture.total)
        if facture.tva:
            facture.total_ttc = str(float(facture.total)*1.20)
        if last_f:
            tmp1 = facture.date_envoi.split('/')
            tmp1.reverse()
            tmp2 = last_f.split('/')
            tmp2.reverse()
            tmp_fact = int(''.join(tmp1))
            tmp_last = int(''.join(tmp2))
            if tmp_fact < tmp_last:
                continue
        last_f = facture.date_envoi
    return l_factures, sold_en, last_f, attent_f

def convert_date(date):
    if not date:
        return 'Aucune'
    l_mois = ['', 'Jan.', 'Fev.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Aou.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
    l_date = date.split('/')
    month = l_date[1]
    return '{} {} {}'.format(l_date[0], l_mois[int(month)], l_date[2])

def get_new_invoice():
    fdao = InvoiceDAO()
    now = datetime.datetime.now()
    annee = now.year
    profile = get_profile_from_session()
    l_fact = fdao.get(fdao.where('id_profile', profile.id))
    last_f = ''
    for facture in l_fact:
        if last_f:
            tmp_fact = int(''.join(facture.name.split('-')))
            tmp_last = int(''.join(last_f.split('-')))
            if tmp_fact < tmp_last:
                continue
        last_f = facture.name
    if last_f:
        last_f.split('-')[0]
        if annee == int(last_f.split('-')[0]):
            nb = last_f.split('-')[1]
            nb = int(nb) + 1
            return '{}-{:04d}'.format(str(annee), nb)
    return '{}-0001'.format(annee)

def pdf_file(factname, download):
    if not factname:
        return redirect('invoices')
    fdao = InvoiceDAO()
    if not fdao.exist(fdao.where('name', factname)):
        return redirect('invoices')
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

    adao = InsuranceDAO()
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

@manager_invoice.route('/invoices', methods=['GET','POST'])
def facts():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    if request.method == 'GET':
        l_factures, sold_en, last_f, attent_f = get_list_invoice(profile.id)
        l_clients = get_list_client(profile.id)
        return render_template(
            'invoice.html', convert_date=convert_date, 
            Page_title='Factures', factures=reversed(l_factures), 
            solde_encaissee=sold_en, last_facture=last_f, 
            solde_non_payee=attent_f, clients=l_clients, new_facture=get_new_invoice(),
            get_client_name=get_client_name, profile=profile, len=len, color=Color
        )
    elif request.method == 'POST':
        add_invoice(request.form)
        return redirect('/invoices')
    else:
        return redirect('/home')

@manager_invoice.route('/invoice/<factname>')
def fact_name(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, True)

@manager_invoice.route('/pdf/<factname>')
def fact_pdf(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, False)

@manager_invoice.route('/invoice-delete', methods=['POST'])
def fact_del():
    if not session.get('logged_in'):
        return redirect('/')
    remove_invoice(request.form['facture-name'])
    return redirect('/invoices')

@manager_invoice.route('/invoice-payee', methods=['POST'])
def fact_payee():
    if not session.get('logged_in'):
        return redirect('/')
    bill(request.form['facture-name'], request.form['facture-payee'] == 'True')
    return redirect('/invoices')

@manager_invoice.route('/invoice-add', methods=['POST'])
def fact_add():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        add_invoice(request.form)
    return redirect('/invoices')
