try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

class Invoice:
    def __init__(self):
        self.name = ''
        self.id_client = 0
        self.projet = ''
        self.date_envoi = ''
        self.date_echeance = ''
        self.delai_max = ''
        self.total = ''
        self.total_ttc = ''
        self.tva = False
        self.days = 0
        self.tjm = 0
        self.payee = False
        self.created = ''
        self.id_profile = -1
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return "<Invoice name: '{}'>".format(self.name)

class InvoiceDAO(DbDAO):
    def __init__(self):
        super().__init__('facture')
        self.obj_type = Invoice
        self.table_create = {
            'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'name': 'text  NOT NULL',
            'id_client': 'INTEGER NOT NULL',
            'projet': 'TEXT',
            'date_envoi': 'TEXT',
            'date_echeance': 'TEXT',
            'delai_max': 'TEXT',
            'tva': 'BOOLEAN',
            'days': 'INTEGER',
            'tjm': 'FLOAT',
            'total': 'TEXT',
            'payee': 'BOOLEAN',
            'created': 'TEXT',
            'id_profile': 'INTEGER NOT NULL'
        }