try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
import logging

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Insurance:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.n_contract = ''
        self.region = ''
        self.created = ''
        self.sel = False
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Insurance name: '{}'>".format(self.name)

class InsuranceDAO(DbDAO):
    def __init__(self, dbpath=None):
        super().__init__('insurance', db_path=dbpath)
        self.obj_type = Insurance
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'name': 'TEXT NOT NULL',
            'type': 'TEXT NOT NULL',
            'n_contract': 'TEXT NOT NULL',
            'region': 'TEXT NOT NULL',
            'sel': 'BOOLEAN NOT NULL',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }
    
    def exist(self, obj):
        if isinstance(obj, Insurance):
            if hasattr(obj, 'id'):
                logging.info('InsuranceDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('InsuranceDAO use existe with n_contract')
                return super().exist(self.where('n_contract', obj.n_contract))
        else:
            logging.info('InsuranceDAO use delete with WHERE')
            return super().exist(obj)
    def update(self, obj):
        if hasattr(obj, 'id'):
            logging.info('InsuranceDAO use update with id')
            return super().update(obj, self.where('id', obj.id))
        else:
            logging.info('InsuranceDAO use update with n_contract')
            return super().update(obj, self.where('n_contract', obj.n_contract))
    def delete(self, obj):
        if isinstance(obj, Insurance):
            if hasattr(obj, 'id'):
                logging.info('InsuranceDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('InsuranceDAO use delete with n_contract')
                return super().delete(self.where('n_contract', obj.n_contract))
        else:
            logging.info('InsuranceDAO use delete with WHERE')
            return super().delete(obj)