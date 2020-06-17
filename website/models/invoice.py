try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
import logging

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Invoice:
    def __init__(self):
        self.name = ''
        self.id_client = 0
        self.project = ''
        self.date_sent = ''
        self.date_expiry = ''
        self.max_delay = ''
        self.total = ''
        self.total_tax = ''
        self.tax = False
        self.days = 0
        self.day_rate = 0
        self.sold = False
        self.created = ''
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Invoice name: '{}'>".format(self.name)

class InvoiceDAO(DbDAO):
    def __init__(self, dbpath=None):
        super().__init__('invoice',db_path=dbpath)
        self.obj_type = Invoice
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'name': 'text  NOT NULL',
            'id_client': 'INTEGER NOT NULL',
            'project': 'TEXT',
            'date_sent': 'TEXT',
            'date_expiry': 'TEXT',
            'max_delay': 'TEXT',
            'tax': 'BOOLEAN',
            'days': 'INTEGER',
            'day_rate': 'FLOAT',
            'total': 'TEXT',
            'sold': 'BOOLEAN',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }

    def exist(self, obj):
        if isinstance(obj, Invoice):
            if hasattr(obj, 'id'):
                logging.info('InvoiceDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('InvoiceDAO use exist with name')
                return super().exist(self.where('name', obj.name))
        else:
            logging.info('InvoiceDAO use exist with WHERE')
            return super().exist(obj)

    def insert(self, obj):
        cpy = obj.total_tax
        del obj.total_tax
        ret = super().insert(obj)
        obj.total_tax = cpy
        return ret

    def update(self, obj):
        cpy = obj.total_tax
        del obj.total_tax
        ret = super().update(obj, self.where('name', obj.name))
        obj.total_tax = cpy
        return ret

    def delete(self, obj):
        if isinstance(obj, Invoice):
            if hasattr(obj, 'id'):
                logging.info('InvoiceDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('InvoiceDAO use delete with name')
                return super().delete(self.where('name', obj.name))
        else:
            logging.info('InvoiceDAO use delete with WHERE')
            return super().delete(obj)