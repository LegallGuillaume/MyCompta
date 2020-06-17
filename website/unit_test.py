import unittest
import os
import logging
from models.client import ClientDAO, Client
from models.db import DbDAO, DB
from models.insurance import InsuranceDAO, Insurance
from models.invoice import InvoiceDAO, Invoice
from models.profile import ProfileDAO, Profile
from models.quotation.quotation import QuotationDAO, Quotation
from models.quotation.item_quotation import QuotationItemDAO, QuotationItem

DB_PATH = ''

class DbTestCase(unittest.TestCase):
    def test_connection(self):
        self.db = DB(DB_PATH)
        self.assertIsNotNone(self.db, msg='Impossible to create db "test_db"')
        self.assertIsNotNone(self.db.get_con(), msg='Impossible to connect to db "test_db"')
        self.db.close()
        self.assertIsNone(self.db.conn, msg='Impossible to disconnect to db "test_db"')

class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.cdao = ClientDAO(DB_PATH)
        self.client = Client()
        self.client.address = "TEST 1"
        self.client.comp_address = "TEST 2"
        self.client.zipcode = "TEST 3"
        self.client.id_profile = 1
        self.client.name = "TEST 4"
        self.client.country = "TEST 5"
        self.client.city = "TEST 6"
    def test_client_obj(self):
        self.assertIsNotNone(self.cdao, msg="Impossible to instance ClientDAO")
        self.assertTrue(self.cdao.create_table(), msg="Impossible to create client table in db")
        self.assertFalse(self.cdao.exist(self.client), msg="Impossible to check client exist in db")
        self.assertTrue(self.cdao.insert(self.client), msg="Impossible to insert client in db")
        list_client = self.cdao.get(self.cdao.where('name', self.client.name))
        self.assertIsInstance(list_client, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_client), 0, msg="No client in db")
        clt = list_client[0]
        self.assertIsInstance(clt, Client, msg="1st element of dao.get is not a Client obj")
        self.assertEqual(self.client.address, clt.address, msg="Client get, has no same attribute 'address'")
        self.assertEqual(self.client.comp_address, clt.comp_address, msg="Client get, has no same attribute 'comp_address'")
        self.assertEqual(self.client.zipcode, clt.zipcode, msg="Client get, has no same attribute 'zipcode'")
        self.assertEqual(self.client.id_profile, clt.id_profile, msg="Client get, has no same attribute 'id_profile'")
        self.assertEqual(self.client.name, clt.name, msg="Client get, has no same attribute 'name'")
        self.assertEqual(self.client.country, clt.country, msg="Client get, has no same attribute 'country'")
        self.assertEqual(self.client.city, clt.city, msg="Client get, has no same attribute 'city'")
        self.assertTrue(hasattr(clt, 'id'), msg="Client get, has no attribute 'id'")
        clt.city = "TEST 12"
        self.assertTrue(self.cdao.update(clt))
        list_client2 = self.cdao.get(self.cdao.where('name', clt.name))
        self.assertIsInstance(list_client2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_client2), 0, msg="No client 2 in db")
        clt2 = list_client2[0]
        self.assertEqual(clt2.city, clt.city, msg="Client get 2, has no same attribute 'city'")
        self.assertTrue(self.cdao.delete(clt), msg="Impossible to delete client from db")
        self.assertFalse(self.cdao.drop(True, False), msg="Drop table client not wanted")
        self.assertFalse(self.cdao.drop(False, True), msg="Drop table client not wanted")
        self.assertTrue(self.cdao.drop(True, True), msg="Cannot drop table client")
        self.assertFalse(self.cdao.drop(True, True), msg="The table has not deleted before")

