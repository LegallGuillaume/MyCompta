try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
import logging

__author__ = "Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__website__ = "www.gyca.fr"
__license__ = "BSD-2"
__version__ = "1.0"

class Enterprise:
    def __init__(self):
        self.id_profile = -1
        self.name = ''
        self.slogan = ''
        self.address = ''
        self.comp_address = ''
        self.zipcode = ''
        self.city = ''
        self.country = ''
        self.siret = ''
        self.phone = ''
        self.email = ''
        self.created = ''

    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Enterprise name: '{}' | siret: '{}'>".format(self.name, self.siret)

class EnterpriseDAO(DbDAO):
    def __init__(self, dbpath=None):
        super().__init__('enterprise', db_path=dbpath)
        self.obj_type = Enterprise
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'id_profile': 'INT NOT NULL',
            'name': 'TEXT NOT NULL',
            'slogan': 'TEXT',
            'address': 'TEXT',
            'comp_address': 'TEXT',
            'zipcode': 'TEXT',
            'city': 'TEXT',
            'country': 'TEXT',
            'siret': 'TEXT UNIQUE',
            'phone': 'TEXT',
            'email': 'TEXT',
            'created': 'TEXT'
        }

    def get_list_enterprise(self):
        return self.get()

    def exist(self, obj):
        if isinstance(obj, Enterprise):
            if hasattr(obj, 'id'):
                logging.info('EnterpriseDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('EnterpriseDAO use exist with siret')
                return super().exist(self.where('siret', obj.siret))
        else:
            logging.info('EnterpriseDAO use exist with WHERE')
            return super().exist(obj)

    def update(self, obj, where=None):
        if not where:
            if hasattr(obj, 'id'):
                logging.info('EnterpriseDAO use update with id')
                return super().update(obj, self.where('id', obj.id))
            else:
                logging.info('EnterpriseDAO use update with siret')
                return super().update(obj, self.where('siret', obj.siret))
        else:
            logging.info('EnterpriseDAO use update')
            return super().update(obj, where)

    def delete(self, obj):
        if isinstance(obj, Enterprise):
            if hasattr(obj, 'id'):
                logging.info('EnterpriseDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('EnterpriseDAO use delete with siret')
                return super().delete(self.where('siret', obj.siret))
        else:
            logging.info('EnterpriseDAO use delete with WHERE')
            return super().delete(obj)
