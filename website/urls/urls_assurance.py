from flask import Blueprint
from models.assurance import Assurance, AssuranceDAO
from models.color import Color
from settings.tools import get_profile_from_session
from flask import flash, request, render_template, redirect, session


manager_assurance = Blueprint("assurance", __name__)

def add_assurance(form):
    profile=get_profile_from_session()
    assurance = Assurance()
    assurance.name = form['assurance-name']
    assurance.type = form['assurance-type']
    assurance.region = form['assurance-region']
    assurance.n_contrat = form['assurance-contrat']
    assurance.sel = False
    assurance.id_profile = profile.id
    adao = AssuranceDAO()
    if adao.insert(assurance):
        flash('L\'assurance {} a été ajoutée avec succès !'.format(assurance.name), 'success')
    else:
        flash("Erreur lors de la création de l\'assurance {} !".format(assurance.name), 'danger')

def remove_assurance(assurancename):
    adao = AssuranceDAO()
    if adao.delete(adao.where('name', assurancename)):
        flash('L\'assurance {} a été supprimée avec succès !'.format(assurancename), 'success')
    else:
        flash("Erreur lors de la suppression de l\'assurance {} !".format(assurancename), 'danger')

def select_assurance(assurancename, select):
    adao = AssuranceDAO()
    profile=get_profile_from_session()
    assu = adao.get([adao.where('name', assurancename), adao.where('id_profile', profile.id)])[0]
    assu.sel = select
    adao.update(assu, adao.where('name', assurancename))

def get_list_assurances(id_profile):
    adao = AssuranceDAO()
    return adao.get(adao.where('id_profile', id_profile))

@manager_assurance.route('/assurance', methods=['GET', 'POST'])
def as_():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'GET':
        profile=get_profile_from_session()
        l_assurances = get_list_assurances(profile.id)
        return render_template('assurance.html', Page_title='Assurance', assurances=reversed(l_assurances),
                                profile=profile, color=Color)
    elif request.method == 'POST':
        add_assurance(request.form)
        return ''
    else:
        return redirect('/home')

@manager_assurance.route('/assurance-delete', methods=['POST'])
def as_del():
    if not session.get('logged_in'):
        return redirect('/')
    remove_assurance(request.form['assurance-name'])
    return redirect('/assurance')

@manager_assurance.route('/assurance-select', methods=['POST'])
def as_select():
    if not session.get('logged_in'):
        return redirect('/')
    select_assurance(request.form['assurance-name'], request.form['assurance-select'])
    return redirect('/assurance')