class QuotationItemTestCase(unittest.TestCase):
    def setUp(self):
        self.iqdao = QuotationItemDAO(DB_PATH)
        self.item = QuotationItem()
        self.item.description = ""
        self.item.id_quotation = 1
        self.item.quantity = 12
        self.item.quantity_text = "12m2"
        self.item.reduction = False
        self.item.unit_price = 1.34
    def test_quotationitem_obj(self):
        self.assertIsNotNone(self.iqdao, msg="Impossible to instance QuotationItemDAO")
        self.assertTrue(self.iqdao.create_table(), msg="Impossible to create devis_item table in db")
        self.assertFalse(self.iqdao.exist(self.item), msg="Impossible to check QuotationItem exist in db")
        self.assertTrue(self.iqdao.insert(self.item), msg="Impossible to insert QuotationItem in db")
        list_item = self.iqdao.get(self.iqdao.where('description', self.item.description))
        self.assertIsInstance(list_item, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_item), 0, msg="No QuotationItem in db")
        itq = list_item[0]
        self.assertIsInstance(itq, QuotationItem, msg="1st element of dao.get is not a QuotationItem obj")
        self.assertEqual(self.item.description, itq.description, msg="QuotationItem get, has no same attribute 'description'")
        self.assertEqual(self.item.id_quotation, itq.id_quotation, msg="QuotationItem get, has no same attribute 'id_quotation'")
        self.assertEqual(self.item.quantity, itq.quantity, msg="QuotationItem get, has no same attribute 'quantity'")
        self.assertEqual(self.item.quantity_text, itq.quantity_text, msg="QuotationItem get, has no same attribute 'quantity_text'")
        self.assertEqual(self.item.reduction, itq.reduction, msg="QuotationItem get, has no same attribute 'reduction'")
        self.assertEqual(self.item.unit_price, itq.unit_price, msg="QuotationItem get, has no same attribute 'unit_price'")
        self.assertTrue(hasattr(itq, 'id'), msg="QuotationItem get, has no attribute 'id'")
        itq.unit_price = 4.20
        self.assertTrue(self.iqdao.update(itq))
        list_item2 = self.iqdao.get(self.iqdao.where('description', itq.description))
        self.assertIsInstance(list_item2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_item2), 0, msg="No QuotationItem 2 in db")
        itq2 = list_item2[0]
        self.assertEqual(itq2.unit_price, itq.unit_price, msg="QuotationItem get 2, has no same attribute 'unit_price'")
        self.assertTrue(self.iqdao.delete(itq), msg="Impossible to delete devis_item from db")
        self.assertFalse(self.iqdao.drop(True, False), msg="Drop table devis_item not wanted")
        self.assertFalse(self.iqdao.drop(False, True), msg="Drop table devis_item not wanted")
        self.assertTrue(self.iqdao.drop(True, True), msg="Cannot drop table devis_item")
        self.assertFalse(self.iqdao.drop(True, True), msg="The table has not deleted before")

class QuotationTestCase(unittest.TestCase):
    def setUp(self):
        self.qdao = QuotationDAO(DB_PATH)
        self.quotation = Quotation()
        self.quotation.client = "TEST 1"
        self.quotation.date_sent = "01/01/2020"
        self.quotation.date_validity = "01/01/2021"
        self.quotation.end_text = "TEST 2\nTEST 3\nTEST 4"
        self.quotation.id_profile = 1
        self.quotation.number = 230
        self.quotation.total = 2030.20
        self.quotation.tax_price = 55.10
    def test_quotation_obj(self):
        self.assertIsNotNone(self.qdao, msg="Impossible to instance QuotationDAO")
        self.assertTrue(self.qdao.create_table(), msg="Impossible to create devis table in db")
        self.assertFalse(self.qdao.exist(self.quotation), msg="Impossible to check Quotation exist in db")
        self.assertTrue(self.qdao.insert(self.quotation), msg="Impossible to insert Quotation in db")
        list_quotation = self.qdao.get(self.qdao.where('number', self.quotation.number))
        self.assertIsInstance(list_quotation, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_quotation), 0, msg="No Quotation in db")
        quota = list_quotation[0]
        self.assertIsInstance(quota, Quotation, msg="1st element of dao.get is not a Quotation obj")
        self.assertEqual(self.quotation.client, quota.client, msg="Quotation get, has no same attribute 'client'")
        self.assertEqual(self.quotation.date_sent, quota.date_sent, msg="Quotation get, has no same attribute 'date_sent'")
        self.assertEqual(self.quotation.date_validity, quota.date_validity, msg="Quotation get, has no same attribute 'date_validity'")
        self.assertEqual(self.quotation.end_text, quota.end_text, msg="Quotation get, has no same attribute 'end_text'")
        self.assertEqual(self.quotation.id_profile, quota.id_profile, msg="Quotation get, has no same attribute 'id_profile'")
        self.assertEqual(self.quotation.number, quota.number, msg="Quotation get, has no same attribute 'number'")
        self.assertEqual(self.quotation.total, quota.total, msg="Quotation get, has no same attribute 'total'")
        self.assertEqual(self.quotation.tax_price, quota.tax_price, msg="Quotation get, has no same attribute 'tax_price'")
        self.assertTrue(hasattr(quota, 'id'), msg="Quotation get, has no attribute 'id'")
        quota.end_text = "TEST 1\nTEST 2\nTEST3"
        self.assertTrue(self.qdao.update(quota))
        list_quotation2 = self.qdao.get(self.qdao.where('number', quota.number))
        self.assertIsInstance(list_quotation2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_quotation2), 0, msg="No Quotation 2 in db")
        quota2 = list_quotation2[0]
        self.assertEqual(quota2.end_text, quota.end_text, msg="Quotation get 2, has no same attribute 'end_text'")
        self.assertTrue(self.qdao.delete(quota), msg="Impossible to delete devis from db")
        self.assertFalse(self.qdao.drop(True, False), msg="Drop table devis not wanted")
        self.assertFalse(self.qdao.drop(False, True), msg="Drop table devis not wanted")
        self.assertTrue(self.qdao.drop(True, True), msg="Cannot drop table devis")
        self.assertFalse(self.qdao.drop(True, True), msg="The table has not deleted before")

