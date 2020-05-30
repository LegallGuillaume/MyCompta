from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from models.facture import Facture, FactureDAO
from models.profile import Profile, ProfileDAO
from models.coffre import Coffre, CoffreDAO
from models.withdraw import WithdrawDAO, Withdraw
from models.color import Color
from settings.tools import get_profile_from_session, CACHE_FACTURE
from urls.urls_facture import manager_facture, get_list_facture, convert_date
from urls.urls_client import manager_client, get_client_name, ClientDAO
from urls.urls_assurance import manager_assurance, AssuranceDAO
from urls.urls_profile import manager_profile
import datetime

app = Flask(__name__, static_folder='static/', template_folder='html/')
app.secret_key = "dsd999fsdf78zeSDez25ré(Fàç!uy23hGg¨*%H£23)"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.register_blueprint(manager_facture, url_prefix="/")
app.register_blueprint(manager_client, url_prefix="/")
app.register_blueprint(manager_assurance, url_prefix="/")
app.register_blueprint(manager_profile, url_prefix="/")

# return 'id' : {l_factures, sold_en, last_f, attent_f}
def get_element_profile_factures(id):
    if not CACHE_FACTURE or id not in CACHE_FACTURE.keys():
        l_factures, sold_en, last_f, attent_f = get_list_facture(id)
        dic = {
            'l_factures': l_factures,
            'sold_en': sold_en,
            'last_f': last_f,
            'attent_f': attent_f,
        }
        CACHE_FACTURE[id] = dic
    return CACHE_FACTURE[id]
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = str(request.form['user-name'])
        pwd = str(request.form['user-password'])
        pdao = ProfileDAO()
        if pdao.check_auth(pdao.where('email', email), pwd):
            session['logged_in'] = str(pdao.get(pdao.where('email', email))[0].id)
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/home')

@app.route('/logout')
def logout():
    del session['logged_in']
    return redirect('/')

@app.route('/home')
def accueil():
    if not session.get('logged_in'):
        return redirect('/')
    profile = get_profile_from_session()
    dic_profile = get_element_profile_factures(profile.id)
    l_factures = dic_profile['l_factures']
    sold_en = dic_profile['sold_en']
    last_f = dic_profile['last_f']
    attent_f = dic_profile['attent_f']

    now = datetime.datetime.now()
    annee = now.year

    tva_total = 0
    ttc_encaissee = 0
    fact_avail = 72000
    ttc_encaissee_last_year = 0
    for fact in l_factures:
        if fact.date_echeance.split('/')[2] == str(annee):
            if fact.tva:
                fact_avail -= (float(fact.total)*1.20)
                if fact.payee:
                    ttc_encaissee += (float(fact.total)*1.20)
            else:
                fact_avail -= float(fact.total)
                if fact.payee:
                    ttc_encaissee += float(fact.total)
        elif fact.date_echeance.split('/')[2] == str(annee-1):
            if fact.payee:
                if fact.tva:
                    ttc_encaissee_last_year += (float(fact.total)*1.20)
                else:
                    ttc_encaissee_last_year += float(fact.total)
        if fact.payee:
            if fact.tva:
                tva_total += (float(fact.total)*0.20)

    return render_template(
        'accueil.html', convert_date=convert_date, 
        Page_title='Accueil', factures=reversed(l_factures), 
        solde_encaissee=sold_en, last_facture=last_f, 
        solde_non_payee=attent_f, annee=annee, get_client_name=get_client_name,
        profile=profile, tva_total=tva_total, ttc_encaissee=ttc_encaissee, 
        facturation_available=fact_avail, color=Color, annee_1=(annee-1), 
        fact_enc_last_year=ttc_encaissee_last_year
    )


if __name__ == "__main__":
    pdao = ProfileDAO()
    for profile in pdao.get_list_profile():
        id = pdao.get_profile_id(pdao.where('siret', profile.siret))
        get_element_profile_factures(id)
    app.run(host='0.0.0.0', port=5000, debug=False)