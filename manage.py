#!/bin/env python3
from website.models.insurance import InsuranceDAO
from website.models.client import ClientDAO
from website.models.invoice import InvoiceDAO
from website.models.profile import ProfileDAO, Profile
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Manage server flask')
parser.add_argument('--init', action='store_true', help='Init db')
parser.add_argument('--demo', help='Create user demo with name arg')
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
        l_db = [InsuranceDAO(), InvoiceDAO(), ClientDAO(), ProfileDAO()]
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
        profile.prenom = "demo"
        profile.adresse = "Val Sec"
        profile.comp_adresse = "Domaine du chateau"
        profile.ville = "Marseille"
        profile.cp = "13000"
        profile.pays = "France"
        profile.tel = "0600000000"
        profile.email = "demo@demo.fr"
        profile.siret = "123456789101112"
        if pdao.insert(profile):
            print('Create user {}'.format(profile.name))
        else:
            print('Impossible to create user {}'.format(profile.name))

    else:
        parser.print_help()