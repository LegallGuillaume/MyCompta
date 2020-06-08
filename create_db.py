#!/bin/env python3

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

from website.models.invoice import InvoiceDAO
from website.models.client import ClientDAO
from website.models.insurance import InsuranceDAO
from website.models.profile import ProfileDAO, Profile
from website.models.quotation.quotation import QuotationDAO, QuotationItemDAO

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


def main():
    fdao = InvoiceDAO()
    print(bcolors.HEADER + 'InvoiceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if fdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    cdao = ClientDAO()
    print(bcolors.HEADER + 'ClientDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if cdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    adao = InsuranceDAO()
    print(bcolors.HEADER + 'InsuranceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if adao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    pdao = ProfileDAO()
    print(bcolors.HEADER + 'ProfileDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if pdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    ddao = QuotationDAO()
    print(bcolors.HEADER + 'QuotationDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if ddao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    didao = QuotationItemDAO()
    print(bcolors.HEADER + 'QuotationItemDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if didao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)

if __name__ == "__main__":
    main()