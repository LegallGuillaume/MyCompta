from flask import Blueprint
from models.insurance import Insurance, InsuranceDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, session


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
        flash('L\'assurance {} a été ajoutée avec succès !'.format(insurance.name), 'success')
    else:
        flash("Erreur lors de la création de l\'assurance {} !".format(insurance.name), 'danger')

def remove_insurance(assurancename):
    adao = InsuranceDAO()
    if adao.delete(adao.where('name', assurancename)):
        flash('L\'assurance {} a été supprimée avec succès !'.format(assurancename), 'success')
    else:
        flash("Erreur lors de la suppression de l\'assurance {} !".format(assurancename), 'danger')

def select_insurance(assurancename, select):
    adao = InsuranceDAO()
    profile=get_profile_from_session()
    assu = adao.get([adao.where('name', assurancename), adao.where('id_profile', profile.id)])[0]
    assu.sel = select
    adao.update(assu, adao.where('name', assurancename))

def get_list_insurance(id_profile):
    adao = InsuranceDAO()
    return adao.get(adao.where('id_profile', id_profile))

@manager_insurance.route('/insurance', methods=['GET', 'POST'])
def as_():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'GET':
        profile=get_profile_from_session()
        l_assurances = get_list_insurance(profile.id)
        return render_template('insurance.html', Page_title='Insurance', assurances=reversed(l_assurances),
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
    remove_insurance(request.form['assurance-name'])
    return redirect('/insurance')

@manager_insurance.route('/insurance-select', methods=['POST'])
def as_select():
    if not session.get('logged_in'):
        return redirect('/')
    select_insurance(request.form['assurance-name'], request.form['assurance-select'])
    return redirect('/insurance')