from flask_socketio import SocketIO
from flask import Flask
from flask_babel import Babel, lazy_gettext as _

from urls.urls_client import manager_client, get_client_name, add_client, remove_client
from urls.urls_insurance import manager_insurance, add_insurance, remove_insurance, select_insurance
from urls.urls_invoice import manager_invoice, get_new_invoice, add_invoice, remove_invoice, bill, convert_date
from urls.urls_profile import manager_profile
from urls.urls_quotation import manager_quotation
import logging
import json


app = Flask(__name__, static_folder='../static/', template_folder='../html/')
app.config['BABEL_TRANSLATION_DIRECTORIES'] = '../../translations'
babel = Babel(app, default_locale='en')
app.secret_key = "dsd999fsdf78zeSDez25ré(Fàç!uy23hGg¨*%H£23)"
app.register_blueprint(manager_invoice, url_prefix="/")
app.register_blueprint(manager_client, url_prefix="/")
app.register_blueprint(manager_insurance, url_prefix="/")
app.register_blueprint(manager_profile, url_prefix="/")
app.register_blueprint(manager_quotation, url_prefix="/")
socketio = SocketIO(app)

class MESSAGE_TYPE:
    danger  = 'danger'
    info    = 'info'
    warning = 'warning'
    success = 'success'
    question = 'question'

## send to client OK if json receive else Error
def emit_result(typ, message):
    data = {'type': typ, 'message': str(message)}
    socketio.emit('alert', data, namespace='/')

def emit_add_invoice(invoice_obj):
    data = {
        'sold' : invoice_obj.sold,
        'name' : invoice_obj.name,
        'client' : get_client_name(invoice_obj.id_client),
        'project' : invoice_obj.project,
        'date_sent' : convert_date(invoice_obj.date_sent),
        'days' : invoice_obj.days,
        'day_rate' : invoice_obj.day_rate,
        'tax' : invoice_obj.tax,
        'date_expiry' : convert_date(invoice_obj.date_expiry),
        'total' : invoice_obj.total,
        'total_tax' : str(float(invoice_obj.total)*(1.20)),
        'YES' : str(_('Yes')),
        'NO' : str(_('No')),
    }
    socketio.emit('add-invoice', data, namespace='/')

def emit_add_client(client_obj):
    data = {
        'id' : client_obj.id,
        'name' : client_obj.name,
        'city' : client_obj.city,
        'country' : client_obj.country,
        'address' : client_obj.address,
        'comp_address' : client_obj.comp_address
    }
    socketio.emit('add-client', data, namespace='/')

def emit_delete_client(clientname):
    data = {
        'name' : clientname.replace(' ', '-')
    }
    socketio.emit('delete-client', data, namespace='/')

def emit_add_insurance(insurance_obj):
    data = {
        'id' : insurance_obj.id,
        'name' : insurance_obj.name,
        'type' : insurance_obj.type,
        'region' : insurance_obj.region,
        'sel' : insurance_obj.sel,
        'SELECT' : str(_('Selected')),
        'NOTSELECT' : str(_('Not Selected'))
    }
    socketio.emit('add-insurance', data, namespace='/')

def emit_delete_insurance(insurancename):
    data = {
        'name' : insurancename.replace(' ', '-')
    }
    socketio.emit('delete-insurance', data, namespace='/')

@socketio.on('v3-invoice-add')
def v3_invoice_add(data):
    logging.info('receive socket from /v3-invoice-add')
    logging.debug('add invoice form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret, invoice = add_invoice(data)
    if ret == 1:
        emit_result(MESSAGE_TYPE.warning, _('This client no longer exists, please reload the page !'))
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.warning, _('Impossible to add this invoice, Your session has been expired'))
        return
    elif ret == 3:
        emit_result(MESSAGE_TYPE.success, _('The invoice %1 has been added successfull').replace('%1', data['invoice_name']))
        new_invoice = get_new_invoice()
        socketio.emit('invoice-name', {'name': new_invoice}, namespace='/')
        emit_add_invoice(invoice)
        return
    elif ret == 4:
        emit_result(MESSAGE_TYPE.danger, _('Error while creation of invoice %1 !').replace('%1', data['invoice_name']))
        return

