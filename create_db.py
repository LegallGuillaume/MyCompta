#!/bin/env python3

from website.models.facture import FactureDAO
from website.models.client import ClientDAO
from website.models.assurance import AssuranceDAO
from website.models.profile import ProfileDAO
from website.models.devis.devis import DevisDAO, DevisItemDAO

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
    fdao = FactureDAO()
    print(bcolors.HEADER + 'FactureDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if fdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    cdao = ClientDAO()
    print(bcolors.HEADER + 'ClientDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if cdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    adao = AssuranceDAO()
    print(bcolors.HEADER + 'AssuranceDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if adao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    pdao = ProfileDAO()
    print(bcolors.HEADER + 'ProfileDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if pdao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    ddao = DevisDAO()
    print(bcolors.HEADER + 'DevisDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if ddao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)
    didao = DevisItemDAO()
    print(bcolors.HEADER + 'DevisItemDAO ?> ' + bcolors.ENDC, bcolors.OKGREEN + 'OK' if didao.create_table() else bcolors.FAIL + "KO", bcolors.ENDC)

if __name__ == "__main__":
    main()