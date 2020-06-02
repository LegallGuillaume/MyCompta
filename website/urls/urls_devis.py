from flask import Blueprint
from models.devis.devis import Devis, DevisDAO
from models.color import Color
from urls.urls_client import get_list_client, ClientDAO, Client, get_client_name
from urls.urls_assurance import AssuranceDAO, Assurance
from settings.config import TVA
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, make_response, session
import pdfkit
import datetime

manager_devis = Blueprint("devis", __name__)

def add_devis(form):
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
    facture = Facture()
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
    fdao = FactureDAO()

    if fdao.insert(facture):
        flash('La facture {} a été ajoutée avec succès !'.format(facture.name), 'success')
        if id_profile in CACHE_FACTURE.keys():
            del CACHE_FACTURE[id_profile]
    else:
        flash("Erreur lors de la création de la facture {} !".format(facture.name), 'danger')

def remove_devis(facturename):
    fdao = FactureDAO()
    if fdao.delete(fdao.where('name', facturename)):
        flash('La facture {} a été supprimée avec succès !'.format(facturename), 'success')
        if id_profile in CACHE_FACTURE.keys():
            del CACHE_FACTURE[id_profile]
    else:
        flash("Erreur lors de la suppression de la facture {} !".format(facturename), 'danger')


def convert_date(date):
    if not date:
        return 'Aucune'
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

@manager_devis.route('/devis', methods=['GET','POST'])
def devis():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    if request.method == 'GET':
        l_clients = get_list_client(profile.id)
        ddao = DevisDAO()
        l_devis = ddao.get(ddao.where('id_profile', profile.id))
        return render_template(
            'devis.html', convert_date=convert_date, 
            Page_title='Devis', devis=reversed(l_devis),
            clients=l_clients,
            get_client_name=get_client_name, profile=profile, len=len, color=Color
        )
    elif request.method == 'POST':
        add_devis(request.form)
        return redirect('/devis')
    else:
        return redirect('/home')

@manager_devis.route('/devis/<int:numero>')
def fact_name(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, True)

@manager_devis.route('/pdf-devis/<int:numero>')
def fact_pdf(factname = None):
    if not session.get('logged_in'):
        return redirect('/')
    return pdf_file(factname, False)

@manager_devis.route('/devis-delete', methods=['POST'])
def fact_del():
    if not session.get('logged_in'):
        return redirect('/')
    remove_devis(request.form['devis-id'])
    return redirect('/devis')

@manager_devis.route('/devis-add', methods=['POST'])
def fact_add():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        add_devis(request.form)
    return redirect('/devis')
