#!/bin/env python3
from website.models.insurance import InsuranceDAO
from website.models.client import ClientDAO
from website.models.invoice import InvoiceDAO
from website.models.profile import ProfileDAO, Profile
from website.models.quotation.quotation import QuotationDAO, QuotationItemDAO
import argparse
import subprocess

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

parser = argparse.ArgumentParser(description='Manage server flask')
parser.add_argument('--init', action='store_true', help='Init db')
parser.add_argument('--demo', help='Create user demo with name arg')
parser.add_argument('--testunit', action='store_true', help='launch unit test program')
parser.add_argument('--testfunc', action='store_true', help='launch functionnal test program')
parser.add_argument('--run', action='store_true', help='Run server')
args = parser.parse_args()

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

def prt(line):
    nline = line.strip().decode("utf-8")
    if nline.startswith('*'):
        nline = bcolors.OKGREEN + nline + bcolors.ENDC
    elif 'WARNING' in nline.upper():
        nline = bcolors.WARNING + nline + bcolors.ENDC
    elif 'ERROR' in nline.upper() or 'DB' in nline.upper():
        nline = bcolors.FAIL + nline + bcolors.ENDC
    elif 'GET /' in nline.upper():
        nline = bcolors.GET + nline + bcolors.ENDC
    elif 'POST /' in nline.upper():
        nline = bcolors.POST + nline + bcolors.ENDC
    print(nline)

if __name__ == "__main__":
    if args.init:
        print(bcolors.BOLD + bcolors.HEADER + 'Starting init db ...' + bcolors.ENDC)
        l_db = [InsuranceDAO(), InvoiceDAO(), ClientDAO(), ProfileDAO(), QuotationDAO(), QuotationItemDAO()]
        tab = 15
        for l in l_db:
            result = bcolors.OKBLUE + 'OK' + bcolors.ENDC if l.create_table() else bcolors.FAIL + 'KO' + bcolors.ENDC
            val = l.get_table_name()
            space = ' ' * (tab - len(val))
            print('Create table {}:{}{}'.format(val, space, result))
        print(bcolors.BOLD + bcolors.HEADER + 'End of init db' + bcolors.ENDC)
    elif args.run:
        try:
            print(bcolors.BOLD + bcolors.HEADER + 'Starting server ...' + bcolors.ENDC)
            cmd=['python3', 'website/server.py']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(p.stdout.readline, b''):
                prt(line)
        except KeyboardInterrupt:
            print(bcolors.BOLD + bcolors.HEADER + '\nEnd of server program' + bcolors.ENDC)
    elif args.demo:
        pdao = ProfileDAO()
        profile = Profile()
        profile.name = args.demo
        profile.firstname = "demo"
        profile.address = "Val Sec"
        profile.comp_address = "Domaine du chateau"
        profile.city = "Marseille"
        profile.zipcode = "13000"
        profile.country = "France"
        profile.phone = "0600000000"
        profile.email = "demo@demo.fr"
        profile.siret = "123456789101112"
        if pdao.insert(profile):
            print('Create user {}'.format(profile.name))
        else:
            print('Impossible to create user {}'.format(profile.name))
    elif args.testunit:
        try:
            cmd=['python3', 'website/unit_test.py']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(p.stdout.readline, b''):
                prt(line)
            p.poll()
            exit(p.returncode)
        except KeyboardInterrupt:
            exit(1)
    elif args.testfunc:
        try:
            cmd=['python3', 'website/test_works.py']
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in iter(p.stdout.readline, b''):
                prt(line)
            p.poll()
            exit(p.returncode)
        except KeyboardInterrupt:
            exit(1)
    else:
        parser.print_help()