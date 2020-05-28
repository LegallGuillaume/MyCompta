from flask import Blueprint
from settings.tools import get_profile_from_session
from models.facture import FactureDAO, Facture
from models.color import Color
from urls.urls_client import get_client_name
from models.coffre import Coffre, CoffreDAO
from flask import flash, request, render_template, redirect, make_response, session


manager_coffre = Blueprint("coffre", __name__)

def exist_coffre(factureid):
    cdao = CoffreDAO()
    return cdao.exist(cdao.where('id_facture', factureid))

@manager_coffre.route('/coffre', methods=['POST', 'GET'])
def coffre():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    codao = CoffreDAO()
    fdao = FactureDAO()
    if request.method == 'GET':
        l_factures = fdao.get([ fdao.where('id_profile', profile.id), fdao.where('payee', True)])
        for f in l_factures:
            if exist_coffre(f.id):
                f.coffre = codao.get(codao.where('id_facture', f.id))[0]
        return render_template(
            'coffre.html', Page_title='Coffre', factures=reversed(l_factures),
            get_client_name=get_client_name, profile=profile, exist_coffre=exist_coffre, color=Color
        )
    elif request.method == 'POST':
        c1 = Coffre()
        facturename = request.form['facture-name']
        c1.tauxtva = float(request.form['facture-tva'])
        c1.tauxfiscal = float(request.form['facture-fiscal'])
        c1.tauxcharge = float(request.form['facture-charge'])
        c1.tauximpot = float(request.form['facture-impot'])
        c1.id_profile = profile.id
        f1 = fdao.get(fdao.where('name', facturename))[0]
        c1.id_facture = f1.id
        total = float(f1.total)

        tmp_charge = 0
        if c1.tauxcharge > 0:
            tmp_charge = total / 100 * c1.tauxcharge
            c1.charge = float('{:.2f}'.format(tmp_charge))

        tmp_tva = 0
        if c1.tauxtva > 0:
            tmp_tva = (total - tmp_charge) / 100 * c1.tauxtva
            c1.tva = float('{:.2f}'.format(tmp_tva))
        
        tmp_fiscal = 0
        if c1.tauxfiscal > 0:
            tmp_fiscal = (total - tmp_charge - tmp_tva) / 100 * c1.tauxfiscal
            c1.fiscal = float('{:.2f}'.format(tmp_fiscal))

        tmp_impot = 0
        if c1.tauximpot > 0:
            tmp_impot = (total - tmp_charge - tmp_tva - tmp_fiscal) / 100 * c1.tauximpot
            c1.impot = float('{:.2f}'.format(tmp_impot))

        c1.total = float('{:.2f}'.format(tmp_charge + tmp_impot + tmp_tva))

        if codao.insert(c1):
            flash('Vous devrez payé {} € sur la facture {}'.format(c1.total, facturename), 'success')
        else:
            flash('Une erreur est survenue lors de la fiche de paie {}'.format(facturename), 'danger')
        return redirect('/coffre')
    else:
        return redirect('/home')

@manager_coffre.route('/coffre-del', methods=['POST'])
def coffre_del():
    if not session.get('logged_in'):
        return redirect('/')
    form = request.form
    id = form['coffre-id']
    codao = CoffreDAO()
    if codao.delete(codao.where('id', id)):
        flash('Vous avez supprimé le coffre {} avec succès'.format(form['coffre-name']), 'success')
    else:
        flash('Une erreur est survenue dans la suppression du coffre {}'.format(form['coffre-name']), 'danger')
    return redirect('/coffre')
