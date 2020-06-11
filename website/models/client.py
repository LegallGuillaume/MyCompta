try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
import logging

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Client:
    def __init__(self):
        self.name = ''
        self.adresse = ''
        self.comp_adresse = ''
        self.cp = ''
        self.ville = ''
        self.pays = ''
        self.created = ''
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Client name: '{}'>".format(self.name)

class ClientDAO(DbDAO):
    def __init__(self,dbpath=None):
        super().__init__('client', db_path=dbpath)
        self.obj_type = Client
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'name': 'TEXT NOT NULL',
            'adresse': 'TEXT',
            'comp_adresse': 'TEXT',
            'cp': 'TEXT',
            'ville': 'TEXT',
            'pays': 'TEXT',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }
    
    def exist(self, obj):
        if isinstance(obj, Client):
            if hasattr(obj, 'id'):
                logging.info('ClientDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('ClientDAO use exist with name')
                return super().exist(self.where('name', obj.name))
        else:
            logging.info('ClientDAO use exist with WHERE')
            return super().exist(obj)
    def update(self, obj):
        if hasattr(obj, 'id'):
            logging.info('ClientDAO use update with id')
            return super().update(obj, self.where('id', obj.id))
        else:
            logging.info('ClientDAO use update with name')
            return super().update(obj, self.where('name', obj.name))
    def delete(self, obj):
        if isinstance(obj, Client):
            if hasattr(obj, 'id'):
                logging.info('ClientDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('ClientDAO use delete with name')
                return super().delete(self.where('name', obj.name))
        else:
            logging.info('ClientDAO use delete with WHERE')
            return super().delete(obj)