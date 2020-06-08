try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

__author__ = "Software Le Gall Guillaume"
__copyright__ = "Copyright (C) 2020 Le Gall Guillaume"
__license__ = "Private Domain"
__version__ = "1.1"

class Insurance:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.n_contrat = ''
        self.region = ''
        self.created = ''
        self.sel = False
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Insurance name: '{}'>".format(self.name)

class InsuranceDAO(DbDAO):
    def __init__(self):
        super().__init__('assurance')
        self.obj_type = Insurance
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'name': 'TEXT NOT NULL',
            'type': 'TEXT NOT NULL',
            'n_contrat': 'TEXT NOT NULL',
            'region': 'TEXT NOT NULL',
            'sel': 'BOOLEAN NOT NULL',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }