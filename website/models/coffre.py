try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

class Coffre:
    def __init__(self):
        self.tauxcharge = 0
        self.charge = 0
        self.tauximpot = 0
        self.impot = 0
        self.tauxtva = 0
        self.tva = 0
        self.tauxfiscal = 0
        self.fiscal = 0
        self.total = 0
        self.created = ''
        self.id_profile = -1
        self.id_facture = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Coffre factureid: '{}'>".format(self.id_facture)

class CoffreDAO(DbDAO):
    def __init__(self):
        super().__init__('coffre')
        self.obj_type = Coffre
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
            'tauxcharge': 'INTEGER NOT NULL',
            'charge': 'INTEGER NOT NULL',
            'tauxtva': 'INTEGER NOT NULL',
            'tva': 'INTEGER NOT NULL',
            'tauximpot': 'INTEGER NOT NULL',
            'impot': 'INTEGER NOT NULL',
            'tauxfiscal': 'INTEGER NOT NULL',
            'fiscal': 'INTEGER NOT NULL',
            'total': 'INTEGER NOT NULL',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL',
            'id_facture': 'INTEGER NOT NULL'
        }