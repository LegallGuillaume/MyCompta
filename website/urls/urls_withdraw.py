from flask import Blueprint
from models.withdraw import Withdraw, WithdrawDAO
from models.color import Color
from settings.tools import get_profile_from_session
from urls.urls_facture import convert_date
from flask import flash, request, render_template, redirect, make_response, session

manager_withdraw = Blueprint("withdraw", __name__)

def add_withdraw(form, id_profile):
    withdraw = Withdraw()
    withdraw.money = form['withdraw-money']
    withdraw.motif = form['withdraw-motif']
    withdraw.id_profile = id_profile
    wdao = WithdrawDAO()
    wdao.insert(withdraw)

def del_withdraw(form):
    id = form['withdraw-id']
    wdao = WithdrawDAO()
    wdao.delete(wdao.where('id', id))

@manager_withdraw.route('/withdraw', methods=['GET'])
def withdraw_():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    if request.method == 'GET':
        wdao = WithdrawDAO()
        user = '{} {}'.format(profile.name, profile.prenom)
        l_withdraw = wdao.get(wdao.where('id_profile', profile.id))
        return render_template(
            'withdraw.html', convert_date=convert_date, withdraws=reversed(l_withdraw),
            utilisateur= user, profile=profile, Page_title='Dépences', color=Color
        )
    return redirect('/home')

@manager_withdraw.route('/withdraw-add', methods=['POST'])
def withdraw_add():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    add_withdraw(request.form, profile.id)
    return redirect('/withdraw')

@manager_withdraw.route('/withdraw-del', methods=['POST'])
def withdraw_del():
    if not session.get('logged_in'):
        return redirect('/')
    del_withdraw(request.form)
    return redirect('/withdraw')