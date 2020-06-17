try:
    from models.db import DbDAO
    from models.quotation.item_quotation import QuotationItem, QuotationItemDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO
    from website.models.quotation.item_quotation import QuotationItem, QuotationItemDAO
import logging

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Quotation:
    def __init__(self):
        self.number = -1
        self.date_sent = ''
        self.date_validity = ''
        self.client = ''
        self.id_profile = -1
        self.total = 0.0
        self.tax_price = 0.0
        self.end_text = '' # comme acompte, n°TVA
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Quotation N°{}>".format(self.number)

    def add_item(self, item):
        if not isinstance(item, QuotationItem):
            return
        if not hasattr(self, 'list_item'):
            self.list_item = list()
        item.id_quotation = self.id
        new_price = (item.quantity*item.unit_price)
        if not item.reduction:
            self.total += new_price
        else:
            self.total = max(0, self.total-new_price)
        self.list_item.append(item)

class QuotationDAO(DbDAO):
    def __init__(self, dbpath=None):
        super().__init__('quotation', db_path=dbpath)
        self.obj_type = Quotation
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'number': 'INTEGER NOT NULL',
            'total': 'FLOAT NOT NULL',
            'tax_price': 'FLOAT NOT NULL',
            'client': 'TEXT NOT NULL',
            'date_validity': 'TEXT NOT NULL',
            'date_sent': 'TEXT NOT NULL',
            'end_text': 'TEXT NOT NULL',
            'created': 'TEXT NOT NULL',
            'id_profile': 'INTEGER NOT NULL'
        }

    def exist(self, obj):
        if isinstance(obj, Quotation):
            if hasattr(obj, 'id'):
                logging.info('QuotationDAO use exist with id')
                return super().exist(self.where('id', obj.id))
            else:
                logging.info('QuotationDAO use exist with number')
                return super().exist(self.where('number', obj.number))
        else:
            logging.info('QuotationDAO use exist with WHERE')
            return super().exist(obj)

    def get(self, where=None):
        obj = super().get(where)
        for o in obj:
            itemdao = QuotationItemDAO()
            itemdao.create_table() # if not exist
            o.list_item = itemdao.get(itemdao.where('id_quotation', o.id))
        return obj

    def insert(self, obj):
        list_item = list()
        if hasattr(obj, 'list_item'):
            list_item = obj.list_item
            del obj.list_item
        ret = super().insert(obj)
        obj.list_item = list_item
        return ret

    def update(self, obj):
        list_item = obj.list_item
        del obj.list_item
        ret = super().update(obj, self.where('number', obj.number))
        obj.list_item = list_item
        return ret

    def delete(self, obj):
        if isinstance(obj, Quotation):
            if hasattr(obj, 'id'):
                logging.info('QuotationDAO use delete with id')
                return super().delete(self.where('id', obj.id))
            else:
                logging.info('QuotationDAO use delete with number')
                return super().delete(self.where('number', obj.number))
        else:
            logging.info('QuotationDAO use delete with WHERE')
            return super().delete(obj)