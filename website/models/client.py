try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

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
    def __init__(self):
        super().__init__('client')
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