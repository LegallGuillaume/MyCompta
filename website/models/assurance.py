try:
    from models.db import DbDAO
except ModuleNotFoundError:
    from website.models.db import DbDAO

class Assurance:
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
        return "<Assurance name: '{}'>".format(self.name)

class AssuranceDAO(DbDAO):
    def __init__(self):
        super().__init__('assurance')
        self.obj_type = Assurance
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