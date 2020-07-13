#!/bin/env python3
from website.models.insurance import InsuranceDAO
from website.models.client import ClientDAO
from website.models.enterprise import EnterpriseDAO
from website.models.invoice import InvoiceDAO
from website.models.profile import ProfileDAO, Profile
from website.models.quotation.quotation import QuotationDAO, QuotationItemDAO
from website.settings.config import DB_PATH
import argparse
import subprocess

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

parser = argparse.ArgumentParser(description='Manage server flask')
parser.add_argument('--init', action='store_true', help='Init db')
parser.add_argument('--demo', help='Create user demo with name arg')
parser.add_argument('--testunit', action='store_true', help='launch unit test program')
parser.add_argument('--testfunc', action='store_true', help='launch functionnal test program')
parser.add_argument('--create', action='store_true', help='Create profile')
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


def input_custom(text):
    ret = ''
    while (ret.rstrip() == ''):
        print(text)
        ret = input()
    if ret.rstrip() in ['exit', 'quit']:
        return None
    return ret.rstrip()

if __name__ == "__main__":
    if args.init:
        open(DB_PATH, 'w').close() # create prog_db if not exist
        print(bcolors.BOLD + bcolors.HEADER + 'Starting init db ...' + bcolors.ENDC)
        l_db = [InsuranceDAO(), InvoiceDAO(), ClientDAO(), ProfileDAO(), QuotationDAO(), QuotationItemDAO(), EnterpriseDAO()]
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
    elif args.create:
        import getpass
        lastname=None;firstname=None;address=None;comp_addr=None;city=None
        zipcode=None;country=None;phone=None;email=None;siret=None;passwd=None
        print(bcolors.BOLD + bcolors.HEADER + 'Creating profile into db ...' + bcolors.ENDC)
        lastname = input_custom(bcolors.BOLD + '  Lastname:' + bcolors.ENDC)
        if lastname is not None:
            firstname = input_custom(bcolors.BOLD + '  Firstname:' + bcolors.ENDC)
        if firstname is not None:
            email = input_custom(bcolors.BOLD + '  Email:' + bcolors.ENDC)
        if email is not None:
            passwd = ''
            password_check = ''
            while passwd.rstrip() in ['', 'exit', 'quit'] or passwd.rstrip() != password_check.rstrip():
                print(bcolors.BOLD + '  Password:' + bcolors.ENDC)
                passwd = ''
                password_check = ''
                passwd = getpass.getpass()
                if passwd.rstrip() == ['exit', 'quit']:
                    passwd = None
                    break
                print(bcolors.BOLD + '  Confirm password:' + bcolors.ENDC)
                password_check = getpass.getpass()
                if password_check.rstrip() == ['exit', 'quit']:
                    password_check = None
                    break
        if passwd is not None:
            siret = input_custom(bcolors.BOLD + '  Siret:' + bcolors.ENDC)
        if siret is None:                          
            print(bcolors.BOLD + bcolors.FAIL + 'Stop creating profile into db' + bcolors.ENDC)
            exit(1)

        pdao = ProfileDAO()
        profile = Profile()
        profile.name = lastname
        profile.firstname = firstname
        profile.address = address
        profile.comp_address = comp_addr
        profile.city = city
        profile.zipcode = zipcode
        profile.country = country
        profile.phone = phone
        profile.email = email
        profile.siret = siret
        profile.password = passwd
        if pdao.insert(profile):
            print('Create user {}'.format(profile.name))
        else:
            print('Impossible to create user {}'.format(profile.name))

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


