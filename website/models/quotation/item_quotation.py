try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class QuotationItem:
    def __init__(self):
        self.description = ''
        self.unit_price = 0.0
        self.quantity = 0.0
        self.quantity_text = ''
        self.reduction = False
        self.id_devis = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<QuotationItem pour N°{}>".format(self.id_devis)

class QuotationItemDAO(DbDAO):
    def __init__(self):
        super().__init__('devis_item')
        self.obj_type = QuotationItem
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'description': 'TEXT NOT NULL',
            'unit_price': 'FLOAT NOT NULL',
            'quantity': 'FLOAT NOT NULL',
            'quantity_text': 'TEXT NOT NULL',
            'reduction': 'BOOLEAN NOT NULL',
            'created': 'TEXT NOT NULL',
            'id_devis': 'INTEGER NOT NULL'
        }