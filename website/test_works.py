import os
import logging
from models.client import ClientDAO, Client
from models.db import DbDAO, DB
from models.insurance import InsuranceDAO, Insurance
from models.invoice import InvoiceDAO, Invoice
from models.profile import ProfileDAO, Profile
from models.enterprise import EnterpriseDAO, Enterprise
from models.quotation.quotation import QuotationDAO, Quotation
from models.quotation.item_quotation import QuotationItemDAO, QuotationItem

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

DB_PATH = '-'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    GET = '\033[100m'
    POST = '\033[104m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Test:
    def __init__(self):
        self.client = None
        self.insurance = None
        self.profile = None
        self.enterprise = None
        self.pdao = None

    def __init_db(self):
        print(bcolors.BOLD + '---------- CREATE DB ----------' + bcolors.ENDC)
        self.pdao = ProfileDAO(DB_PATH)
        pdaoret = self.pdao.create_table()
        print(bcolors.HEADER + 'ProfileDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if pdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.edao = EnterpriseDAO(DB_PATH)
        edaoret = self.edao.create_table()
        print(bcolors.HEADER + 'EnterpriseDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if edaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.idao = InsuranceDAO(DB_PATH)
        idaoret = self.idao.create_table()
        print(bcolors.HEADER + 'InsuranceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if idaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.fdao = InvoiceDAO(DB_PATH)
        fdaoret = self.fdao.create_table()
        print(bcolors.HEADER + 'InvoiceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if fdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.cdao = ClientDAO(DB_PATH)
        cdaoret = self.cdao.create_table()
        print(bcolors.HEADER + 'ClientDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if cdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.qdao = QuotationDAO(DB_PATH)
        qdaoret = self.qdao.create_table()
        print(bcolors.HEADER + 'QuotationDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if qdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        self.qidao = QuotationItemDAO(DB_PATH)
        qidaoret = self.qidao.create_table()
        print(bcolors.HEADER + 'QuotationItemDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if qidaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        return pdaoret and idaoret and fdaoret and cdaoret and qdaoret and qidaoret

    def drop_db(self):
        print(bcolors.BOLD + '---------- DROP DB ----------' + bcolors.ENDC)
        pdaoret = self.pdao.drop(True,True)
        print(bcolors.HEADER + 'ProfileDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if pdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        idaoret = self.idao.drop(True,True)
        print(bcolors.HEADER + 'InsuranceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if idaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        fdaoret = self.fdao.drop(True,True)
        print(bcolors.HEADER + 'InvoiceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if fdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        cdaoret = self.cdao.drop(True,True)
        print(bcolors.HEADER + 'ClientDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if cdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        qdaoret = self.qdao.drop(True,True)
        print(bcolors.HEADER + 'QuotationDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if qdaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        qidaoret = self.qidao.drop(True,True)
        print(bcolors.HEADER + 'QuotationItemDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if qidaoret else bcolors.FAIL + "KO", bcolors.ENDC)
        return pdaoret and idaoret and fdaoret and cdaoret and qdaoret and qidaoret

    def __profile_db(self):
        print(bcolors.BOLD + '---------- Profile DB ----------' + bcolors.ENDC)
        self.profile = Profile()
        self.profile.email = 'TEST1@TEST2.TEST3'
        self.profile.name = 'TEST 3'
        self.profile.firstname = 'TEST 4'
        self.profile.password = 'CECIESTUNTEST'
        self.profile.autoentrepreneur = False

        inspdao = self.pdao.insert(self.profile)
        print(bcolors.HEADER + 'insert profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if inspdao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.profile.password = "NEW PASSWORD"
        chpasswdpdao = self.pdao.update(self.profile)
        print(bcolors.HEADER + 'update profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chpasswdpdao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_profile_list = self.pdao.get(self.pdao.where('name', self.profile.name))
        print(bcolors.HEADER + 'get profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_profile_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_profile_list:
            return False
        get_profile = get_profile_list[0]
        chkauthpdao = self.pdao.check_auth(get_profile, "NEW PASSWORD")
        self.profile = get_profile
        print(bcolors.HEADER + 'auth profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chkauthpdao else bcolors.FAIL + "KO", bcolors.ENDC)
        return (inspdao and chpasswdpdao and chkauthpdao)

    def __enterprise_db(self):
        print(bcolors.BOLD + '---------- Enterprise DB ----------' + bcolors.ENDC)
        self.enterprise = Enterprise()
        self.enterprise.id_profile = self.profile.id
        self.enterprise.name = 'TEST 3'
        self.enterprise.slogan = 'CECI EST UN SLOGAN !'
        self.enterprise.address = 'TEST 1'
        self.enterprise.comp_address = 'TEST 2'
        self.enterprise.zipcode = '13132'
        self.enterprise.email = 'TEST1@TEST2.TEST3'
        self.enterprise.country = 'FRANCE'
        self.enterprise.siret = '0292029102'
        self.enterprise.phone = '0439403920'
        self.enterprise.city = 'MARSEILLE'

        insedao = self.edao.insert(self.enterprise)
        print(bcolors.HEADER + 'insert enterprise ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if insedao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.enterprise.slogan = "SLOGAN MODIFIER !"
        sloganchange = self.edao.update(self.enterprise)
        print(bcolors.HEADER + 'update enterprise ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if sloganchange else bcolors.FAIL + "KO", bcolors.ENDC)
        get_enterprise_list = self.edao.get(self.edao.where('siret', self.enterprise.siret))
        print(bcolors.HEADER + 'get enterprise ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_enterprise_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_enterprise_list:
            return False
        get_enterprise = get_enterprise_list[0]

        entermodif = (self.enterprise.slogan == get_enterprise.slogan)
        self.enterprise = get_enterprise
        print(bcolors.HEADER + 'slogan modify enterprise ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if entermodif else bcolors.FAIL + "KO", bcolors.ENDC)
        return (insedao and sloganchange and entermodif)

    def __insurance_db(self):
        print(bcolors.BOLD + '---------- Insurance DB ----------' + bcolors.ENDC)
        if not self.profile:
            print(bcolors.HEADER + 'no profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __profile_db()", bcolors.ENDC)
            return
        self.insurance = Insurance()
        self.insurance.id_profile = self.profile.id
        self.insurance.n_contract = "1234567891011121314"
        self.insurance.name = "TEST 1"
        self.insurance.region = "FRANCE"
        self.insurance.sel = False
        self.insurance.type = "ALL INCLUDE"

        insidao = self.idao.insert(self.insurance)
        print(bcolors.HEADER + 'insert insurance ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if insidao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.insurance.sel = True
        chselidao = self.idao.update(self.insurance)
        print(bcolors.HEADER + 'update insurance ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chselidao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_insurance_list = self.idao.get(self.idao.where('n_contract', self.insurance.n_contract))
        print(bcolors.HEADER + 'get insurance ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_insurance_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_insurance_list:
            return False
        is_sel_insurance = get_insurance_list[0].sel
        print(bcolors.HEADER + 'change sel insurance ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if is_sel_insurance else bcolors.FAIL + "KO", bcolors.ENDC)
        return (insidao and chselidao and is_sel_insurance)

    def __client_db(self):
        print(bcolors.BOLD + '---------- Client DB ----------' + bcolors.ENDC)
        if not self.profile:
            print(bcolors.HEADER + 'no profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __profile_db()", bcolors.ENDC)
            return
        self.client = Client()
        self.client.address = "TEST 1"
        self.client.comp_address = "TEST 2"
        self.client.zipcode = "TEST 3"
        self.client.id_profile = self.profile.id
        self.client.name = "TEST 4"
        self.client.country = "TEST 5"
        self.client.city = "TEST 6"

        inscdao = self.cdao.insert(self.client)
        print(bcolors.HEADER + 'insert client ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if inscdao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.client.zipcode = "13013"
        chzipcodecdao = self.cdao.update(self.client)
        print(bcolors.HEADER + 'update client ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chzipcodecdao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_client_list = self.cdao.get(self.cdao.where('name', self.client.name))
        print(bcolors.HEADER + 'get client ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_client_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_client_list:
            return False
        self.client = get_client_list[0]
        is_change_zipcode = (self.client.zipcode == "13013")
        print(bcolors.HEADER + 'change zip code client ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if is_change_zipcode else bcolors.FAIL + "KO", bcolors.ENDC)
        return (inscdao and chzipcodecdao and is_change_zipcode)

    def __invoice_db(self):
        print(bcolors.BOLD + '---------- Invoice DB ----------' + bcolors.ENDC)
        if not self.profile:
            print(bcolors.HEADER + 'no profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __profile_db()", bcolors.ENDC)
            return
        if not self.client:
            print(bcolors.HEADER + 'no client ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __client_db()", bcolors.ENDC)
            return
        self.invoice = Invoice()
        self.invoice.date_expiry = '01/01/2020'
        self.invoice.date_sent = '01/01/2020'
        self.invoice.days = 10
        self.invoice.max_delay = '01/01/2020'
        self.invoice.id_client = self.client.id
        self.invoice.id_profile = self.profile.id
        self.invoice.name = 'Invoice TEST 1'
        self.invoice.sold = False
        self.invoice.project = 'TEST 1 2 3'
        self.invoice.day_rate = 5000
        self.invoice.total = '50000'
        self.invoice.tax = False

        insindao = self.fdao.insert(self.invoice)
        print(bcolors.HEADER + 'insert invoice ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if insindao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.invoice.sold = True
        chpyfdao = self.fdao.update(self.invoice)
        print(bcolors.HEADER + 'update invoice ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chpyfdao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_invoice_list = self.fdao.get(self.fdao.where('id_client', self.invoice.id_client))
        print(bcolors.HEADER + 'get invoice ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_invoice_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_invoice_list:
            return False
        self.invoice = get_invoice_list[0]
        is_change_sold = self.invoice.sold
        print(bcolors.HEADER + 'change to bill invoice ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if is_change_sold else bcolors.FAIL + "KO", bcolors.ENDC)
        return (insindao and chpyfdao and is_change_sold)

    def __quotation_db(self):
        print(bcolors.BOLD + '---------- Quotation DB ----------' + bcolors.ENDC)
        if not self.profile:
            print(bcolors.HEADER + 'no profile ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __profile_db()", bcolors.ENDC)
            return
        self.quotation = Quotation()
        self.quotation.client = "TEST 1"
        self.quotation.date_sent = "01/01/2020"
        self.quotation.date_validity = "01/01/2021"
        self.quotation.end_text = "TEST 2\nTEST 3\nTEST 4"
        self.quotation.id_profile = self.profile.id
        self.quotation.number = 203
        self.quotation.total = 2030.20
        self.quotation.tax_price = (2030.20*0.2)

        insqdao = self.qdao.insert(self.quotation)
        print(bcolors.HEADER + 'insert quotation ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if insqdao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.quotation.end_text = "TEST 1\nTEST 2"
        chpyqdao = self.qdao.update(self.quotation)
        print(bcolors.HEADER + 'update quotation ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chpyqdao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_quotation_list = self.qdao.get(self.qdao.where('number', self.quotation.number))
        print(bcolors.HEADER + 'get quotation ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_quotation_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_quotation_list:
            return False
        self.quotation = get_quotation_list[0]
        is_change_end_text = (self.quotation.end_text == "TEST 1\nTEST 2")
        print(bcolors.HEADER + 'change end text quotation ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if is_change_end_text else bcolors.FAIL + "KO", bcolors.ENDC)
        return (insqdao and chpyqdao and is_change_end_text)

    def __quotation_item_db(self):
        print(bcolors.BOLD + '---------- QuotationItem DB ----------' + bcolors.ENDC)
        if not self.quotation:
            print(bcolors.HEADER + 'no quotation ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if False else bcolors.FAIL + "Please call __quotation_db()", bcolors.ENDC)
            return
        self.quotation_item = QuotationItem()
        self.quotation_item.description = ""
        self.quotation_item.id_quotation = self.quotation.id
        self.quotation_item.quantity = 12
        self.quotation_item.quantity_text = "12m2"
        self.quotation_item.reduction = False
        self.quotation_item.unit_price = 1.34

        insqidao = self.qidao.insert(self.quotation_item)
        print(bcolors.HEADER + 'insert quotationitem ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if insqidao else bcolors.FAIL + "KO", bcolors.ENDC)
        self.quotation_item.description = "Fondation en pierre"
        chdscqidao = self.qidao.update(self.quotation_item)
        print(bcolors.HEADER + 'update quotationitem ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if chdscqidao else bcolors.FAIL + "KO", bcolors.ENDC)
        get_quotation_item_list = self.qidao.get(self.qidao.where('description', self.quotation_item.description))
        print(bcolors.HEADER + 'get quotationitem ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if get_quotation_item_list else bcolors.FAIL + "KO", bcolors.ENDC)
        if not get_quotation_item_list:
            return False
        self.quotation_item = get_quotation_item_list[0]
        is_change_description = (self.quotation_item.description == "Fondation en pierre")
        print(bcolors.HEADER + 'change end text quotationitem ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if is_change_description else bcolors.FAIL + "KO", bcolors.ENDC)
        return (insqidao and chdscqidao and is_change_description)

    def run_invoice(self):
        ret = False
        if self.__init_db():
            ret = (self.__profile_db() and self.__client_db() and self.__invoice_db() and self.__enterprise_db())
            self.drop_db()
        return ret

    def run_quotation(self):
        ret = False
        if self.__init_db():
            ret = (self.__profile_db() and self.__client_db() and self.__quotation_db() and self.__quotation_item_db() and self.__enterprise_db())
            self.drop_db()
        return ret

if __name__ == "__main__":
    directory_test = 'test_dir'
    os.makedirs(directory_test, exist_ok=True)
    DB_PATH = directory_test + os.sep + 'test_db'
    open(DB_PATH, 'w').close()
    DEBUG = False
    format_log = '(%(asctime)s)(%(filename)s:%(lineno)d) %(levelname)s >> %(message)s'
    format_date = '%d/%m/%Y %I:%M:%S'
    if not DEBUG:
        logging.basicConfig(
            filename='test_works.log',filemode='w', 
            format=format_log, datefmt=format_date,
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            format=format_log, datefmt=format_date,
            level=logging.DEBUG
        )

    test = Test()
    ret = test.run_quotation()
    ret &= test.run_invoice()

    exit(not ret)