class InsuranceTestCase(unittest.TestCase):
    def setUp(self):
        self.idao = InsuranceDAO(DB_PATH)
        self.insurance = Insurance()
        self.insurance.id_profile = 1
        self.insurance.n_contract = "1234567891011121314"
        self.insurance.name = "TEST 1"
        self.insurance.region = "FRANCE"
        self.insurance.sel = False
        self.insurance.type = "ALL INCLUDE"
    def test_insurance_obj(self):
        self.assertIsNotNone(self.idao, msg="Impossible to instance InsuranceDAO")
        self.assertTrue(self.idao.create_table(), msg="Impossible to create assurance table in db")
        self.assertFalse(self.idao.exist(self.insurance), msg="Impossible to check Insurance exist in db")
        self.assertTrue(self.idao.insert(self.insurance), msg="Impossible to insert Insurance in db")
        list_insurance = self.idao.get(self.idao.where('n_contract', self.insurance.n_contract))
        self.assertIsInstance(list_insurance, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_insurance), 0, msg="No Insurance in db")
        insur = list_insurance[0]
        self.assertIsInstance(insur, Insurance, msg="1st element of dao.get is not a Insurance obj")
        self.assertEqual(self.insurance.id_profile, insur.id_profile, msg="Insurance get, has no same attribute 'id_profile'")
        self.assertEqual(self.insurance.n_contract, insur.n_contract, msg="Insurance get, has no same attribute 'n_contract'")
        self.assertEqual(self.insurance.name, insur.name, msg="Insurance get, has no same attribute 'name'")
        self.assertEqual(self.insurance.region, insur.region, msg="Insurance get, has no same attribute 'region'")
        self.assertEqual(self.insurance.sel, insur.sel, msg="Insurance get, has no same attribute 'sel'")
        self.assertEqual(self.insurance.type, insur.type, msg="Insurance get, has no same attribute 'type'")
        self.assertTrue(hasattr(insur, 'id'), msg="Insurance get, has no attribute 'id'")
        insur.sel = True
        self.assertTrue(self.idao.update(insur))
        list_insurance2 = self.idao.get(self.idao.where('n_contract', insur.n_contract))
        self.assertIsInstance(list_insurance2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_insurance2), 0, msg="No Insurance 2 in db")
        insur2 = list_insurance2[0]
        self.assertEqual(insur2.sel, insur.sel, msg="Insurance get 2, has no same attribute 'sel'")
        self.assertTrue(self.idao.delete(insur), msg="Impossible to delete assurance from db")
        self.assertFalse(self.idao.drop(True, False), msg="Drop table assurance not wanted")
        self.assertFalse(self.idao.drop(False, True), msg="Drop table assurance not wanted")
        self.assertTrue(self.idao.drop(True, True), msg="Cannot drop table assurance")
        self.assertFalse(self.idao.drop(True, True), msg="The table has not deleted before")