@socketio.on('v3-invoice-delete')
def v3_invoice_delete(data):
    logging.info('receive socket from /v3-invoice-delete')
    logging.debug('delete invoice form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret = remove_invoice(data['invoice_name'])
    if ret == 1:
        emit_result(MESSAGE_TYPE.warning, _('Impossible to add this invoice, Your session has been expired'))
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.success, _('The invoice %1 has been deleted successfull').replace('%1', data['invoice_name']))
        new_invoice = get_new_invoice()
        socketio.emit('invoice-name', {'name': new_invoice}, namespace='/')
        socketio.emit('delete-invoice', {'name': data['invoice_name']}, namespace='/')
        return
    elif ret == 3:
        emit_result(MESSAGE_TYPE.danger, _('Error while suppression of invoice %1 !').replace('%1', data['invoice_name']))
        return

@socketio.on('v3-invoice-bill')
def v3_invoice_bill(data):
    logging.info('receive socket from /v3-invoice-bill')
    logging.debug('bill invoice form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret = bill(data['invoice_name'], True)
    if ret == 1:
        emit_result(MESSAGE_TYPE.warning, _('Impossible to add this invoice, Your session has been expired'))
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.success, _('The invoice %1 has been sold successfull').replace('%1', data['invoice_name']))
        socketio.emit('bill-invoice', {'name': data['invoice_name']}, namespace='/')
        return
    elif ret == 3:
        emit_result(MESSAGE_TYPE.danger, _('Error while invoice %1 has been sold').replace('%1', data['invoice_name']))
        return

@socketio.on('v3-client-add')
def v3_client_add(data):
    logging.info('receive socket from /v3-client-add')
    logging.debug('add client form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret, client = add_client(data)
    if ret == 1:
        emit_result(MESSAGE_TYPE.success, _('The client %1 has been added successfull').replace('%1', data['client_name']))
        emit_add_client(client)
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.danger, _('Error while creation of client %1 !').replace('%1', data['client_name']))
        return

@socketio.on('v3-client-delete')
def v3_client_delete(data):
    logging.info('receive socket from /v3-client-delete')
    logging.debug('delete client form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret = remove_client(data['client_name'])
    if ret == 1:
        emit_result(MESSAGE_TYPE.success, _('The client %1 has been deleted!').replace('%1', data['client_name']))
        emit_delete_client(data['client_name'])
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.danger, _('Error while supression of client %1 !').replace('%1', data['client_name']))
        return

@socketio.on('v3-insurance-add')
def v3_insurance_add(data):
    logging.info('receive socket from /v3-insurance-add')
    logging.debug('add insurance form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret, insurance = add_insurance(data)
    if ret == 1:
        emit_result(MESSAGE_TYPE.success, _("The insurance %1 has been added successfull").replace('%1', data['insurance_name']))
        emit_add_insurance(insurance)
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.danger, _('Error while creation of insurance %1 !').replace('%1', data['insurance_name']))
        return

@socketio.on('v3-insurance-delete')
def v3_insurance_delete(data):
    logging.info('receive socket from /v3-insurance-delete')
    logging.debug('delete insurance form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret = remove_insurance(data['insurance_name'])
    if ret == 1:
        emit_result(MESSAGE_TYPE.success, _('The insurance %1 has been deleted successfull').replace('%1', data['insurance_name']))
        emit_delete_insurance(data['insurance_name'])
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.danger, _('Error while supression of insurance %1 !').replace('%1', data['insurance_name']))
        return

@socketio.on('v3-insurance-sel')
def v3_insurance_sel(data):
    logging.info('receive socket from /v3-insurance-sel')
    logging.debug('sel insurance form : %s', str(data))
    if '' in data.values():
        emit_result(MESSAGE_TYPE.warning, _('Please fill in all fields !'))
        return
    ret = select_insurance(data['insurance_name'], True)
    if ret == 1:
        emit_result(MESSAGE_TYPE.success, _('The insurance %1 has been selected successfull').replace('%1', data['insurance_name']))
        socketio.emit('sel-insurance', {'name': data['insurance_name'], 'SELECT': str(_('Selected'))}, namespace='/')
        return
    elif ret == 2:
        emit_result(MESSAGE_TYPE.danger, _('Error while insurance %1 has been selected').replace('%1', data['insurance_name']))
        return