class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.pdao = ProfileDAO(DB_PATH)
        self.profile = Profile()
        self.profile.address = 'TEST 1'
        self.profile.comp_address = 'TEST 2'
        self.profile.zipcode = '13132'
        self.profile.email = 'TEST1@TEST2.TEST3'
        self.profile.name = 'TEST'
        self.profile.password = 'CECIESTUNTEST'
        self.profile.country = 'FRANCE'
        self.profile.firstname = 'TEST 4'
        self.profile.siret = '0292029102'
        self.profile.phone = '0439403920'
        self.profile.city = 'MARSEILLE'
    def test_profile_obj(self):
        self.assertIsNotNone(self.pdao, msg="Impossible to instance ProfileDAO")
        self.assertTrue(self.pdao.create_table(), msg="Impossible to create profile table in db")
        self.assertFalse(self.pdao.exist(self.profile), msg="Impossible to check Profile exist in db")
        self.assertTrue(self.pdao.insert(self.profile), msg="Impossible to insert Profile in db")
        list_profile = self.pdao.get(self.pdao.where('siret', self.profile.siret))
        self.assertIsInstance(list_profile, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_profile), 0, msg="No Profile in db")
        prfl = list_profile[0]
        self.assertIsInstance(prfl, Profile, msg="1st element of dao.get is not a Profile obj")
        self.assertEqual(self.profile.address, prfl.address, msg="Profile get, has no same attribute 'address'")
        self.assertEqual(self.profile.comp_address, prfl.comp_address, msg="Profile get, has no same attribute 'comp_address'")
        self.assertEqual(self.profile.zipcode, prfl.zipcode, msg="Profile get, has no same attribute 'zipcode'")
        self.assertEqual(self.profile.email, prfl.email, msg="Profile get, has no same attribute 'email'")
        self.assertEqual(self.profile.name, prfl.name, msg="Profile get, has no same attribute 'name'")
        self.assertEqual(self.profile.password, prfl.password, msg="Profile get, has no same attribute 'password'")
        self.assertEqual(self.profile.country, prfl.country, msg="Profile get, has no same attribute 'country'")
        self.assertEqual(self.profile.firstname, prfl.firstname, msg="Profile get, has no same attribute 'firstname'")
        self.assertEqual(self.profile.siret, prfl.siret, msg="Profile get, has no same attribute 'siret'")
        self.assertEqual(self.profile.phone, prfl.phone, msg="Profile get, has no same attribute 'phone'")
        self.assertEqual(self.profile.city, prfl.city, msg="Profile get, has no same attribute 'city'")
        self.assertTrue(hasattr(prfl, 'id'), msg="Profile get, has no attribute 'id'")
        prfl.zipcode = '12131'
        self.assertTrue(self.pdao.update(prfl))
        list_profile2 = self.pdao.get(self.pdao.where('siret', prfl.siret))
        self.assertIsInstance(list_profile2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_profile2), 0, msg="No Profile 2 in db")
        prfl2 = list_profile2[0]
        self.assertEqual(prfl2.zipcode, prfl.zipcode, msg="Profile get 2, has no same attribute 'zipcode'")
        self.assertTrue(self.pdao.delete(prfl), msg="Impossible to delete profile from db")
        self.assertFalse(self.pdao.drop(True, False), msg="Drop table profile not wanted")
        self.assertFalse(self.pdao.drop(False, True), msg="Drop table profile not wanted")
        self.assertTrue(self.pdao.drop(True, True), msg="Cannot drop table profile")
        self.assertFalse(self.pdao.drop(True, True), msg="The table has not deleted before")

class InvoiceTestCase(unittest.TestCase):
    def setUp(self):
        self.fdao = InvoiceDAO(DB_PATH)
        self.invoice = Invoice()
        self.invoice.date_expiry = '01/01/2020'
        self.invoice.date_sent = '01/01/2020'
        self.invoice.days = 10
        self.invoice.max_delay = '01/01/2020'
        self.invoice.id_client = 1
        self.invoice.id_profile = 1
        self.invoice.name = 'FACTURE TEST 1'
        self.invoice.sold = False
        self.invoice.project = 'TEST 1 2 3'
        self.invoice.day_rate = 5000
        self.invoice.total = '50000'
        self.invoice.tax = False
    def test_invoice_obj(self):
        self.assertIsNotNone(self.fdao, msg="Impossible to instance InvoiceDAO")
        self.assertTrue(self.fdao.create_table(), msg="Impossible to create invoice table in db")
        self.assertFalse(self.fdao.exist(self.invoice), msg="Impossible to check Invoice exist in db")
        self.assertTrue(self.fdao.insert(self.invoice), msg="Impossible to insert Invoice in db")
        list_invoice = self.fdao.get(self.fdao.where('name', self.invoice.name))
        self.assertIsInstance(list_invoice, list, msg="dao.get function not return a list")
        self.assertGreater(len(list_invoice), 0, msg="No Invoice in db")
        invce = list_invoice[0]
        self.assertIsInstance(invce, Invoice, msg="1st element of dao.get is not a Invoice obj")
        self.assertEqual(self.invoice.date_expiry, invce.date_expiry, msg="Invoice get, has no same attribute 'date_expiry'")
        self.assertEqual(self.invoice.date_sent, invce.date_sent, msg="Invoice get, has no same attribute 'date_sent'")
        self.assertEqual(self.invoice.days, invce.days, msg="Invoice get, has no same attribute 'days'")
        self.assertEqual(self.invoice.max_delay, invce.max_delay, msg="Invoice get, has no same attribute 'max_delay'")
        self.assertEqual(self.invoice.id_client, invce.id_client, msg="Invoice get, has no same attribute 'id_client'")
        self.assertEqual(self.invoice.id_profile, invce.id_profile, msg="Invoice get, has no same attribute 'id_profile'")
        self.assertEqual(self.invoice.name, invce.name, msg="Invoice get, has no same attribute 'name'")
        self.assertEqual(self.invoice.sold, invce.sold, msg="Invoice get, has no same attribute 'sold'")
        self.assertEqual(self.invoice.project, invce.project, msg="Invoice get, has no same attribute 'project'")
        self.assertEqual(self.invoice.day_rate, invce.day_rate, msg="Invoice get, has no same attribute 'day_rate'")
        self.assertEqual(self.invoice.total, invce.total, msg="Invoice get, has no same attribute 'total'")
        self.assertEqual(self.invoice.tax, invce.tax, msg="Invoice get, has no same attribute 'tax'")
        self.assertTrue(hasattr(invce, 'id'), msg="Invoice get, has no attribute 'id'")
        invce.sold = True
        self.assertTrue(self.fdao.update(invce))
        list_invoice2 = self.fdao.get(self.fdao.where('name', invce.name))
        self.assertIsInstance(list_invoice2, list, msg="dao.get function not return a list 2")
        self.assertGreater(len(list_invoice2), 0, msg="No Invoice 2 in db")
        invce2 = list_invoice2[0]
        self.assertEqual(invce2.date_expiry, invce.date_expiry, msg="Invoice get 2, has no same attribute 'date_expiry'")
        self.assertEqual(invce2.date_sent, invce.date_sent, msg="Invoice get 2, has no same attribute 'date_sent'")
        self.assertEqual(invce2.days, invce.days, msg="Invoice get 2, has no same attribute 'days'")
        self.assertEqual(invce2.max_delay, invce.max_delay, msg="Invoice get 2, has no same attribute 'max_delay'")
        self.assertEqual(invce2.id_client, invce.id_client, msg="Invoice get 2, has no same attribute 'id_client'")
        self.assertEqual(invce2.id_profile, invce.id_profile, msg="Invoice get 2, has no same attribute 'id_profile'")
        self.assertEqual(invce2.name, invce.name, msg="Invoice get 2, has no same attribute 'name'")
        self.assertEqual(invce2.sold, invce.sold, msg="Invoice get 2, has no same attribute 'sold'")
        self.assertEqual(invce2.project, invce.project, msg="Invoice get 2, has no same attribute 'project'")
        self.assertEqual(invce2.day_rate, invce.day_rate, msg="Invoice get 2, has no same attribute 'day_rate'")
        self.assertEqual(invce2.total, invce.total, msg="Invoice get 2, has no same attribute 'total'")
        self.assertEqual(invce2.tax, invce.tax, msg="Invoice get 2, has no same attribute 'tax'")
        self.assertTrue(self.fdao.delete(invce), msg="Impossible to delete invoice from db")
        self.assertFalse(self.fdao.drop(True, False), msg="Drop table invoice not wanted")
        self.assertFalse(self.fdao.drop(False, True), msg="Drop table invoice not wanted")
        self.assertTrue(self.fdao.drop(True, True), msg="Cannot drop table invoice")
        self.assertFalse(self.fdao.drop(True, True), msg="The table has not deleted before")

if __name__ == '__main__':
    directory_test = 'test_dir'
    os.makedirs(directory_test, exist_ok=True)
    DB_PATH = directory_test + os.sep + 'test_db'
    open(DB_PATH, 'w').close()
    DEBUG = False
    format_log = '(%(asctime)s)(%(filename)s:%(lineno)d) %(levelname)s >> %(message)s'
    format_date = '%d/%m/%Y %I:%M:%S'
    if not DEBUG:
        logging.basicConfig(
            filename='test_unit.log',filemode='w', 
            format=format_log, datefmt=format_date,
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            format=format_log, datefmt=format_date,
            level=logging.DEBUG
        )
    unittest.main()
